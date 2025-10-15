import os
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

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
            raise FileNotFoundError(f"Base vector store not found at {path}. Please ensure it's created and available in the mounted volume.")
    return _base_db

class RAGManager:
    """Manages the RAG process for a single user session."""
    def __init__(self, base_db_path):
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0.1, convert_system_message_to_human=True)

        # Load base vector store (from global cache if available)
        base_db = load_base_db(base_db_path, self.embeddings)

        # Create a session-specific, in-memory vector store that starts with the base data.
        self.db = FAISS.from_documents([], self.embeddings) # Start with an empty store
        self.db.merge_from(base_db) # Merge the base documents in

        # Initialize conversational memory for this session
        self.memory = ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True,
            output_key='answer'
        )

        # Initialize the conversational chain
        self.chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.db.as_retriever(search_kwargs={"k": 5}),
            memory=self.memory,
            return_source_documents=True,
            output_key='answer',
            verbose=True
        )

