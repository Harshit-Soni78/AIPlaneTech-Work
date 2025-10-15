# 📖 Visual Question Answering (VQA) Service

## 📌 About VQA

**Visual Question Answering (VQA)** is an AI service that takes an image and a natural language question as input and generates an appropriate answer based on the image content. This system combines computer vision and natural language processing to understand and reason about images in human-like ways.

## 🚀 Quick Start

### ▶️ Using Docker Compose (Recommended)

    ```bash
    # In the project root
    # Build and start both backend and frontend
    cd path/to/project
    docker-compose up --build
    ```

- Backend: <http://localhost:8000>
- Frontend: <http://localhost:3000>

## 🖥️ Manual Setup

### 1️⃣ Using Virtual Environment (Backend Only)

    ```bash
    # Create a virtual environment
    python -m venv venv

    # Activate venv
    # On Windows
    venv\Scripts\activate
    # On Mac/Linux
    source venv/bin/activate

    # Install dependencies
    pip install -r requirements.txt

    # Run the service
    chmod +x run.sh
    ./run.sh
    ```

### 2️⃣ Using Docker (Manual Backend Build)

    ```bash
    # Build the backend image
    # Replace <your-image-name> as needed
    docker build -t <your-image-name> .

    # Run the backend container
    # Replace <your-image-name> as needed
    docker run --env-file .env -p 8000:8000 <your-image-name>
    ```

## 🛑 Container Management

    ```bash`
    # Start container
    docker run -d --name my-vqa-container -p 8000:8000 my-vqa-image

    # Stop container
    docker stop my-vqa-container

    docker rm my-vqa-container

    # Remove image
    docker rmi my-vqa-image
    ````

## 📂 Project Structure

    ```bash
    VQA/
    ├── backend/
    │   ├── main.py
    │   ├── requirements.txt
    │   ├── run.sh
    │   ├── images/
    │   └── ...
    ├── frontend/ (or vqa-frontend/)
    │   ├── src/
    │   ├── public/
    │   ├── package.json
    │   └── ...
    ├── docker-compose.yml
    └── readme.md
    ```

## 📬 API Usage

- Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API documentation (Swagger UI).
