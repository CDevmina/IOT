import cv2
import numpy as np
from ultralytics import YOLO
from sort.sort import *
from util import get_car, read_license_plate

mot_tracker = Sort()

# Load models
coco_model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('./models/license_plate_detector.pt')

vehicles = [2, 3, 5, 7]

# You can change the path to an image or a video file
input_path = 'testdata/9.jpg'  # Change this to the path of your image or video file

# Check if the input is an image or a video
is_video = input_path.endswith('.mp4') or input_path.endswith('.avi') or input_path.endswith('.mov')
cap = cv2.VideoCapture(input_path) if is_video else None

while True:
    # Read frames from the input (image or video)
    ret, frame = cap.read() if is_video else (True, cv2.imread(input_path))

    if not ret:
        break

    # Detect vehicles
    detections = coco_model(frame)[0]
    detections_ = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        # Filter vehicles based on class_id
        if int(class_id) in vehicles:
            detections_.append([x1, y1, x2, y2, score, int(class_id)])

    # Track vehicles
    track_ids = mot_tracker.update(np.asarray(detections_))

    # Detect license plates
    license_plates = license_plate_detector(frame)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate

        # Assign license plate to car
        xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

        if car_id != -1:
            # Draw bounding boxes on the frame for vehicles
            cv2.rectangle(frame, (int(xcar1), int(ycar1)), (int(xcar2), int(ycar2)), (0, 255, 0), 2)

            # Draw bounding boxes on the frame for license plates
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

            # Crop license plate
            license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

            # Process license plate
            license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
            _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)

            # Read license plate number
            license_plate_text, _ = read_license_plate(license_plate_crop_thresh)

            if license_plate_text is not None:
                # Display license string above the box with larger font and thicker text
                text_position = (int((x1 + x2) / 2), int(y1) - 10)
                cv2.putText(frame, f'License Plate: {license_plate_text} - Vehicle Type: {class_id}',
                            text_position, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 3)  # Increased size and thickness

    # Display the frame
    frame = cv2.resize(frame, (1280, 720))
    cv2.imshow('Frame', frame)

    # Break the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture
if is_video:
    cap.release()

# Close all OpenCV windows
cv2.destroyAllWindows()
