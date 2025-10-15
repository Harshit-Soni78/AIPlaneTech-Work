# Student Attendance System with Face Recognition

A comprehensive face recognition-based attendance management system built with Python, OpenCV, and Flask. The system enables automatic student enrollment, real-time face recognition, and attendance tracking through a web interface.

## 🚀 Features

- **Real-Time Face Detection**: Uses OpenCV Haar cascades for accurate face detection
- **Student Enrollment**: Capture and store face images for new students
- **Face Recognition**: LBPH (Local Binary Patterns Histograms) algorithm for recognition
- **Web Interface**: Flask-based dashboard for easy management
- **Attendance Tracking**: Automatic attendance marking with timestamps
- **Live Camera Feed**: Real-time video streaming with face detection overlays
- **Status Management**: Track entry/exit times and prevent duplicate markings
- **Data Persistence**: CSV-based storage for students and attendance records

## 🛠️ Tech Stack

- **Backend**: Python Flask
- **Computer Vision**: OpenCV
- **Face Recognition**: OpenCV LBPH Face Recognizer
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Data Storage**: CSV files
- **Image Processing**: PIL (Pillow)

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam/Camera device
- Operating System: Windows/Linux/macOS

## 🔧 Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd Student-Attendance-System
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Download Haar Cascade file**:
   - The system uses `haarcascade_frontalface_default.xml`
   - This file is included in the repository

## 🎯 Usage

### Web Interface (Recommended)

1. **Start the Flask application**:

   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to `http://127.0.0.1:5000/`

3. **Enroll New Students**:

   - Fill in student name and ID
   - Click "Start Face Capture"
   - Position face in camera view
   - Click "Start Capture" to begin image collection
   - System captures 50 face images automatically

4. **Train Recognition Model**:

   - After enrolling students, click "Train Recognition Model"
   - System trains on captured images

5. **Mark Attendance**:
   - Click "Start Face Recognition"
   - Students face the camera
   - System automatically recognizes and marks attendance

### Command Line Tools

#### Enroll Students

```bash
python capture_images.py --name "John Doe" --id "12345"
# Or run interactively
python capture_images.py
```

#### Train Model

```bash
python train_model.py
```

#### Mark Attendance

```bash
python recognize_student.py
```

## 📁 Project Structure

```bash
Student Attendance System/
├── app.py                    # Main Flask application
├── capture_images.py         # Student enrollment script
├── train_model.py           # Model training script
├── recognize_student.py     # Attendance marking script
├── requirements.txt         # Python dependencies
├── haarcascade_frontalface_default.xml  # Face detection model
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Main dashboard
│   └── attendance.html      # Attendance records page
├── static/                  # Static assets (CSS, JS, images)
├── Training_Data/           # Face images for training
├── TrainingImageLabel/      # Trained model files
├── Student_Details/         # Student information CSV
├── Student_Status/          # Daily attendance records
└── Status_Images/           # Attendance snapshot images
```

## 🔍 How It Works

### 1. Student Enrollment

- Capture 50 face images from different angles
- Store images in `Training_Data/` with naming convention: `Name.ID.Number.jpg`
- Save student details to CSV

### 2. Model Training

- Extract face features using LBPH algorithm
- Train recognizer on collected face images
- Save trained model to `TrainingImageLabel/Trainner.yml`

### 3. Face Recognition

- Detect faces in real-time video stream
- Compare detected faces with trained model
- Mark attendance if confidence < 50 (lower = better match)
- Prevent duplicate attendance for same day

### 4. Attendance Management

- Store attendance records by date
- Track entry/exit times
- Save face snapshots for verification

## 📊 System Status Monitoring

The web dashboard provides real-time status of:

- Face detection model availability
- Recognition model training status
- Number of enrolled students
- Today's attendance records

## 🔒 Security Features

- Unique student ID validation
- Confidence threshold for recognition
- Duplicate attendance prevention
- Face image snapshots for verification

## 📈 Performance Considerations

- **Training Data**: Minimum 50 images per student recommended
- **Lighting**: Ensure adequate lighting for accurate detection
- **Camera Quality**: Use good quality webcam for better results
- **Face Angle**: Train with various face angles for robustness

## 🤝 API Endpoints

- `GET /`: Main dashboard
- `GET /video_feed`: MJPEG video stream
- `POST /enroll`: Enroll new student
- `POST /recognize`: Start face recognition
- `POST /train`: Train recognition model
- `GET /api/status`: System status JSON
- `GET /attendance`: Attendance records page

## 📝 Notes

- Ensure proper lighting and camera positioning
- Students should face the camera directly during recognition
- Remove glasses/sunglasses if possible for better accuracy
- The system works best with frontal face images
- Regular model retraining improves accuracy

## 🐛 Troubleshooting

### Common Issues

1. **Camera not detected**: Check camera permissions and connections
2. **Low recognition accuracy**: Ensure good lighting and more training images
3. **Model training fails**: Check if training images exist in `Training_Data/`
4. **Face not detected**: Adjust camera angle and lighting

### Error Messages

- "Haarcascade file missing": Ensure `haarcascade_frontalface_default.xml` exists
- "Model not trained": Train the model before attempting recognition
- "No training data found": Enroll students first

## 🔄 Future Enhancements

- [ ] Multiple camera support
- [ ] Mobile app integration
- [ ] Advanced recognition algorithms (CNN-based)
- [ ] Email/SMS notifications
- [ ] Attendance analytics dashboard
- [ ] Multi-face recognition in single frame
- [ ] Time zone support

## 📄 License

This project is open-source. Feel free to use and modify as needed.

## 👥 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For issues and questions, please create an issue in the repository or contact the development team.
