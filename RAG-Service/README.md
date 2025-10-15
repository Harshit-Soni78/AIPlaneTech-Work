# RAG Service

A Flask-based Retrieval-Augmented Generation (RAG) service that enables document ingestion and intelligent question-answering using advanced AI technologies. This service processes various document formats and provides context-aware responses based on uploaded content.

## Technologies Used

This project leverages a modern, robust tech stack designed for scalable AI-powered document processing:

### Core Framework & Web Technologies

- **Flask**: Lightweight Python web framework for building RESTful APIs
- **Flask-CORS**: Cross-Origin Resource Sharing support for web integration
- **Gunicorn**: Production-ready WSGI HTTP Server for serving the Flask application

### AI & Machine Learning Stack

- **LangChain**: Comprehensive framework for building applications with large language models
- **Google Generative AI (Gemini)**: Advanced multimodal large language models for natural language processing
  - Chat Model: `gemini-1.5-flash-latest` for conversational AI
  - Embedding Model: `models/embedding-001` for semantic text representations
- **FAISS (Facebook AI Similarity Search)**: Efficient vector database for similarity search and retrieval

### Document Processing & Text Analysis

- **PyMuPDF**: High-performance PDF text extraction and processing
- **python-docx**: Microsoft Word document (.docx) parsing and text extraction
- **BeautifulSoup4**: HTML parsing and web content extraction from URLs
- **lxml**: XML and HTML processing library for robust parsing

### Data & Storage

- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping for database operations
- **Google Cloud Storage**: Cloud-based file storage integration
- **FAISS Vector Stores**: Local and user-specific vector databases for semantic search

### Development & Deployment Tools

- **Docker**: Containerization for consistent deployment across environments
- **python-dotenv**: Environment variable management for secure configuration
- **Requests**: HTTP library for URL content fetching
- **Werkzeug**: WSGI utility library for Flask integration

### Additional Libraries

- **NumPy**: Numerical computing for vector operations
- **Pydantic**: Data validation and settings management
- **Tenacity**: Retry logic for robust API interactions
- **Colorama**: Cross-platform colored terminal text

## Features

- **Multi-format Document Ingestion**: Support for PDF, DOCX, JSON, TXT, MD files, and web URLs
- **Session-based User Isolation**: Secure per-user data management with unique session IDs
- **Intelligent Text Processing**: Advanced text extraction and preprocessing from various sources
- **Vector-based Semantic Search**: FAISS-powered similarity search for relevant context retrieval
- **Conversational AI**: Context-aware question answering with chat history support
- **Scalable Architecture**: Modular design supporting base knowledge and user-specific data
- **Production Ready**: Docker containerization and Gunicorn deployment
- **Cross-platform Compatibility**: Works on Windows, Linux, and macOS

## Prerequisites

- Python 3.11 or higher
- Google Cloud API Key (for Gemini AI services)
- Docker (optional, for containerized deployment)

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd rag-service
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:

   ```bash
   GOOGLE_API_KEY=your_google_api_key_here
   MOUNT_PATH=website-data/rag-service  # Optional: defaults to local directory
   ```

## Usage

### Local Development

1. **Run the Flask application:**

   ```bash
   python app.py
   ```

   The service will start on `http://localhost:5001`

2. **Test the API endpoints** using tools like curl, Postman, or your frontend application

### API Endpoints

#### POST /ingest

Ingest documents or web content for processing.

**Headers:**

- `X-Session-Id`: Unique session identifier (required)

**Request Body (File Upload):**

- `file`: Multipart file upload (PDF, DOCX, JSON, TXT, MD)

**Request Body (URL):**

```json
{
  "url": "https://example.com/document"
}
```

**Response:**

```json
{
  "message": "Content ingested successfully!"
}
```

#### POST /rag

Query the RAG system with a question.

**Headers:**

- `X-Session-Id`: Unique session identifier (required)

**Request Body:**

```json
{
  "query": "What is the main topic of the document?",
  "history": [
    { "role": "user", "content": "Previous question" },
    { "role": "assistant", "content": "Previous answer" }
  ]
}
```

**Response:**

```json
{
  "answer": "The main topic is artificial intelligence and machine learning."
}
```

## Deployment

### Docker Deployment

1. **Build the Docker image:**

   ```bash
   docker build -t rag-service .
   ```

2. **Run the container:**

   ```bash
   docker run -p 8080:8080 -e GOOGLE_API_KEY=your_api_key rag-service
   ```

### Cloud Run Deployment

This service is optimized for deployment on Google Cloud Run with persistent volume mounts for data storage.

## Configuration

Key configuration options in `config.py`:

- **MOUNT_PATH**: Root directory for data storage (defaults to `website-data/rag-service`)
- **EMBEDDING_MODEL**: Google AI embedding model (`models/embedding-001`)
- **CHAT_MODEL**: Google AI chat model (`gemini-1.5-flash-latest`)

## Project Structure

```bash
rag-service/
├── app.py                 # Main Flask application
├── rag.py                 # RAG manager and AI logic
├── TextProcessor.py       # Document processing utilities
├── config.py              # Configuration settings
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container configuration
├── main.py                # Standalone RAG testing script
├── create_base_db.py      # Base database creation utility
└── uploadValidification.py # Input validation helpers
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Team

- Harshit Soni
- Abhijeet Sharma
- Megha Acharya
- Pawan Kumar
