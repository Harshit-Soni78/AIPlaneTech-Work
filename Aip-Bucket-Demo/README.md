# GCP Bucket Demo

A comprehensive demonstration of Google Cloud Storage (GCS) operations using Python and the Google Cloud Storage client library. This project showcases how to interact with GCS buckets programmatically, including uploading, downloading, listing, viewing, editing, and organizing files.

## 🚀 Features

- **Bucket Management**: Create and manage GCS buckets
- **File Operations**: Upload, download, view, and edit files
- **Directory Structure**: Create folders and organize content
- **Authentication**: Service account-based authentication
- **Error Handling**: Robust error handling for all operations
- **Demonstration Scripts**: Ready-to-run demo scripts and Jupyter notebooks

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Cloud Platform**: Google Cloud Storage
- **Libraries**:
  - `google-cloud-storage` - Official GCS client library
  - `json` - For configuration and data handling
  - `argparse` - Command-line argument parsing

## 📋 Prerequisites

1. **Google Cloud Project**: Active GCP project with billing enabled
2. **Service Account**: Service account with Storage Admin permissions
3. **Service Account Key**: JSON key file downloaded from GCP console
4. **Python Environment**: Python 3.8 or higher

## 🔧 Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd Aip-Bucket-Demo
   ```

2. **Install dependencies**:

   ```bash
   pip install google-cloud-storage
   ```

3. **Set up credentials**:
   - Place your service account JSON key in the `env/` directory
   - Update the credentials path in the scripts as needed

## 🎯 Usage

### Command Line Demo

Run the main demonstration script:

```bash
python gcp_bucket_demo.py --credentials env/your-service-account-key.json
```

**Available options**:

- `--credentials`: Path to service account JSON key (default: `env/sodium-lodge-462105-a5-8bd3b06c45b2.json`)
- `--bucket-suffix`: Bucket name suffix (default: `-demo-bucket-aip`)
- `--demo-plan`: Path to demo plan JSON file (default: `demo_plan.json`)

### Jupyter Notebook Demo

Open and run `Demo.ipynb` for an interactive demonstration:

```bash
jupyter notebook Demo.ipynb
```

### GCS Manager Class

Use the `GCSManager` class for programmatic access:

```python
from gcs_manager import GCSManager

# Initialize manager
gcs = GCSManager('path/to/credentials.json', 'your-bucket-name')

# Perform operations
gcs.upload_file('local_file.txt', 'remote_file.txt')
gcs.list_files()
gcs.download_file('remote_file.txt', 'downloaded_file.txt')
```

## 📁 Project Structure

```bash
Aip-Bucket-Demo/
├── gcs_manager.py              # Core GCS operations class
├── gcp_bucket_demo.py          # Command-line demo script
├── Demo.ipynb                  # Jupyter notebook demo
├── demo_plan.json              # Demonstration plan configuration
├── demo_upload.txt             # Sample upload file
├── demo_downloaded.txt         # Download destination
├── 3.guide_to_use_this_resource.md  # User guide
├── env/                        # Service account credentials (not committed)
└── README.md                   # This file
```

## 🔍 Demo Plan Configuration

The `demo_plan.json` file defines the sequence of operations to perform:

```json
[
  {
    "action": "list_all_project_buckets",
    "params": {}
  },
  {
    "action": "upload_file",
    "params": {
      "source_file_path": "demo_upload.txt",
      "destination_blob_name": "my-test-file.txt"
    }
  }
]
```

**Available actions**:

- `list_all_project_buckets`: List all buckets in the project
- `upload_file`: Upload a local file to GCS
- `list_files`: List all files in the bucket
- `view_file`: Display file content
- `download_file`: Download file from GCS
- `edit_file`: Update file content
- `create_folder`: Create a folder structure
- `list_directories`: List folder structure

## 🔐 Authentication

### Service Account Setup

1. **Create Service Account** in GCP Console:

   - Go to IAM & Admin > Service Accounts
   - Create new service account with Storage Admin role

2. **Download Key**:

   - Generate and download JSON key file
   - Store securely (never commit to version control)

3. **Environment Setup**:

   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account-key.json"
   ```

## 📊 GCS Operations

### Bucket Operations

- **Create Bucket**: Automatically created if it doesn't exist
- **List Buckets**: View all buckets in your project
- **Bucket Permissions**: Configured via service account roles

### File Operations

- **Upload**: Local files to GCS with custom blob names
- **Download**: GCS files to local filesystem
- **View Content**: Display text file contents directly
- **Edit Content**: Update file content in-place
- **Delete Files**: Remove files from bucket

### Organization

- **Folders**: Create pseudo-folders using blob naming
- **Directory Listing**: Navigate folder structures
- **File Organization**: Logical grouping with prefixes

## 🚨 Error Handling

The demo includes comprehensive error handling for:

- **Authentication failures**: Invalid credentials or permissions
- **Network issues**: Connection timeouts and retries
- **File operations**: Missing files, permission errors
- **Bucket conflicts**: Name conflicts and access issues

## 🔒 Security Best Practices

- **Never commit credentials** to version control
- **Use environment variables** for sensitive data
- **Implement least privilege** access for service accounts
- **Rotate keys regularly** and revoke unused ones
- **Monitor access logs** for suspicious activity

## 📈 Performance Considerations

- **Batch Operations**: Use batch requests for multiple files
- **Chunked Uploads**: For large files, use resumable uploads
- **Caching**: Implement caching for frequently accessed data
- **Compression**: Compress data before storage
- **Lifecycle Policies**: Set up automatic deletion rules

## 🤝 Integration Examples

### With Flask Applications

```python
from flask import Flask
from gcs_manager import GCSManager

app = Flask(__name__)
gcs = GCSManager('credentials.json', 'my-bucket')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Handle file upload to GCS
    pass
```

### With Data Processing Pipelines

```python
import pandas as pd
from gcs_manager import GCSManager

gcs = GCSManager('credentials.json', 'data-bucket')

# Download and process data
gcs.download_file('data.csv', 'local_data.csv')
df = pd.read_csv('local_data.csv')
# Process data...
gcs.upload_file('processed_data.csv', 'results/processed.csv')
```

## 📝 Logging and Monitoring

- **Operation Logging**: All operations are logged with timestamps
- **Error Tracking**: Detailed error messages for debugging
- **Progress Monitoring**: Real-time progress for long operations
- **Audit Trail**: Complete record of all GCS interactions

## 🔄 CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: GCS Demo CI
on: [push]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.8"
      - name: Install dependencies
        run: pip install google-cloud-storage
      - name: Run demo
        run: python gcp_bucket_demo.py
        env:
          GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GCP_SA_KEY }}
```

## 🐛 Troubleshooting

### Common Issues

1. **Authentication Error**:

   - Verify service account key path
   - Check service account permissions
   - Ensure project ID is correct

2. **Bucket Not Found**:

   - Verify bucket name and region
   - Check if bucket exists in GCP console
   - Confirm service account has access

3. **File Upload/Download Issues**:
   - Check file paths and permissions
   - Verify network connectivity
   - Ensure sufficient storage quota

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📚 Additional Resources

- [Google Cloud Storage Documentation](https://cloud.google.com/storage/docs)
- [Python Client Library Reference](https://googleapis.dev/python/storage/latest/index.html)
- [GCP Best Practices](https://cloud.google.com/storage/docs/best-practices)
- [Service Account Authentication](https://cloud.google.com/docs/authentication/production)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions and support:

- Create an issue in the repository
- Check the troubleshooting section
- Review GCP documentation

---

**Note**: This demo is for educational purposes. In production environments, implement additional security measures and error handling.
