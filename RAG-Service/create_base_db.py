import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader

import config

def main():
    """
    Processes all .txt files in the base_data directory and creates a FAISS vector store.
    This script should be run once to initialize the base knowledge for the RAG service.
    """
    load_dotenv()

    # Check if GOOGLE_API_KEY is set
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY environment variable not set in your .env file.")
        return

    # Ensure the base data path exists and is not empty
    if not os.path.exists(config.BASE_DATA_PATH) or not os.listdir(config.BASE_DATA_PATH):
        print(f"The directory '{config.BASE_DATA_PATH}' is empty or does not exist.")
        print("Please add your base knowledge files (e.g., aiplanetech.txt) to this directory and try again.")
        return

    print(f"Loading documents from '{config.BASE_DATA_PATH}'...")
    loader = DirectoryLoader(config.BASE_DATA_PATH, glob="**/*.txt", loader_cls=TextLoader, show_progress=True)
    docs = loader.load()

    if not docs:
        print("No .txt documents found to process.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    embeddings = GoogleGenerativeAIEmbeddings(model=config.EMBEDDING_MODEL)
    vector_store = FAISS.from_documents(split_docs, embeddings)
    vector_store.save_local(config.BASE_VECTOR_STORE_PATH)

    print(f"\nBase vector store created successfully at '{config.BASE_VECTOR_STORE_PATH}'.")

if __name__ == "__main__":
    main()