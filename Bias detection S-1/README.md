# Bias Detection System S-1

A desktop application for managing and defining bias parameters in machine learning models. Built with Python and Tkinter, this system provides a graphical user interface for storing, editing, and tracking bias detection parameters in a SQLite database.

## 🚀 Features

- **Parameter Management**: Define and store bias detection parameters
- **Database Integration**: SQLite database for persistent storage
- **GUI Interface**: User-friendly desktop application with Tkinter
- **CRUD Operations**: Create, Read, Update, Delete parameter definitions
- **Data Validation**: Input validation and duplicate prevention
- **Search & Filter**: Sortable table view with search capabilities
- **Audit Trail**: Timestamp tracking for all operations
- **Export Capabilities**: Data export functionality

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **GUI Framework**: Tkinter (built-in Python GUI)
- **Database**: SQLite3 (built-in Python database)
- **UI Components**: ttk (themed Tkinter widgets)
- **Date/Time**: datetime module for timestamp tracking

## 📋 Prerequisites

- Python 3.8 or higher (Tkinter comes pre-installed)
- No additional dependencies required
- Windows/Linux/macOS with GUI support

## 🔧 Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd Bias-detection-S-1
   ```

2. **Run the application**:

   ```bash
   python parameter_input_gui.py
   ```

   The GUI application will launch automatically.

## 🎯 Usage

### Starting the Application

Run the main script to launch the GUI:

```bash
python parameter_input_gui.py
```

### Main Interface

#### Parameter Input Section

- **Bias Parameter Code**: Enter the unique identifier for the bias parameter
- **Description**: Provide detailed description of the bias parameter
- **Save Button**: Store the parameter in the database
- **Status Display**: Real-time feedback on operations

#### Database Viewer

- **View Database Button**: Open detailed database viewer window
- **Table Display**: Sortable table with all stored parameters
- **Edit Records**: Modify existing parameter definitions
- **Delete Records**: Remove parameters with confirmation
- **Refresh Data**: Update table with latest information

### Database Operations

#### Adding Parameters

1. Enter parameter code and description
2. Click "Save Parameters"
3. Receive confirmation or error message

#### Editing Parameters

1. Open database viewer
2. Select record to edit
3. Modify values in edit dialog
4. Save changes

#### Deleting Parameters

1. Open database viewer
2. Select one or multiple records
3. Click "Delete Selected Record(s)"
4. Confirm deletion

## 📁 Project Structure

```bash
Bias detection S-1/
├── parameter_input_gui.py     # Main GUI application
├── app_parameters.db         # SQLite database (auto-created)
├── Meet with Vinay, project selection and discussion.txt
├── previous_archive.py       # Legacy/archive code
└── README.md                 # This documentation
```

## 🗄️ Database Schema

### Parameters Table

```sql
CREATE TABLE settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    bias_parameter TEXT,
    description_bias_parameter TEXT
);
```

**Fields**:

- `id`: Auto-incrementing primary key
- `timestamp`: Automatic timestamp on record creation/update
- `bias_parameter`: Bias parameter code/name
- `description_bias_parameter`: Detailed parameter description

## 🔍 Application Features

### Input Validation

- **Required Fields**: Both parameter code and description mandatory
- **Duplicate Prevention**: Checks for existing parameter combinations
- **Data Sanitization**: Automatic whitespace trimming

### Database Viewer

- **Multi-Column Sorting**: Click column headers to sort
- **Multi-Selection**: Select multiple records for batch operations
- **Real-time Updates**: Refresh button for latest data
- **Edit Dialog**: Modal window for record editing

### Error Handling

- **Database Errors**: Comprehensive error messages
- **File System Issues**: Path and permission error handling
- **User Input Errors**: Validation feedback
- **Operation Failures**: Graceful failure handling

## 🎨 GUI Design

### Main Window Layout

```bash
+-----------------------------+
| Bias Parameters Definition  |
+-----------------------------+
|                             |
| Bias Parameter Code: [____] |
|                             |
| Description: [____________] |
|                    [Save]   |
|                             |
| Status: [messages here]     |
|                             |
| [View Database]             |
+-----------------------------+
```

### Database Viewer Window

```bash
+-----------------------------+
| Database Viewer             |
+-----------------------------+
| +------------------------+  |
| | ID | Timestamp | Param |  |
| |    |           | Code  |  |
| +------------------------+  |
| |    |           |       |  |
| +------------------------+  |
|                             |
| [Edit] [Delete] [Refresh]   |
+-----------------------------+
```

## 🔒 Data Security

### Database Security

- **Local Storage**: SQLite database stored locally
- **No Network Exposure**: Completely offline application
- **File Permissions**: Standard file system permissions
- **Backup Recommendations**: Regular database backups

### Input Security

- **SQL Injection Prevention**: Parameterized queries
- **XSS Prevention**: Input sanitization
- **Data Validation**: Type and format checking

## 📊 Data Management

### Record Operations

- **Create**: Add new bias parameter definitions
- **Read**: View all stored parameters
- **Update**: Modify existing parameter details
- **Delete**: Remove unwanted parameters

### Data Integrity

- **Unique Constraints**: Prevent duplicate parameter codes
- **Referential Integrity**: Maintain data consistency
- **Transaction Safety**: Atomic database operations

## 🚀 Advanced Features

### Sorting and Filtering

- **Column Sorting**: Click headers to sort ascending/descending
- **Search Functionality**: Filter records by content
- **Pagination**: Handle large datasets efficiently

### Batch Operations

- **Multi-Delete**: Select and delete multiple records
- **Bulk Edit**: Planned feature for batch modifications
- **Export Options**: CSV/JSON export capabilities

## 🔧 Configuration

### Database Path

The database file is automatically created in the same directory as the script:

```python
DB_ABSOLUTE_PATH = os.path.join(APPLICATION_PATH, DB_FILENAME)
```

### UI Customization

Modify appearance through Tkinter styling:

```python
# Example customization
style = ttk.Style()
style.configure("Custom.TButton", foreground="blue")
```

## 🧪 Testing

### Manual Testing Checklist

- [ ] Application launches without errors
- [ ] Database file created automatically
- [ ] Parameter input validation works
- [ ] Duplicate prevention functions
- [ ] Database viewer opens correctly
- [ ] Edit operations work properly
- [ ] Delete operations work with confirmation
- [ ] Sorting functionality works
- [ ] Error messages display correctly

### Automated Testing

```python
# Example test structure
def test_parameter_validation():
    # Test input validation logic
    pass

def test_database_operations():
    # Test CRUD operations
    pass
```

## 🚨 Troubleshooting

### Common Issues

1. **Application Won't Start**

   - Ensure Python 3.8+ is installed
   - Check if Tkinter is available (`python -c "import tkinter"`)
   - Verify file permissions

2. **Database Errors**

   - Check write permissions in application directory
   - Ensure no other application is using the database
   - Try deleting and recreating the database file

3. **GUI Display Issues**
   - Check display scaling settings
   - Ensure compatible graphics drivers
   - Try running with different DPI settings

### Debug Mode

Enable debug logging by modifying the script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📈 Performance Considerations

### Database Performance

- **Indexing**: Primary key indexing for fast lookups
- **Connection Pooling**: Efficient database connections
- **Query Optimization**: Optimized SQL queries

### UI Performance

- **Lazy Loading**: Load data on demand
- **Efficient Updates**: Minimize UI redraws
- **Memory Management**: Proper object cleanup

## 🔄 Version Control

### Data Versioning

- **Timestamp Tracking**: All changes recorded with timestamps
- **Audit Trail**: Complete history of modifications
- **Backup Strategy**: Regular database backups recommended

## 📚 Learning Resources

### Tkinter Documentation

- [Tkinter Official Docs](https://docs.python.org/3/library/tkinter.html)
- [Tkinter Tutorial](https://tkdocs.com/)

### SQLite Documentation

- [SQLite Python Docs](https://docs.python.org/3/library/sqlite3.html)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)

### GUI Design

- [Tkinter Best Practices](https://tkdocs.com/tutorial/)
- [Python GUI Programming](https://realpython.com/python-gui-tkinter/)

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
- Review Tkinter documentation
- Create an issue for bugs or features

---

**Note**: This application is designed for desktop use with GUI support. For server deployments or web interfaces, consider alternative frameworks like Flask or Django.
