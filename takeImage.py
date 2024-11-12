import os
import cv2
import numpy as np
from PIL import Image
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('attendance_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('TakeImage')

def validate_input(enrollment, name):
    """
    Validate user input for enrollment and name
    Returns tuple of (is_valid, error_message)
    """
    if not enrollment:
        return False, "Enrollment number cannot be empty"
    if not name:
        return False, "Name cannot be empty"
    if not enrollment.isdigit():
        return False, "Enrollment must be numeric"
    if len(enrollment) < 3:
        return False, "Enrollment number too short"
    if not name.replace(" ", "").isalpha():
        return False, "Name should only contain letters"
    return True, ""

def TakeImage(enrollment, name, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    """
    Capture and save student images for face recognition training
    
    Parameters:
    enrollment (str): Student enrollment number
    name (str): Student name
    haarcasecade_path (str): Path to haar cascade classifier
    trainimage_path (str): Directory to save training images
    message (tk.Label): GUI label for showing messages
    err_screen: Function to show error screen
    text_to_speech: Function for voice feedback
    """
    try:
        # Validate inputs
        is_valid, error_message = validate_input(enrollment, name)
        if not is_valid:
            message.configure(text=error_message)
            text_to_speech(error_message)
            return False

        # Check if haar cascade file exists
        if not os.path.exists(haarcasecade_path):
            raise FileNotFoundError(f"Haar cascade file not found at {haarcasecade_path}")

        # Initialize face detector
        detector = cv2.CascadeClassifier(haarcasecade_path)
        if detector.empty():
            raise Exception("Failed to load face detector")

        # Initialize camera
        cam = cv2.VideoCapture(0)
        if not cam.isOpened():
            raise Exception("Could not open camera")

        # Create directory for student
        student_path = os.path.join(trainimage_path, f"student_{enrollment}")
        os.makedirs(student_path, exist_ok=True)

        # Update GUI
        message.configure(text="Starting camera... Look at the camera")
        text_to_speech("Please look at the camera")

        # Initialize counters
        img_counter = 0
        image_count = 0
        max_images = 50  # Number of images to capture
        timeout = time.time() + 30  # 30 seconds timeout

        while True:
            ret, frame = cam.read()
            if not ret:
                raise Exception("Failed to grab frame from camera")

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                image_count += 1
                
                # Save the captured face
                if image_count % 2 == 0:  # Save every second detection
                    img_name = os.path.join(student_path, f"{name}_{enrollment}_{img_counter}.jpg")
                    cv2.imwrite(img_name, gray[y:y+h, x:x+w])
                    img_counter += 1
                    
                    # Update progress
                    progress_msg = f"Images Captured: {img_counter}/{max_images}"
                    message.configure(text=progress_msg)
                    
                    if img_counter >= max_images:
                        break

            cv2.imshow("Taking Images", frame)
            
            # Check for timeout or completion
            if time.time() > timeout or img_counter >= max_images:
                break
                
            # Check for escape key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Cleanup
        cam.release()
        cv2.destroyAllWindows()

        # Check if enough images were captured
        if img_counter < max_images:
            raise Exception(f"Only captured {img_counter} images. Please try again with better lighting and face positioning.")

        # Update student details
        update_student_details(enrollment, name)
        
        # Success message
        success_msg = f"Images captured successfully! {img_counter} images saved."
        message.configure(text=success_msg)
        text_to_speech(success_msg)
        logger.info(success_msg)
        
        return True

    except Exception as e:
        error_msg = f"Error during image capture: {str(e)}"
        logger.error(error_msg)
        message.configure(text=error_msg)
        text_to_speech(error_msg)
        
        # Cleanup on error
        if 'cam' in locals() and cam.isOpened():
            cam.release()
        cv2.destroyAllWindows()
        return False

def update_student_details(enrollment, name):
    """Update student details in CSV file"""
    import csv
    
    csv_path = "StudentDetails/studentdetails.csv"
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    
    # Check if student already exists
    exists = False
    if os.path.exists(csv_path):
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == enrollment:
                    exists = True
                    break
    
    # Add student if not exists
    if not exists:
        with open(csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            if file.tell() == 0:  # File is empty
                writer.writerow(["Enrollment", "Name"])
            writer.writerow([enrollment, name])
            logger.info(f"Added student details: {enrollment}, {name}")