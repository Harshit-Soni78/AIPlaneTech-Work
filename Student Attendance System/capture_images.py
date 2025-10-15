import os
import csv
import cv2
import argparse
from datetime import datetime
from PIL import Image

def assure_path_exists(path):
    """Ensure directory exists, create if it doesn't"""
    if not os.path.exists(path):
        os.makedirs(path)

def capture_student_images(student_name=None, student_id=None):
    """Capture face images for a new student"""
    data_folder = "Training_Data/"
    assure_path_exists(data_folder)
    
    # Get student information if not provided
    if student_name is None:
        student_name = input("Enter student name: ").strip()
    if student_id is None:
        student_id = input("Enter student ID: ").strip()
    
    # Initialize face detector
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return False
    
    print("\nStarting face capture...")
    print("Press 's' to start capturing")
    print("Press 'q' to quit")
    
    image_count = 0
    capturing = False
    
    while image_count < 50:
        ret, frame = cap.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        # Draw rectangle around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Display instructions
        cv2.putText(frame, f"Captured: {image_count}/50", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "'s' to start, 'q' to quit", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Student Enrollment', frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('s'):
            capturing = True
        elif key == ord('q'):
            break
            
        if capturing and len(faces) == 1:
            # Save face image
            for (x, y, w, h) in faces:
                face_img = gray[y:y+h, x:x+w]
                filename = f"{data_folder}{student_name}.{student_id}.{image_count+1}.jpg"
                cv2.imwrite(filename, face_img)
                image_count += 1
    
    cap.release()
    cv2.destroyAllWindows()
    
    if image_count >= 50:
        print("\nSuccessfully captured 50 images!")
        save_to_csv(student_name, student_id)
        return True
    else:
        print("\nCapture session ended early")
        return False

def save_to_csv(name, id):
    """Save student data to CSV file"""
    student_details = "Student_Details/"
    assure_path_exists(student_details)
    csv_file = os.path.join(student_details, "students.csv")
    
    # Check if CSV exists, if not create with header
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Enrollment Date", "Enrollment Time"])
    
    # Append new student entry
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        now = datetime.now()
        writer.writerow([
            id,
            name,
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M:%S")
        ])

def main():
    parser = argparse.ArgumentParser(description='Student Enrollment System')
    parser.add_argument('--name', help='Student name', required=False)
    parser.add_argument('--id', help='Student ID', required=False)
    args = parser.parse_args()

    if args.name and args.id:
        success = capture_student_images(args.name, args.id)
        sys.exit(0 if success else 1)
    else:
        print("=== Student Enrollment System ===")
        print("1. Enroll New Student")
        print("2. Exit")
        
        choice = input("Select option (1/2): ")
        
        if choice == '1':
            capture_student_images()
        else:
            print("Exiting program")

if __name__ == "__main__":
    import sys
    main()