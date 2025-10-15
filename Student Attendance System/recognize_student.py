import os
import csv
import cv2
import numpy as np
import pandas as pd
import argparse
from datetime import datetime
import sys

def assure_path_exists(path):
    """Ensure directory exists, create if it doesn't"""
    if not os.path.exists(path):
        os.makedirs(path)

def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if not exists:
        print('Haarcascade file missing. Please contact us for help')
        return False
    return True

def mark_status():
    """Mark Status using face recognition"""
    if not check_haarcascadefile():
        return False

    assure_path_exists("Student_Status/")
    assure_path_exists("Student_Details/")
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    if not os.path.isfile("TrainingImageLabel/Trainner.yml"):
        print("Model Missing...")
        return False
    
    recognizer.read("TrainingImageLabel/Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    if not os.path.isfile("Student_Details/students.csv"):
        print("Students details are missing, please check!")
        return False
    
    df = pd.read_csv("Student_Details/students.csv")
    
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")
    
    status_file = f"Student_Status/Status_for_{date}.csv"
    col_names = ['Id', 'Name', 'Date', 'In Time', 'Out Time']
    
    in_students = []
    if os.path.isfile(status_file):
        with open(status_file, 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for lines in reader1:
                if len(lines) > 0:
                    in_students.append(lines[0])
    else:
        with open(status_file, 'a+', newline='') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)
    
    status_image_folder = f"Status_Images/{date}/"
    assure_path_exists(status_image_folder)
    
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera")
        return False
    
    print("Camera Loaded Successfully... Press 'q' or 'Esc' to exit.")
    
    while True:  
        ret, im = cam.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)  
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)  
        
        for (x, y, w, h) in faces:  
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)  
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])  
            
            if conf < 50:  
                try:
                    aa = df.loc[df['ID'] == serial]['Name'].values
                    ID = df.loc[df['ID'] == serial]['ID'].values 
                    ID = str(ID[0])
                    name = str(aa[0])
                    
                    status_row = [str(ID), name, date, time]  
                    
                    if ID not in in_students:
                        in_students.append(ID)
                        with open(status_file, 'a', newline='') as csvFile1:
                            writer = csv.writer(csvFile1)
                            writer.writerow(status_row)
                        
                        # Save the status image
                        cv2.imwrite(f"{status_image_folder}{ID}.{name}.jpg", gray[y:y + h, x:x + w])
                        ##print(f'Status marked for {ID}.{name}')
                        cam.release()
                        cv2.destroyAllWindows()
                        return True
                    else:
                        print(f'Status for {name} (ID: {ID}) already marked today')
                        cam.release()
                        cv2.destroyAllWindows()
                        return 2
                        
                except Exception as e:
                    print(f"Error processing recognition: {str(e)}")
                    continue
                    
            else:
                name = 'Unknown'
                
            cv2.putText(im, str(name), (x, y + h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Capturing Status', im)
        
        if cv2.waitKey(1) in [ord('q'), 27]:  # 27 is ESC key
            break

    cam.release()
    cv2.destroyAllWindows()
    return False

def main():
    parser = argparse.ArgumentParser(description='Mark Student Status')
    args = parser.parse_args()

    print("=== Starting Status Marking marking ===")
    success = mark_status()
    
    if success == True:
        print("Status marked successfully!")
        sys.exit(0)
    elif success == 2:
        print("Status Already marked successfully!")
        sys.exit(2)
    else:
        print("Status marking failed or already marked!")
        sys.exit(1)

if __name__ == "__main__":
    main()