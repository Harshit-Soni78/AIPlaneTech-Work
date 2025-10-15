import json
import os
from flask import Flask, render_template, request, jsonify
from google.cloud import storage
import logging

app = Flask(__name__)

# Configure basic logging if not already configured by Flask/Gunicorn
if not app.debug:
    logging.basicConfig(level=logging.INFO)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_JSON_FILE = os.path.join(BASE_DIR, "users.json")
GCS_DESTINATION_BLOB_NAME = "users.json" # Name of the file in GCS
BUCKET_NAME = 'test-bucket-90'

# Service account path (Ensure correct path)
# SERVICE_ACCOUNT_PATH = os.path.join(BASE_DIR, "env", "aip-india-webhosting-2967914d3116.json")
SERVICE_ACCOUNT_PATH = "env/sodium-lodge-462105-a5-8bd3b06c45b2.json"

storage_client = None

def get_gcp_storage_client():
    global storage_client
    if storage_client is None:
        try:
            storage_client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_PATH)
            app.logger.info("Successfully initialized Google Cloud Storage client.")
        except FileNotFoundError:
            app.logger.error(f"Service account key file not found: {SERVICE_ACCOUNT_PATH}")
        except Exception as e:
            app.logger.error(f"Failed to initialize Google Cloud Storage client: {e}")
    return storage_client

# Load users from JSON file
def load_users():
    try:
        with open(LOCAL_JSON_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

users = load_users()

# Save users to JSON file
def save_users(users):
    with open(LOCAL_JSON_FILE, "w") as f:
        json.dump(users, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html', users=users)

@app.route('/get_users', methods=['GET'])
def get_users():
    return jsonify(users), 200

@app.route('/get_user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    return jsonify(user) if user else jsonify({"error": "User not found"}), 204

@app.route('/download_from_gcp', methods=['GET'])
def download_from_gcp():
    """Downloads JSON file from GCP Bucket"""
    client = get_gcp_storage_client()
    if not client:
        return jsonify({"error": "Storage client not initialized."}), 500
    try:
        bucket = client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(GCS_DESTINATION_BLOB_NAME)
        blob.download_to_filename(LOCAL_JSON_FILE)
        return jsonify({"message": "Data downloaded from GCP successfully!", "data": load_users()}), 200
    except Exception as e:
        return jsonify({"error": f"Download failed: {str(e)}"}), 500

@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid input: No JSON data provided"}), 400
    
    name = data.get("name")
    age_str = data.get("age")

    if not name or age_str is None: # age can be 0, so check for None
        return jsonify({"error": "Invalid input: 'name' and 'age' are required"}), 400

    try:
        age = int(age_str)
    except ValueError:
        return jsonify({"error": "Invalid input: 'age' must be an integer"}), 400

    user_id = max(map(int, users.keys()), default=0) + 1
    users[str(user_id)] = {"name": name, "age": age} # Store with string key for consistency
    save_users(users)
    return jsonify({"message": "User added", "user_id": str(user_id), "user": users[str(user_id)]}), 201

@app.route('/upload_to_gcp', methods=['POST'])
def upload_to_gcp():
    """Uploads JSON file to Google Cloud Bucket with error handling"""
    client = get_gcp_storage_client()
    if not client:
        return jsonify({"error": "Storage client not initialized or failed to initialize. Check logs."}), 500
    try:
        # Ensure the local JSON file exists with the current user data before uploading
        save_users(users)
        bucket = client.get_bucket(BUCKET_NAME)
        blob_upload = bucket.blob(GCS_DESTINATION_BLOB_NAME)
        blob_upload.upload_from_filename(LOCAL_JSON_FILE)
        return jsonify({"message": "Data uploaded to GCP Bucket successfully!"}), 200
    except FileNotFoundError:
        return jsonify({"error": f"Local JSON file for upload not found: {LOCAL_JSON_FILE}"}), 404
    except Exception as e:
        return jsonify({"error": f"Upload failed: {str(e)}"}), 500

@app.route('/update_user/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    if "name" in data:
        users[user_id]["name"] = data["name"]
    if "age" in data:
        try:
            users[user_id]["age"] = int(data["age"])
        except ValueError:
            return jsonify({"error": "Age must be an integer"}), 400

    save_users(users)
    return jsonify({"message": "User updated", "user": users[user_id]}), 200

@app.route('/delete_user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        save_users(users)
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
