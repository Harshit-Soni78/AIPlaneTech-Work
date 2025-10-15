import os

# The root path provided by the Cloud Run volume mount.
# Default to a local directory for testing.
MOUNT_PATH = os.getenv("MOUNT_PATH", "website-data/rag-service")

# --- Path Definitions ---

# Base data (e.g., aiplanetech.txt) and its vector store
BASE_DATA_PATH = os.path.join(MOUNT_PATH, "base_data")
BASE_VECTOR_STORE_PATH = os.path.join(MOUNT_PATH, "base_db")

# User-specific uploads and their vector stores
USER_UPLOADS_PATH = os.path.join(MOUNT_PATH, "user_uploads")
USER_VECTOR_STORES_PATH = os.path.join(MOUNT_PATH, "user_dbs")

# --- Ensure Directories Exist on Startup ---
os.makedirs(BASE_DATA_PATH, exist_ok=True)
os.makedirs(BASE_VECTOR_STORE_PATH, exist_ok=True)
os.makedirs(USER_UPLOADS_PATH, exist_ok=True)
os.makedirs(USER_VECTOR_STORES_PATH, exist_ok=True)

# --- Model and Embeddings Configuration ---
EMBEDDING_MODEL = "models/embedding-001"
CHAT_MODEL = "gemini-1.5-flash-latest"