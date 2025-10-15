import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.retrievers import MergerRetriever
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.messages import AIMessage, HumanMessage

import config

load_dotenv()

# Global cache for the base vector store to avoid reloading from disk for every session
_base_db = None

def load_base_db(path, embeddings):
    """Loads the base FAISS vector store from the specified path into a global variable."""
    global _base_db
    if _base_db is None:
        if os.path.exists(path):
            print(f"Loading base FAISS vector store for the first time from: {path}")
            _base_db = FAISS.load_local(
                path,
                embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            # In a real scenario, you might want to create an empty base DB
            # or handle this more gracefully.
            print(f"Base vector store not found at {path}. It will be created if base_data exists, otherwise it will be skipped.")
            _base_db = None # Explicitly set to None if not found
    return _base_db


class RAGManager:
    """Manages the RAG process for a single user session."""
    def __init__(self, session_id):
        self.session_id = session_id
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set.")

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=config.EMBEDDING_MODEL,
            google_api_key=self.google_api_key
        )
        self.llm = ChatGoogleGenerativeAI(
            model=config.CHAT_MODEL,
            google_api_key=self.google_api_key,
            temperature=0.3,
            convert_system_message_to_human=True # Important for some models
        )
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.user_vector_store_path = os.path.join(config.USER_VECTOR_STORES_PATH, self.session_id)

    def _load_or_create_vector_store(self, store_path, data_path=None):
        """Loads a FAISS vector store from path, or creates it from data_path if it doesn't exist."""
        # Check for existing store first
        if os.path.exists(store_path):
            print(f"Loading existing vector store from: {store_path}")
            return FAISS.load_local(store_path, self.embeddings, allow_dangerous_deserialization=True)

        # If no store, try to create one from data_path
        if data_path and os.path.exists(data_path) and os.listdir(data_path):
            print(f"Creating new vector store from: {data_path}")
            loader = DirectoryLoader(data_path, glob="**/*.txt", loader_cls=TextLoader, show_progress=True)
            docs = loader.load()
            if not docs:
                print(f"No documents found in {data_path}. Cannot create vector store.")
                return None

            split_docs = self.text_splitter.split_documents(docs)
            vector_store = FAISS.from_documents(split_docs, self.embeddings)
            vector_store.save_local(store_path)
            print(f"Vector store created and saved to: {store_path}")
            return vector_store

        # Return None if store doesn't exist and cannot be created
        return None

    def add_text_to_user_store(self, text):
        """Adds new text to the user-specific vector store."""
        docs = self.text_splitter.create_documents([text])

        if os.path.exists(self.user_vector_store_path):
            vector_store = FAISS.load_local(self.user_vector_store_path, self.embeddings, allow_dangerous_deserialization=True)
            vector_store.add_documents(docs)
        else:
            vector_store = FAISS.from_documents(docs, self.embeddings)

        vector_store.save_local(self.user_vector_store_path)
        print(f"Updated user vector store at: {self.user_vector_store_path}")

    def get_retriever(self):
        """Gets a merged retriever for both base and user-specific knowledge."""
        # Load or create the base vector store (for general knowledge)
        # Use the global caching function
        base_vs = load_base_db(config.BASE_VECTOR_STORE_PATH, self.embeddings)

        # Load the user-specific vector store (if it exists)
        user_vs = self._load_or_create_vector_store(self.user_vector_store_path)

        retrievers = []
        if base_vs:
            retrievers.append(base_vs.as_retriever(search_kwargs={"k": 3}))
        if user_vs:
            retrievers.append(user_vs.as_retriever(search_kwargs={"k": 3}))

        if not retrievers:
            # This case happens if neither base nor user data exists.
            # We can't create a retriever, so we'll have to handle this in the answer_question method.
            return None

        # If there's more than one retriever, merge them. Otherwise, just use the one.
        if len(retrievers) > 1:
            return MergerRetriever(retrievers=retrievers)
        else:
            return retrievers[0]

    def answer_question(self, user_question, chat_history):
        """Answers a user's question based on context and chat history."""
        retriever = self.get_retriever()

        if retriever is None:
            return "I'm sorry, but no knowledge base has been loaded. Please upload a document to begin."

        # 1. Context-aware retriever to reformulate questions
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "Given a chat history and the latest user question which might reference context in the chat history, formulate a standalone question which can be understood without the chat history. Do NOT answer the question, just reformulate it if needed and otherwise return it as is."),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        history_aware_retriever = create_history_aware_retriever(self.llm, retriever, contextualize_q_prompt)

        # 2. Question-answering chain
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.\n\n{context}"),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )
        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)

        # 3. Final RAG chain
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        # Convert chat history from frontend format to LangChain message objects
        langchain_chat_history = []
        for msg in chat_history:
            if msg.get("role") == "user":
                langchain_chat_history.append(HumanMessage(content=msg.get("content")))
            elif msg.get("role") == "assistant":
                langchain_chat_history.append(AIMessage(content=msg.get("content")))

        # Invoke the chain
        result = rag_chain.invoke({"input": user_question, "chat_history": langchain_chat_history})

        return result.get("answer", "I could not find an answer.")
