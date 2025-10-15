import cv2
from ultralytics import YOLO
import os
# import torch

# model = YOLO("Models\\yolov8s.pt")  # Load YOLOv8 model


model = YOLO("Models\\yolo12n.pt")  # Load YOLOv8 model

current_person_ids = [] # Stores IDs of currently detected persons

def process_video(input_video_path, output_folder="output"):
    global current_person_ids

    if not os.path.exists(input_video_path):
        print(f"Error: Input video not found at {input_video_path}")
        return

    cap = cv2.VideoCapture(input_video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {input_video_path}")
        return

    # Get video properties for VideoWriter
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    output_video_name = os.path.join(output_folder, f"processed_{os.path.basename(input_video_path)}")
    
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # or 'XVID'
    out = cv2.VideoWriter(output_video_name, fourcc, fps, (frame_width, frame_height))

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
        
        # Write the frame to the output video
        out.write(annotated_frame)

        # If you still want to display it (optional)
        cv2.imshow("Processed Video", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'q' to quit display
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Processed video saved to: {output_video_name}")

if __name__ == '__main__':
    # Replace "your_stock_video.mp4" with the actual path to your video file
    for video_file in os.listdir("Input"):
        if video_file.endswith(('.mp4', '.avi', '.mov')):
            input_video_path = os.path.join("Input", video_file)
            print(f"Processing video: {input_video_path}")
            process_video(input_video_path, output_folder="output_videos")