import numpy as np
from ultralytics import YOLO
import cv2
from Backend_Model.util import read_license_plate
from DB_Scripts.Database_Vehicle import exit_app
from LicensePlateError import get_license_plate_manually

# load models
coco_model = YOLO('../models/yolov8n.pt')
license_plate_detector = YOLO('../models/license_plate_detector.pt')

vehicles = {2: 'car', 3: 'bus', 5: 'truck', 7: 'van'}


def process_image(image_path):
    frame = cv2.imread(image_path)
    cvframe, plate = process_frame(frame)
    return cvframe, plate


def process_frame(frame):
    detections = coco_model(frame)[0]
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) in vehicles.keys():

            # vehicle bounding box
            cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            vehicle_type = vehicles.get(int(class_id), 'unknown')
            cv2.putText(frame, f"Vehicle Type: {vehicle_type}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)

            license_plates = license_plate_detector(frame)[0]
            print(f"Detected {len(license_plates.boxes.data.tolist())} license plates.")

            for license_plate in license_plates.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = license_plate
                license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]

                # Convert to grayscale
                license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)

                # Resize image
                license_plate_crop_gray = cv2.resize(license_plate_crop_gray, None, fx=1.5, fy=1.5,
                                                     interpolation=cv2.INTER_CUBIC)

                # Reduce noise
                license_plate_crop_gray = cv2.medianBlur(license_plate_crop_gray, 3)

                # Binarization
                _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 0, 255,
                                                             cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                # Dilation and Erosion
                kernel = np.ones((1, 1), np.uint8)
                license_plate_crop_thresh = cv2.dilate(license_plate_crop_thresh, kernel, iterations=1)
                license_plate_crop_thresh = cv2.erode(license_plate_crop_thresh, kernel, iterations=1)

                # Apply morphological operations
                license_plate_crop_thresh = cv2.morphologyEx(license_plate_crop_thresh, cv2.MORPH_OPEN, kernel)
                license_plate_crop_thresh = cv2.morphologyEx(license_plate_crop_thresh, cv2.MORPH_CLOSE, kernel)

                license_plate_text = read_license_plate(license_plate_crop_thresh)

                # Plate not detected
                if license_plate_text == (None, None):
                    print("License plate not detected please enter manually!!!")
                    # Prompt the user to enter a license plate manually
                    license_plate_text = get_license_plate_manually()

                # license plate text and confidence score
                print(f"License Plate: {license_plate_text}, Confidence: {score}")

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.putText(frame, f"License Plate: {license_plate_text}", (int(x1), int(y1) - 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)

                licenseplate_score = round(score * 100, 2)
                cv2.putText(frame, f"Confidence: {licenseplate_score}%", (int(x1), int(y1) - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (36, 255, 12), 2)

                if license_plate_text is not None:
                    # Select vehicle from database
                    vehicle = exit_app(license_plate_text)
                    if vehicle is not None:
                        print(vehicle)
                    else:
                        print("Vehicle does not exist in the database.")

                return frame, license_plate_text

    return frame, None
