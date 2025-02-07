import cv2
import numpy as np
import face_recognition
import os
import csv
from datetime import datetime

# Attendance marking function with 1-hour interval check (based on hour, not second)
def mark_attendance(name):
    file_path = "attendance.csv"
    now = datetime.now()
    date_string = now.strftime('%Y-%m-%d')
    current_hour = now.strftime('%H')  # Get the current hour (24-hour format)
    # Check if the file exists and read the last attendance time for the student
    last_attendance = {}
    if os.path.exists(file_path):
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                recorded_name, recorded_date, recorded_time, marked = row
                if recorded_name == name and recorded_date == date_string:
                    last_attendance[name] = recorded_time
    marked=False
    # Check if attendance was already marked within the last hour (based on hour only)
    if name in last_attendance:
        last_time = datetime.strptime(last_attendance[name], '%H:%M:%S')
        last_hour = last_time.strftime('%H')  # Get the hour part of the last recorded time
        if current_hour == last_hour:  # If the current hour is the same as the last recorded hour
            marked=True
            print(f"Attendance already marked for {name} in the current hour, next entry allowed after 1 hour.")
            return
    # If file does not exist, create it with the header
    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Date", "Time","Marked"])
    # Append new attendance record with the current time
    with open(file_path, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([name, date_string, now.strftime('%H:%M:%S'),True])
        print(f"Attendance marked for {name} at {now.strftime('%H:%M:%S')}.")
    return marked