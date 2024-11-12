import os
import cv2
import numpy as np
from PIL import Image

# Train Image
def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)
    faces, Ids = getImagesAndLables(trainimage_path)
    recognizer.train(faces, np.array(Ids))
    recognizer.save(trainimagelabel_path)
    res = "Image Trained successfully"
    message.configure(text=res)
    text_to_speech(res)

def getImagesAndLables(path):
    # Gather all directories in the specified path
    newdir = [os.path.join(path, d) for d in os.listdir(path)]
    
    # Get all image paths, filtering out non-image files
    imagePaths = [
        os.path.join(newdir[i], f)
        for i in range(len(newdir))
        if os.path.isdir(newdir[i])  # Ensure we're looking only at directories
        for f in os.listdir(newdir[i])
        if f.endswith(('.png', '.jpg', '.jpeg'))  # Include only image files
    ]

    faces = []
    Ids = []

    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert("L")  # Convert to grayscale
        imageNp = np.array(pilImage, "uint8")  # Convert image to numpy array

        # Extract ID assuming the filename format is 'Name_ID.extension'
        try:
            Id = int(os.path.split(imagePath)[-1].split("_")[1].split(".")[0])
            faces.append(imageNp)
            Ids.append(Id)
        except (IndexError, ValueError):
            print(f"Skipping file with invalid format: {imagePath}")

    return faces, Ids
