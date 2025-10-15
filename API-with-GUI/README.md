# API with GUI

A full-stack web application combining a REST API backend with an interactive web interface. Built with Flask and modern web technologies, this project demonstrates CRUD operations, cloud storage integration, and real-time data synchronization between frontend and backend.

## 🚀 Features

- **Full-Stack Application**: REST API backend with web frontend
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Cloud Storage Integration**: Google Cloud Storage for data persistence
- **Interactive Web Interface**: Bootstrap-based responsive UI
- **Real-Time Updates**: Dynamic data synchronization
- **Error Handling**: Comprehensive error handling and user feedback
- **Data Validation**: Client and server-side validation
- **RESTful Design**: Proper REST API architecture

## 🛠️ Tech Stack

### Backend

- **Framework**: Flask (Python web framework)
- **Cloud Storage**: Google Cloud Storage
- **Data Format**: JSON for data exchange
- **Authentication**: Service account authentication

### Frontend

- **HTML5**: Semantic markup
- **CSS3**: Custom styling with Bootstrap
- **JavaScript**: Vanilla JS for interactivity
- **Bootstrap**: Responsive UI components

## 📋 Prerequisites

- Python 3.8 or higher
- Flask web framework
- Google Cloud Storage account and credentials
- Modern web browser
- Internet connection for cloud operations

## 🔧 Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd API-with-GUI
   ```

2. **Install Python dependencies**:

   ```bash
   pip install flask google-cloud-storage
   ```

3. **Set up Google Cloud credentials**:

   - Place service account JSON key in `env/` directory
   - Update `SERVICE_ACCOUNT_PATH` in `app.py` if needed

4. **Configure bucket name**:
   - Update `BUCKET_NAME` in `app.py` to your GCS bucket

## 🎯 Usage

### Starting the Application

Run the Flask application:

```bash
python app.py
```

Access the application at `http://127.0.0.1:5000/`

### Web Interface Features

#### User Management Dashboard

- **View Users**: Display all users in a table format
- **Add Users**: Form to create new users with name and age
- **Edit Users**: Inline editing of existing user data
- **Delete Users**: Remove users with confirmation
- **Real-time Updates**: Changes reflect immediately

#### Cloud Storage Operations

- **Upload Data**: Sync local data to Google Cloud Storage
- **Download Data**: Fetch latest data from cloud storage
- **Data Persistence**: Automatic backup to cloud

## 📁 Project Structure

```bash
API-with-GUI/
├── app.py                    # Main Flask application
├── users.json               # Local user data storage
├── env/                     # Service account credentials
├── static/                  # CSS, JS, images
├── templates/
│   ├── index.html          # Main dashboard template
│   └── (other templates)
└── README.md               # This documentation
```

## 🔍 API Endpoints

### User Management

```bash
GET    /              # Main dashboard
GET    /get_users     # Retrieve all users (JSON)
GET    /get_user/<id> # Retrieve specific user (JSON)
POST   /add_user      # Create new user
PUT    /update_user/<id> # Update existing user
DELETE /delete_user/<id> # Delete user
```

### Cloud Storage

```bash
GET    /download_from_gcp  # Download data from GCS
POST   /upload_to_gcp      # Upload data to GCS
```

## 🌐 Web Interface

### Dashboard Layout

- **Navigation**: Clean header with application title
- **User Table**: Responsive table displaying user data
- **Action Buttons**: Add, edit, delete, and sync operations
- **Status Messages**: Real-time feedback for operations
- **Forms**: Modal dialogs for user input

### User Interactions

- **Add User**: Click "Add User" button to open form modal
- **Edit User**: Click edit icon in table row
- **Delete User**: Click delete icon with confirmation
- **Sync Data**: Upload/download buttons for cloud operations

## ☁️ Google Cloud Storage Integration

### Setup Requirements

1. **GCP Project**: Active Google Cloud project
2. **Storage Bucket**: Created GCS bucket for data storage
3. **Service Account**: Account with Storage Object Admin permissions
4. **Credentials**: JSON key file for authentication

### Configuration

```python
SERVICE_ACCOUNT_PATH = "env/your-service-account-key.json"
BUCKET_NAME = 'your-bucket-name'
GCS_DESTINATION_BLOB_NAME = "users.json"
```

### Operations

- **Upload**: Local `users.json` → GCS bucket
- **Download**: GCS bucket → Local `users.json`
- **Sync**: Bidirectional data synchronization
- **Backup**: Automatic cloud backup on operations

## 🔒 Security Features

### Authentication

- Service account authentication for GCS
- Secure credential storage in environment
- No hardcoded secrets in source code

### Data Validation

- **Client-side**: JavaScript form validation
- **Server-side**: Flask request validation
- **Type checking**: Age as integer validation
- **Required fields**: Name and age mandatory

### Error Handling

- **HTTP Status Codes**: Proper REST API responses
- **User Feedback**: Clear error messages
- **Logging**: Server-side operation logging
- **Graceful Degradation**: Fallback for failed operations

## 🎨 Frontend Implementation

### HTML Structure

```html
<div class="container">
  <div class="row">
    <div class="col-md-12">
      <h1>User Management System</h1>
      <table id="users-table" class="table">
        <!-- User data rows -->
      </table>
    </div>
  </div>
</div>
```

### JavaScript Functionality

```javascript
// Add user function
function addUser() {
  const name = document.getElementById("name").value;
  const age = document.getElementById("age").value;

  fetch("/add_user", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, age }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Handle response
      updateUserTable();
    });
}
```

### CSS Styling

- Bootstrap framework for responsive design
- Custom CSS for enhanced UI elements
- Status indicators and feedback styling
- Mobile-responsive layout

## 🔄 Data Flow

### Local Operations

1. **User Action** → Frontend JavaScript
2. **AJAX Request** → Flask backend
3. **Data Processing** → Update `users.json`
4. **Response** → Update frontend display

### Cloud Operations

1. **Sync Action** → Upload/Download request
2. **GCS API Call** → Cloud storage interaction
3. **Data Transfer** → Local ↔ Cloud synchronization
4. **Status Update** → User feedback

## 📊 Data Management

### Local Storage

- **File-based**: `users.json` for data persistence
- **In-memory**: Runtime data manipulation
- **Backup**: Automatic local file updates

### Cloud Storage

- **Blob Storage**: JSON files in GCS buckets
- **Versioning**: File overwrite with latest data
- **Access Control**: Service account permissions
- **Global Access**: Data available worldwide

## 🚀 Deployment

### Local Development

```bash
# Run with debug mode
export FLASK_ENV=development
python app.py
```

### Production Deployment

```bash
# Use production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 🧪 Testing

### Manual Testing

1. **Start Application**: `python app.py`
2. **Open Browser**: Navigate to `http://127.0.0.1:5000`
3. **Test CRUD**: Add, edit, delete users
4. **Test Sync**: Upload/download with cloud storage

### API Testing with curl

```bash
# Get all users
curl http://127.0.0.1:5000/get_users

# Add user
curl -X POST http://127.0.0.1:5000/add_user \
  -H "Content-Type: application/json" \
  -d '{"name": "John Doe", "age": 30}'
```

## 🔧 Troubleshooting

### Common Issues

1. **GCS Connection Failed**

   - Verify service account credentials
   - Check bucket name and permissions
   - Ensure network connectivity

2. **Data Not Syncing**

   - Confirm local file permissions
   - Check cloud storage quota
   - Verify bucket exists

3. **UI Not Updating**
   - Check browser console for JavaScript errors
   - Verify Flask routes are accessible
   - Clear browser cache

### Debug Mode

```python
app.run(debug=True)  # Enable debug mode
```

## 📈 Performance Optimization

### Frontend Optimizations

- **Minified Assets**: Compress CSS and JavaScript
- **Lazy Loading**: Load data on demand
- **Caching**: Browser caching for static assets
- **Responsive Design**: Mobile-friendly interface

### Backend Optimizations

- **Connection Pooling**: Reuse GCS connections
- **Async Operations**: Non-blocking cloud operations
- **Data Pagination**: Handle large user datasets
- **Error Recovery**: Graceful failure handling

## 🔄 Version Control

### Data Versioning

- **Local History**: File-based version tracking
- **Cloud Backup**: Timestamped cloud storage
- **Conflict Resolution**: Last-write-wins strategy
- **Audit Trail**: Operation logging

## 📚 Learning Resources

### Flask Development

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask REST API Tutorial](https://blog.miguelgrinberg.com/)

### Google Cloud Storage

- [GCS Python Client](https://googleapis.dev/python/storage/latest/index.html)
- [GCS Best Practices](https://cloud.google.com/storage/docs/best-practices)

### Web Development

- [Bootstrap Documentation](https://getbootstrap.com/)
- [JavaScript MDN](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions:

- Check the troubleshooting section
- Review Flask and GCS documentation
- Create an issue for bugs or features

---

**Note**: This application demonstrates full-stack development concepts. For production use, implement additional security measures, user authentication, and data validation.
