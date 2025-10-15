import os
import cv2
import numpy as np
import argparse
from PIL import Image
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

def getImagesAndLabels(path):
    """Get training images and labels"""
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]
    faces = []
    Ids = []
    
    for imagePath in imagePaths:
        try:
            pilImage = Image.open(imagePath).convert('L')
            imageNp = np.array(pilImage, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split(".")[1])
            faces.append(imageNp)
            Ids.append(ID)
        except Exception as e:
            print(f"Error processing {imagePath}: {str(e)}")
            continue
            
    return faces, Ids

def train_model():
    """Train the face recognition model"""
    if not check_haarcascadefile():
        return False

    assure_path_exists("TrainingImageLabel/")
    
    try:
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        
        print("Getting training data...")
        faces, Ids = getImagesAndLabels("Training_Data")
        
        if len(faces) == 0:
            print("No training data found!")
            return False
            
        print("Training model...")
        recognizer.train(faces, np.array(Ids))
        recognizer.save("TrainingImageLabel/Trainner.yml")
        
        print(f"Trained {len(faces)} images for {len(set(Ids))} students")
        return True
        
    except Exception as e:
        print(f'Error during training: {str(e)}')
        return False

def main():
    parser = argparse.ArgumentParser(description='Train Face Recognition Model')
    args = parser.parse_args()

    print("=== Starting model training ===")
    success = train_model()
    
    if success:
        print("Training completed successfully!")
        sys.exit(0)
    else:
        print("Training failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()