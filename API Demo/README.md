# API Demo

A comprehensive demonstration of REST API development and consumption using Python and Flask. This project showcases building RESTful APIs, handling HTTP requests, data serialization, and integrating with external APIs for data sourcing.

## 🚀 Features

- **REST API Development**: Complete CRUD operations with Flask
- **External API Integration**: Fetch data from public APIs
- **Authentication Handling**: API key and Bearer token authentication
- **Data Storage**: JSON-based data persistence
- **Error Handling**: Comprehensive error handling and validation
- **Interactive Notebooks**: Jupyter notebooks for API exploration
- **Data Processing**: JSON and CSV data handling

## 🛠️ Tech Stack

- **Backend Framework**: Flask (Python web framework)
- **HTTP Client**: Requests library for API calls
- **Data Formats**: JSON for data exchange
- **Development Tools**: Jupyter Notebook for interactive demos
- **Cloud Storage**: Google Cloud Storage integration

## 📋 Prerequisites

- Python 3.8 or higher
- Flask and requests libraries
- Google Cloud Storage credentials (for cloud integration)
- Jupyter Notebook (for interactive demos)

## 🔧 Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd API-Demo
   ```

2. **Install dependencies**:

   ```bash
   pip install flask requests google-cloud-storage jupyter
   ```

3. **Set up environment** (optional):

   ```bash
   # For cloud storage integration
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
   ```

## 🎯 Usage

### Running the Flask API

Start the REST API server:

```bash
python api-making-example.py
```

The API will be available at `http://localhost:5000`

### API Endpoints

| Method | Endpoint      | Description        |
| ------ | ------------- | ------------------ |
| GET    | `/users`      | Retrieve all users |
| POST   | `/users`      | Add a new user     |
| PUT    | `/users/<id>` | Update user by ID  |
| DELETE | `/users/<id>` | Delete user by ID  |

### Example API Usage

```python
import requests

# Get all users
response = requests.get('http://localhost:5000/users')
users = response.json()

# Add new user
new_user = {'name': 'John Doe'}
response = requests.post('http://localhost:5000/users', json=new_user)
```

### External API Data Fetching

Run the data sourcing notebook:

```bash
jupyter notebook make_example_api.ipynb
```

This demonstrates:

- Fetching data from REST APIs
- Handling authentication
- Saving data to JSON files
- Uploading to cloud storage

## 📁 Project Structure

```bash
API Demo/
├── api-making-example.py       # Main Flask API application
├── make_example_api.ipynb      # Jupyter notebook for API demos
├── api_data.json              # Sample API response data
├── downloaded_workshop_data.json  # Workshop data downloads
├── Storage_Interaction_with_Cloud.ipynb  # Cloud storage integration
├── Data/                      # Data storage directory
├── env/                       # Environment configuration
└── README.md                  # This documentation
```

## 🔍 API Development Concepts

### REST Principles

- **Stateless**: Each request contains all necessary information
- **Resource-Based**: APIs expose resources (users, data, etc.)
- **HTTP Methods**: GET, POST, PUT, DELETE for CRUD operations
- **JSON Format**: Standard data exchange format

### Flask API Structure

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    # Process data...
    return jsonify(new_user), 201
```

### Error Handling

```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500
```

## 🌐 External API Integration

### Basic API Calls

```python
import requests

def fetch_api_data(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None
```

### Authentication

```python
# API Key authentication
headers = {'Authorization': f'Bearer {api_key}'}
response = requests.get(api_url, headers=headers)

# Basic authentication
response = requests.get(api_url, auth=('username', 'password'))
```

### Data Processing

```python
# Save to JSON
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

# Save to CSV
import csv
with open('data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    # Write data...
```

## ☁️ Cloud Storage Integration

### Google Cloud Storage Upload

```python
from google.cloud import storage

def upload_to_gcs(bucket_name, source_file, destination_blob):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_file)
```

### Environment Setup

```bash
# Set credentials
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"

# Or in Python
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/key.json'
```

## 📊 Data Handling

### JSON Operations

- **Serialization**: Convert Python objects to JSON strings
- **Deserialization**: Parse JSON strings to Python objects
- **File I/O**: Read/write JSON files
- **API Responses**: Return JSON from Flask endpoints

### Data Validation

```python
def validate_user_data(data):
    required_fields = ['name', 'email']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    return True
```

## 🔒 Security Considerations

### API Security

- **Input Validation**: Validate all incoming data
- **Authentication**: Implement proper auth mechanisms
- **Rate Limiting**: Prevent abuse with request limits
- **HTTPS**: Use secure connections in production

### Best Practices

- **Environment Variables**: Store sensitive data securely
- **Error Messages**: Don't expose internal details
- **Logging**: Log requests and errors appropriately
- **CORS**: Configure Cross-Origin Resource Sharing

## 🧪 Testing APIs

### Manual Testing with curl

```bash
# GET request
curl http://localhost:5000/users

# POST request
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe"}'
```

### Python Testing

```python
import requests

def test_api():
    # Test GET
    response = requests.get('http://localhost:5000/users')
    assert response.status_code == 200

    # Test POST
    data = {'name': 'Test User'}
    response = requests.post('http://localhost:5000/users', json=data)
    assert response.status_code == 201
```

## 🚀 Deployment

### Local Development

```bash
# Run with debug mode
export FLASK_ENV=development
python api-making-example.py
```

### Production Deployment

```bash
# Use production WSGI server
gunicorn -w 4 -b 0.0.0.0:5000 api-making-example:app
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "api-making-example.py"]
```

## 📈 Performance Optimization

### Flask Optimizations

- **Blueprints**: Organize large applications
- **Caching**: Implement response caching
- **Async**: Use async endpoints for I/O operations
- **Database**: Use proper database instead of in-memory storage

### API Performance

- **Pagination**: Implement pagination for large datasets
- **Compression**: Enable response compression
- **Connection Pooling**: Reuse HTTP connections
- **Load Balancing**: Distribute requests across multiple instances

## 🔄 API Versioning

### URL Versioning

```bash
/api/v1/users
/api/v2/users
```

### Header Versioning

```bash
Accept: application/vnd.api.v1+json
```

### Best Practices

- **Backward Compatibility**: Maintain old versions
- **Deprecation Notices**: Warn about deprecated endpoints
- **Documentation**: Document version differences
- **Testing**: Test all supported versions

## 📚 Learning Resources

### Flask Documentation

- [Flask Official Docs](https://flask.palletsprojects.com/)
- [Flask REST API Tutorial](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask)

### API Design

- [REST API Design Best Practices](https://restfulapi.net/)
- [JSON API Specification](https://jsonapi.org/)

### External APIs

- [Public APIs Directory](https://public-apis.io/)
- [RESTful API Testing](https://reqres.in/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new endpoints
4. Update documentation
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For questions and support:

- Review the Flask documentation
- Check API design best practices
- Create an issue for bugs or feature requests

---

**Note**: This demo focuses on educational purposes. For production APIs, implement additional security, monitoring, and scalability measures.
