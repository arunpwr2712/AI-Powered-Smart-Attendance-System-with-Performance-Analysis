import cv2
import numpy as np
import face_recognition
import os
import csv

from datetime import datetime
from face_recognition_module import recognize_face
from attendance import mark_attendance
from analysis import analyze_attendance_with_astar

# Main function to run face recognition and attendance system
def main():
    video_capture = cv2.VideoCapture(0)
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        recognized_names, face_locations = recognize_face(frame)
        for name in recognized_names:
            if name != "Unknown":
                marked=mark_attendance(name)
        for (top, right, bottom, left), name in zip(face_locations, recognized_names):
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        cv2.imshow('Attendance System', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    video_capture.release()
    cv2.destroyAllWindows()
    target_percentage = 90.0  # Target attendance percentage to optimize towards
    analyze_attendance_with_astar(target_percentage)
if __name__ == "__main__":
    main()