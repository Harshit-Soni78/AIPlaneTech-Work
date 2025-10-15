# External API Data Sourcing

A comprehensive Python project demonstrating external API integration, data fetching, authentication, and cloud storage operations. This project showcases how to consume REST APIs, handle different authentication methods, process JSON data, and store results in Google Cloud Storage.

## 🚀 Features

- **REST API Integration**: Fetch data from public REST APIs
- **Authentication Methods**: API key and Bearer token authentication
- **Data Processing**: JSON data handling and manipulation
- **Cloud Storage**: Google Cloud Storage integrationWWW
- **Error Handling**: Comprehensive error handling and logging
- **Interactive Notebooks**: Jupyter notebooks for exploration
- **Data Persistence**: Local and cloud data storage
- **Modular Design**: Reusable functions and classes

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **HTTP Client**: Requests library for API calls
- **Data Processing**: JSON for data interchange
- **Cloud Storage**: Google Cloud Storage (GCS)
- **Development Environment**: Jupyter Notebook
- **Authentication**: API keys and Bearer tokens

## 📋 Prerequisites

- Python 3.8 or higher
- Google Cloud Platform account with Storage enabled
- Service account credentials for GCS
- Internet connection for API calls
- Jupyter Notebook (for interactive demos)

## 🔧 Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd External-API-Data-Sourcing
   ```

2. **Install dependencies**:

   ```bash
   pip install requests google-cloud-storage jupyter
   ```

3. **Set up Google Cloud credentials**:
   - Create a service account in GCP
   - Download JSON key file
   - Place in `env/` directory
   - Set environment variable:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="env/your-service-account-key.json"
   ```

## 🎯 Usage

### Running the Jupyter Notebook

Launch the interactive demo:

```bash
jupyter notebook DataSourcing.ipynb
```

This notebook demonstrates:

- API data fetching
- Authentication implementation
- Data processing and storage
- Cloud upload operations

### Command Line Usage

Run individual components:

```python
from DataSourcing import fetch_api_data, fetch_api_data_with_auth, save_data_to_json

# Fetch public API data
data = fetch_api_data("https://api.restful-api.dev/objects")
print(data)

# Fetch with authentication
auth_data = fetch_api_data_with_auth("https://api.example.com/data", "your-api-key")

# Save data locally
save_data_to_json(data, "api_data.json")
```

## 📁 Project Structure

```
External API Data Sourcing/
├── DataSourcing.ipynb              # Main Jupyter notebook
├── api_data.json                  # Sample API response data
├── downloaded_workshop_data.json  # Workshop download data
├── env/                           # Service account credentials
└── README.md                      # This documentation
```

## 🔍 API Integration Concepts

### REST API Fundamentals

- **HTTP Methods**: GET, POST, PUT, DELETE
- **Status Codes**: 200 (OK), 404 (Not Found), 500 (Server Error)
- **Headers**: Content-Type, Authorization, User-Agent
- **Query Parameters**: URL parameters for filtering/sorting

### Authentication Types

```python
# API Key authentication
headers = {'X-API-Key': 'your-api-key'}

# Bearer token authentication
headers = {'Authorization': f'Bearer {token}'}

# Basic authentication
import requests
response = requests.get(url, auth=('username', 'password'))
```

### Error Handling

```python
try:
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()  # Raises exception for 4xx/5xx status
    data = response.json()
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
except json.JSONDecodeError as e:
    print(f"JSON parsing failed: {e}")
```

## ☁️ Google Cloud Storage Integration

### Setup Requirements

1. **GCP Project**: Active Google Cloud project
2. **Storage API**: Enabled Cloud Storage API
3. **Service Account**: Storage Object Admin permissions
4. **Bucket**: Created GCS bucket for data storage

### Authentication

```python
from google.cloud import storage

# Method 1: Environment variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/key.json'
client = storage.Client()

# Method 2: Explicit credentials
client = storage.Client.from_service_account_json('key.json')
```

### Basic Operations

```python
# Upload file
bucket = client.bucket('your-bucket')
blob = bucket.blob('data/api_data.json')
blob.upload_from_filename('local_file.json')

# Download file
blob.download_to_filename('downloaded_file.json')

# List files
blobs = client.list_blobs('your-bucket')
for blob in blobs:
    print(blob.name)
```

## 📊 Data Processing

### JSON Handling

```python
import json

# Parse JSON string
data = json.loads(json_string)

# Convert to JSON string
json_string = json.dumps(data, indent=4)

# Read from file
with open('data.json', 'r') as f:
    data = json.load(f)

# Write to file
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)
```

### Data Validation

```python
def validate_api_response(data):
    """Validate API response structure"""
    if not isinstance(data, list):
        raise ValueError("Expected list of objects")

    required_fields = ['id', 'name']
    for item in data:
        for field in required_fields:
            if field not in item:
                raise ValueError(f"Missing required field: {field}")

    return True
```

## 🔒 Security Best Practices

### API Security

- **HTTPS Only**: Always use HTTPS endpoints
- **API Key Protection**: Never expose keys in code
- **Rate Limiting**: Respect API rate limits
- **Input Validation**: Validate all API inputs

### Cloud Security

- **Service Accounts**: Use minimal required permissions
- **Key Rotation**: Regularly rotate service account keys
- **Bucket Security**: Configure appropriate bucket permissions
- **Access Logging**: Enable GCS access logging

## 🚀 Advanced Features

### Pagination Handling

```python
def fetch_paginated_data(api_url, api_key):
    """Fetch data from paginated API"""
    all_data = []
    page = 1

    while True:
        params = {'page': page, 'per_page': 100}
        response = requests.get(api_url, params=params,
                              headers={'Authorization': f'Bearer {api_key}'})
        data = response.json()

        if not data:  # No more data
            break

        all_data.extend(data)
        page += 1

    return all_data
```

### Retry Logic

```python
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_resilient_session():
    """Create requests session with retry logic"""
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session
```

### Async Processing

```python
import asyncio
import aiohttp

async def fetch_multiple_apis(urls):
    """Fetch data from multiple APIs concurrently"""
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)

        results = []
        for response in responses:
            data = await response.json()
            results.append(data)

        return results
```

## 🧪 Testing

### Unit Testing

```python
import unittest
from unittest.mock import patch, MagicMock

class TestAPIFunctions(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_api_data_success(self, mock_get):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {'data': 'test'}
        mock_get.return_value = mock_response

        result = fetch_api_data('http://test.com')
        self.assertEqual(result, {'data': 'test'})

    @patch('requests.get')
    def test_fetch_api_data_error(self, mock_get):
        # Mock failed API response
        mock_get.side_effect = requests.exceptions.RequestException("Network error")

        result = fetch_api_data('http://test.com')
        self.assertIsNone(result)
```

### Integration Testing

```python
def test_full_data_pipeline():
    """Test complete data fetching and storage pipeline"""
    # Fetch data
    data = fetch_api_data(TEST_API_URL)
    assert data is not None

    # Save locally
    save_data_to_json(data, 'test_data.json')
    assert os.path.exists('test_data.json')

    # Upload to cloud
    upload_to_gcs('test-bucket', 'test_data.json', 'test/data.json')

    # Verify upload
    # (Add GCS verification logic)

    # Cleanup
    os.remove('test_data.json')
```

## 📈 Performance Optimization

### Connection Pooling

```python
# Reuse HTTP connections
session = requests.Session()
adapter = HTTPAdapter(pool_connections=100, pool_maxsize=100)
session.mount('https://', adapter)
```

### Caching

```python
from cachetools import TTLCache
import hashlib

cache = TTLCache(maxsize=100, ttl=300)  # 5 minute cache

def cached_api_call(url, params=None):
    """Cache API responses to reduce redundant calls"""
    cache_key = hashlib.md5(f"{url}{str(params)}".encode()).hexdigest()

    if cache_key in cache:
        return cache[cache_key]

    response = requests.get(url, params=params)
    data = response.json()
    cache[cache_key] = data
    return data
```

### Batch Processing

```python
def process_data_in_batches(data, batch_size=100):
    """Process large datasets in batches"""
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        # Process batch
        yield batch
```

## 🚨 Troubleshooting

### Common Issues

1. **API Connection Failed**

   - Check internet connection
   - Verify API endpoint URL
   - Check API status page

2. **Authentication Error**

   - Verify API key/token validity
   - Check authentication method
   - Ensure proper header format

3. **GCS Upload Failed**

   - Verify service account credentials
   - Check bucket permissions
   - Ensure bucket exists

4. **JSON Parsing Error**
   - Validate API response format
   - Check for malformed JSON
   - Handle unexpected response types

### Debug Techniques

```python
# Enable request logging
import logging
logging.basicConfig(level=logging.DEBUG)
urllib3_logger = logging.getLogger('urllib3')
urllib3_logger.setLevel(logging.DEBUG)

# Inspect response details
response = requests.get(url)
print(f"Status: {response.status_code}")
print(f"Headers: {response.headers}")
print(f"Content: {response.text[:500]}")
```

## 📚 API Resources

### Public APIs for Testing

- [RESTful API Dev](https://api.restful-api.dev/) - Test API endpoints
- [JSONPlaceholder](https://jsonplaceholder.typicode.com/) - Fake REST API
- [ReqRes](https://reqres.in/) - Test user API
- [Public APIs](https://public-apis.io/) - Directory of public APIs

### Documentation

- [Requests Library](https://requests.readthedocs.io/)
- [Google Cloud Storage](https://cloud.google.com/storage/docs)
- [REST API Design](https://restfulapi.net/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new API integrations or improve existing ones
4. Update documentation
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions:

- Check the troubleshooting section
- Review API documentation
- Test with simple examples first
- Create an issue for bugs or features

---

**Note**: This project demonstrates API integration concepts. Always respect API terms of service, implement proper error handling, and secure sensitive credentials in production environments.
