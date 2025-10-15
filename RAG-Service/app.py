import os
import uuid
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS
from dotenv import load_dotenv

import config
from TextProcessor import FileConverter
from rag import RAGManager

# Load environment variables from .env file for local development
load_dotenv()

app = Flask(__name__)
CORS(app)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'json', 'txt', 'md'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_session_id():
    """
    Retrieves session_id from the request headers.
    This ID is crucial for isolating user data and conversations.
    The frontend should generate and manage this ID (e.g., using UUID).
    """
    session_id = request.headers.get('X-Session-Id')
    if not session_id:
        return None, (jsonify({"error": "X-Session-Id header is required"}), 400)
    return session_id, None

@app.route('/ingest', methods=["POST"])
def ingest_data():
    """
    A single endpoint to handle ingestion from either a file upload or a URL.
    It requires a session_id to associate the data with a user session.
    """
    session_id, error_response = get_session_id()
    if error_response:
        return error_response

    # Ingest from either a file or a URL from a JSON body
    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({"error": "Invalid or unsupported file"}), 400
        
        filename = secure_filename(file.filename)
        user_upload_dir = os.path.join(config.USER_UPLOADS_PATH, session_id)
        os.makedirs(user_upload_dir, exist_ok=True)
        filepath = os.path.join(user_upload_dir, filename)
        file.save(filepath)
        input_data = filepath
    elif request.is_json and 'url' in request.get_json():
        input_data = request.get_json()['url']
    else:
        return jsonify({"error": "No file or URL provided"}), 400

    try:
        print(f"Processing input for session {session_id}: {input_data}")
        converter = FileConverter(input_data)
        text_content = converter.convert()

        if text_content.startswith("Error"):
            return jsonify({"error": text_content}), 500

        # Add the extracted text to the user's vector store
        rag_manager = RAGManager(session_id)
        rag_manager.add_text_to_user_store(text_content)

        return jsonify({"message": "Content ingested successfully!"}), 200
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"Error during ingestion for session {session_id}: {e}")
        return jsonify({"error": f"An error occurred during ingestion: {str(e)}"}), 500


@app.route('/rag', methods=['POST'])
def ask_question():
    """
    Handles a user's question, incorporating session_id and chat history.
    """
    session_id, error_response = get_session_id()
    if error_response:
        return error_response

    data = request.get_json()
    if not data or 'query' not in data:
        return jsonify({"error": "Missing 'query' in request body"}), 400

    user_question = data['query']
    # The frontend should send the chat history. Default to an empty list if not provided.
    chat_history = data.get('history', [])

    try:
        # Each session gets its own RAGManager instance
        rag_manager = RAGManager(session_id)
        answer = rag_manager.answer_question(user_question, chat_history)
        return jsonify({"answer": answer})
    except Exception as e:
        print(f"Error during RAG query for session {session_id}: {e}")
        return jsonify({"error": f"An error occurred while processing the query: {str(e)}"}), 500

# ------------------------ Run App ------------------------
# This block is for local development. Gunicorn will run the app in production.
if __name__ == "__main__":
    # For local testing, you can use a different port than your Next.js app, e.g., 5001
    app.run(debug=True, host="0.0.0.0", port=5001)
