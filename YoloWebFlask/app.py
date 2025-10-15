from flask import Flask, render_template, Response, jsonify
import cv2
from ultralytics import YOLO
# import torch

app = Flask(__name__)

# model = YOLO("Models\\yolov8s.pt")  # Load YOLOv8 model


model = YOLO("yolo12n.pt")  # Load YOLOv8 model

current_person_ids = [] # Stores IDs of currently detected persons

def generate_frames():
    global current_person_ids
    cap = cv2.VideoCapture(0)  # Open the camera
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        # Perform tracking, filtering for 'person' class (index 0)
        # persist=True helps maintain tracks across frames
        # tracker="bytetrack.yaml" specifies a good tracking algorithm (default is BoT-SORT)
        results = model.track(frame, classes=0, persist=True, tracker="bytetrack.yaml") 
        
        temp_ids = []
        if results[0].boxes is not None and results[0].boxes.id is not None:
            # Extract track IDs for persons
            temp_ids = results[0].boxes.id.int().cpu().tolist()
        
        current_person_ids = temp_ids # Update the global list of current person IDs
        
        # Use the plot() method from Ultralytics to draw boxes, labels, and track IDs
        annotated_frame = results[0].plot()
        
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    
    cap.release()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/get_predictions')
def get_predictions():
    # Return the list of currently tracked person IDs
    return jsonify(current_person_ids)

if __name__ == '__main__':
    app.run(debug=True)
