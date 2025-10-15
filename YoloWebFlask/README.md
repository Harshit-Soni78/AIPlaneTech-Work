# YOLO Person Tracking with Flask Web Interface

A real-time person detection and tracking system using YOLO (YOLOv12) integrated with a Flask web application. The system captures live video from a webcam, performs person tracking with unique IDs, and provides both a web interface for visualization and an API for accessing tracking data. Additionally, it includes functionality to process pre-recorded videos for batch analysis.

## 🚀 Features

- **Real-Time Person Tracking**: Uses YOLOv12 model with ByteTrack for accurate person detection and tracking across frames
- **Web Interface**: Live video stream with annotated bounding boxes and track IDs via Flask
- **API Endpoints**: RESTful API to retrieve current tracked person IDs
- **Video Processing**: Batch process video files from the `Input/` folder and save annotated outputs to `output_videos/`
- **Modular Design**: Separate scripts for live streaming and video processing

## 🛠️ Tech Stack

- **Python 3.x**
- **Flask**: Web framework for the application
- **Ultralytics YOLO**: YOLOv12 model for object detection
- **OpenCV**: Video capture and processing
- **ByteTrack**: Tracking algorithm for maintaining person identities
- **PyTorch**: Underlying deep learning framework

## 📋 Prerequisites

- Python 3.8 or higher
- Webcam (for live tracking)
- Video files in `Input/` folder (for batch processing)

## 🔧 Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd YoloWebFlask
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
   pip install -r requirenment.txt
   ```

4. **Download YOLO model**:
   - The project uses `yolo12n.pt` (place it in the root directory)
   - Download from Ultralytics or use your preferred YOLO model

## 🎯 Usage

### Live Webcam Tracking

1. **Run the Flask application**:

   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to `http://127.0.0.1:5000/`

3. **View the live stream** with person tracking annotations

### Video File Processing

1. **Place video files** in the `Input/` folder (supported formats: .mp4, .avi, .mov)

2. **Run the video processing script**:

   ```bash
   python video-demo.py
   ```

3. **Check outputs** in the `output_videos/` folder

## 📡 API Endpoints

- **GET /**: Serves the main web interface
- **GET /video_feed**: MJPEG stream of the annotated video feed
- **GET /get_predictions**: Returns JSON array of currently tracked person IDs

  ```json
  [1, 2, 3]
  ```

## 📁 Project Structure

```bash
YoloWebFlask/
├── app.py                 # Main Flask app for live tracking
├── video-demo.py          # Script for batch video processing
├── test.ipynb             # Jupyter notebook for testing YOLO
├── requirenment.txt       # Python dependencies
├── yolo12n.pt            # YOLO model weights
├── templates/
│   └── index.html        # Web interface template
├── Input/                # Folder for input video files
├── Models/               # Folder for additional models
└── output_videos/        # Folder for processed video outputs
```

## 🔍 How It Works

1. **Detection**: YOLOv12 identifies persons in each frame
2. **Tracking**: ByteTrack maintains consistent IDs across frames
3. **Annotation**: Bounding boxes and track IDs are drawn on frames
4. **Streaming**: Annotated frames are streamed to the web interface
5. **API Access**: Current track IDs are available via REST endpoint

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Notes

- Ensure your webcam is accessible for live tracking
- For video processing, videos should be in common formats (.mp4, .avi, .mov)
- The system is optimized for person tracking; modify `classes=0` in code for other objects
- Model performance may vary based on hardware and video quality

## 📄 License

This project is open-source. Feel free to use and modify as needed.
