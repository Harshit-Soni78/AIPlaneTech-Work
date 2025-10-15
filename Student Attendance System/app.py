from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, Response
import os
import subprocess
import sys
import pandas as pd
from datetime import datetime
import json
import cv2
import csv
import numpy as np
import threading
import time
from PIL import Image

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Global variables for camera streaming
recognized_student_message = ''
already_marked_message = ''
camera = None
camera_active = False
capture_mode = None  # 'enroll' or 'recognize'
student_info = {}
image_count = 0
capturing = False

# Common functions
def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def check_haarcascadefile():
    return os.path.isfile("haarcascade_frontalface_default.xml")

def get_system_status():
    """Get system status information"""
    haarcascade_status = check_haarcascadefile()
    model_trained = os.path.isfile("TrainingImageLabel/Trainner.yml")
    
    student_count = 0
    if os.path.isfile("Student_Details/students.csv"):
        try:
            df = pd.read_csv("Student_Details/students.csv")
            student_count = len(df)
        except:
            student_count = 0
    
    return {
        'haarcascade_status': haarcascade_status,
        'model_trained': model_trained,
        'student_count': student_count
    }

def get_today_attendance():
    """Get today's attendance records"""
    date = datetime.now().strftime("%Y-%m-%d")
    status_file = f"Student_Status/Status_for_{date}.csv"

    
    if os.path.isfile(status_file):
        try:
            df = pd.read_csv(status_file)
            return df.to_dict('records')
        except:
            return []
    return []

def save_student_to_csv(name, student_id):
    """Save student data to CSV file"""
    student_details = "Student_Details/"
    assure_path_exists(student_details)
    csv_file = os.path.join(student_details, "students.csv")
    
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Enrollment Date", "Enrollment Time"])
    
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        now = datetime.now()
        writer.writerow([
            student_id,
            name,
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S")
        ])

def train_face_recognition_model():
    """Train the face recognition model"""
    try:
        # Initialize recognizer
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        
        # Path for face images
        path = 'Training_Data'
        
        # Function to get images and label data
        def get_images_and_labels(path):
            image_paths = [os.path.join(path, f) for f in os.listdir(path)]
            face_samples = []
            ids = []
            
            for image_path in image_paths:
                if image_path.endswith('.jpg') or image_path.endswith('.png'):
                    # Get the label (ID) from filename
                    filename = os.path.basename(image_path)
                    try:
                        # Expecting format: name.id.number.jpg
                        parts = filename.split('.')
                        if len(parts) >= 3:
                            label_id = int(parts[1])
                        else:
                            continue
                    except (ValueError, IndexError):
                        print(f"Skipping file with invalid format: {filename}")
                        continue
                    
                    # Load image and convert to grayscale
                    pil_image = Image.open(image_path).convert('L')  # Convert to grayscale
                    img_numpy = np.array(pil_image, 'uint8')
                    
                    face_samples.append(img_numpy)
                    ids.append(label_id)
            
            return face_samples, ids
        
        print("Training faces. It will take a few seconds. Wait ...")
        faces, ids = get_images_and_labels(path)
        
        if len(faces) == 0:
            raise Exception("No training images found. Please capture some images first.")
        
        # Train the recognizer
        recognizer.train(faces, np.array(ids))
        
        # Save the model
        assure_path_exists("TrainingImageLabel/")
        recognizer.write('TrainingImageLabel/Trainner.yml')
        
        print(f"Model trained successfully. {len(np.unique(ids))} students trained.")
        return True, f"Model trained successfully with {len(faces)} images for {len(np.unique(ids))} students."
        
    except Exception as e:
        print(f"Training error: {str(e)}")
        return False, str(e)

class CameraStream:
    def __init__(self):
        self.camera = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        # For recognition
        self.recognizer = None
        self.students_df = None
        
    def __del__(self):
        if self.camera:
            self.camera.release()
    
    def get_frame(self):
        global capture_mode, student_info, image_count, capturing
        
        ret, frame = self.camera.read()
        if not ret:
            return None
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        if capture_mode == 'enroll':
            # Enrollment mode
            cv2.putText(frame, f"Captured: {image_count}/50", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, f"Student: {student_info.get('name', '')}", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(frame, "Click 'Start Capture' to begin", (10, 90),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            if capturing and len(faces) == 1 and image_count < 50:
                # Save face image
                for (x, y, w, h) in faces:
                    face_img = gray[y:y+h, x:x+w]
                    data_folder = "Training_Data/"
                    assure_path_exists(data_folder)
                    filename = f"{data_folder}{student_info['name']}.{student_info['id']}.{image_count+1}.jpg"
                    image_count += 1
                    cv2.imwrite(filename, face_img)
                    time.sleep(0.2)  # Small delay between captures
                    
                if image_count >= 50:
                    save_student_to_csv(student_info['name'], student_info['id'])
                    capturing = False
                    # Auto-stop camera
                    global camera_active, camera
                    camera_active = False
                    if camera:
                        del camera
                        camera = None
                    
        elif capture_mode == 'recognize':
            # Recognition mode
            if self.recognizer is None:
                self.setup_recognition()
            
            if self.recognizer and self.students_df is not None:
                for (x, y, w, h) in faces:
                    roi_gray = gray[y:y+h, x:x+w]
                    serial, conf = self.recognizer.predict(roi_gray)

                    if conf < 50:
                        student_row = self.students_df[self.students_df['ID'] == serial]
                        if not student_row.empty:
                            name = student_row['Name'].iloc[0]
                            student_id = str(serial)

                            # Auto-mark attendance if not already marked today
                            date = datetime.now().strftime("%Y-%m-%d")
                            time_str = datetime.now().strftime("%H:%M:%S")
                            status_file = f"Student_Status/Status_for_{date}.csv"
                            status_image_folder = f"Status_Images/{date}/"
                            assure_path_exists(status_image_folder)

                            existing_ids = []

                            if os.path.isfile(status_file):
                                with open(status_file, 'r') as csvFile:
                                    reader = csv.reader(csvFile)
                                    for row in reader:
                                        if len(row) > 0:
                                            existing_ids.append(row[0])

                            if student_id not in existing_ids:
                                assure_path_exists("Student_Status/")
                                if not os.path.isfile(status_file):
                                    with open(status_file, 'w', newline='') as csvFile:
                                        writer = csv.writer(csvFile)
                                        writer.writerow(['Id', 'Name', 'Date', 'In Time', 'Out Time'])

                                with open(status_file, 'a', newline='') as csvFile:
                                    writer = csv.writer(csvFile)
                                    writer.writerow([student_id, name, date, time_str, ''])

                                #gray[y:y + h, x:x + w] = cropped image
                                #frame = full image
                                #gray = full gray image
                                cv2.imwrite(f"{status_image_folder}{student_id}.{name}.jpg", frame)

                                # Set recognition message
                                global recognized_student_message
                                recognized_student_message = f"{name} marked successfully!"
                            else:
                                global already_marked_message
                                already_marked_message = f"{name} already marked today!"

                            # Show recognized label
                            cv2.putText(frame, f"{name} (Conf: {conf:.1f})", 
                                        (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        else:
                            cv2.putText(frame, "Unknown", 
                                        (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    else:
                        cv2.putText(frame, "Unknown", 
                                    (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            cv2.putText(frame, "Face Recognition Active", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Encode frame as JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        if ret:
            return buffer.tobytes()
        return None
    
    def setup_recognition(self):
        """Setup face recognition"""
        try:
            if os.path.isfile("TrainingImageLabel/Trainner.yml"):
                self.recognizer = cv2.face.LBPHFaceRecognizer_create()
                self.recognizer.read("TrainingImageLabel/Trainner.yml")
                
                if os.path.isfile("Student_Details/students.csv"):
                    self.students_df = pd.read_csv("Student_Details/students.csv")
        except Exception as e:
            print(f"Error setting up recognition: {e}")

def generate_frames():
    """Generate camera frames"""
    global camera
    
    while camera_active:
        if camera is None:
            camera = CameraStream()
        
        frame = camera.get_frame()
        if frame is not None:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        else:
            break

# Initialize directories
assure_path_exists("Training_Data/")
assure_path_exists("TrainingImageLabel/")
assure_path_exists("Student_Details/")
assure_path_exists("Student_Status/")

@app.route('/')
def index():
    """Main dashboard page"""
    status = get_system_status()
    attendance = get_today_attendance()
    current_time = datetime.now().strftime('%A, %B %d, %Y at %H:%M:%S')
    
    return render_template('index.html', 
                         status=status, 
                         attendance=attendance,
                         current_time=current_time,
                         camera_active=camera_active,
                         capture_mode=capture_mode)

@app.route('/start_camera/<mode>')
def start_camera(mode):
    """Start camera for enrollment or recognition"""
    global camera_active, capture_mode, image_count, capturing
    
    if mode in ['enroll', 'recognize']:
        camera_active = True
        capture_mode = mode
        image_count = 0
        capturing = False
        flash(f'Camera started for {mode}', 'success')
    else:
        flash('Invalid camera mode', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/recognized_message')
def get_recognition_message():
    global recognized_student_message, already_marked_message

    if recognized_student_message:
        msg = recognized_student_message
        recognized_student_message = ''  # reset
        return jsonify({'message': msg, 'type': 'success'})
    
    elif already_marked_message:
        msg = already_marked_message
        already_marked_message = ''  # reset
        return jsonify({'message': msg, 'type': 'info'})

    return jsonify({'message': '', 'type': ''})

@app.route('/stop_camera')
def stop_camera():
    """Stop camera"""
    global camera_active, camera
    
    camera_active = False
    if camera:
        del camera
        camera = None
    
    flash('Camera stopped', 'info')
    return redirect(url_for('index'))

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    if camera_active:
        return Response(generate_frames(),
                       mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return "Camera not active", 404

@app.route('/enroll', methods=['POST'])
def enroll_student():
    global student_info, capture_mode, camera_active, image_count

    name = request.form.get('name', '').strip()
    student_id = request.form.get('student_id', '').strip()

    if not name or not student_id:
        flash('Please fill in all fields', 'error')
        return redirect(url_for('index'))

    # Check if student ID already exists
    if os.path.isfile("Student_Details/students.csv"):
        try:
            df = pd.read_csv("Student_Details/students.csv")
            if int(student_id) in df['ID'].values:
                flash(f'Student ID {student_id} already exists!', 'error')
                return redirect(url_for('index'))
        except:
            pass

    student_info = {'name': name, 'id': student_id}
    camera_active = True
    capture_mode = 'enroll'
    image_count = 0

    flash(f'Enrollment started for {name} (ID: {student_id})', 'success')
    return redirect(url_for('index'))

@app.route('/start_capture')
def start_capture():
    global capturing, image_count
    capturing = True
    image_count = 0
    return jsonify({'status': 'started'})

@app.route('/recognize', methods=['POST'])
def recognize_student():
    """Handle face recognition for attendance"""
    global camera_active, capture_mode
    
    if not os.path.isfile("TrainingImageLabel/Trainner.yml"):
        flash('Model not trained. Please train the model first.', 'error')
        return redirect(url_for('index'))
    
    camera_active = True
    capture_mode = 'recognize'
    
    flash('Face recognition started', 'success')
    return redirect(url_for('index'))

@app.route('/train', methods=['POST'])
def train_model():
    """Handle model training"""
    # Check if there are training images
    training_files = []
    if os.path.exists("Training_Data/"):
        training_files = [f for f in os.listdir("Training_Data/") if f.endswith(('.jpg', '.png'))]
    
    if len(training_files) < 10:
        flash('Please capture at least 10 images before training', 'warning')
        return redirect(url_for('index'))
    
    try:
        success, message = train_face_recognition_model()
        
        if success:
            flash(message, 'success')
        else:
            flash(f'Training error: {message}', 'error')
            
    except Exception as e:
        flash(f'Failed to start training: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/status')
def api_status():
    """API endpoint for system status"""
    global image_count, capturing
    
    status = get_system_status()
    attendance = get_today_attendance()
    
    return jsonify({
        'status': status,
        'attendance': attendance,
        'camera_active': camera_active,
        'capture_mode': capture_mode,
        'image_count': image_count,
        'capturing': capturing,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/attendance')
def attendance_page():
    """Attendance records page"""
    attendance = get_today_attendance()
    current_time = datetime.now().strftime('%A, %B %d, %Y at %H:%M:%S')
    
    return render_template('attendance.html', 
                         attendance=attendance,
                         current_time=current_time)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)