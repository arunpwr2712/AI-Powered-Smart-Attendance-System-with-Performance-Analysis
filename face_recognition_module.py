import cv2
import numpy as np
import face_recognition
import os
import csv
from datetime import datetime

# Load known faces
known_faces = []
known_names = []
# Path to known images
KNOWN_FACES_DIR = "Students"
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)
for filename in os.listdir(KNOWN_FACES_DIR):
    image = face_recognition.load_image_file(os.path.join(KNOWN_FACES_DIR, filename))
    encoding = face_recognition.face_encodings(image)[0]
    known_faces.append(encoding)
    known_names.append(os.path.splitext(filename)[0])
def recognize_face(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    recognized_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_faces, face_encoding)
        name = "Unknown"
        if True in matches:
            match_index = matches.index(True)
            name = known_names[match_index]
        recognized_names.append(name)
    return recognized_names, face_locations