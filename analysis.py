import csv
import os
from datetime import datetime
import math

class StudentAttendance:
    def __init__(self, name, missed_days, total_days):
        self.name = name
        self.missed_days = missed_days
        self.total_days = total_days
        self.attendance_percentage = (total_days - missed_days) / total_days * 100
    def heuristic(self, target_percentage):
        return abs(self.attendance_percentage - target_percentage)
# Attendance analysis function with custom A* approach
def analyze_attendance_with_astar(TARGET_PERCENTAGE=90.0):
    file_path = "attendance.csv"
    attendance_data = {}
    total_days = set()
    # Read the attendance data
    if os.path.exists(file_path):
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header
            for row in reader:
                name, date, _ ,_= row
                total_days.add(date)
                if name not in attendance_data:
                    attendance_data[name] = set()
                attendance_data[name].add(date)
    total_days_count = len(total_days)
    report = {}
    for name, dates in attendance_data.items():
        attended_days = len(dates)
        attendance_percentage = (attended_days / total_days_count * 100) if total_days_count > 0 else 0
        heuristic = TARGET_PERCENTAGE - attendance_percentage  # How much improvement is needed
        # Calculate additional days needed to reach target
        if attendance_percentage < TARGET_PERCENTAGE:
            required_days = math.ceil((TARGET_PERCENTAGE * total_days_count / 100) - attended_days)
        else:
            required_days = 0  # Already meeting or exceeding target
        report[name] = {
            "Attendance Percentage": round(attendance_percentage, 2),
            "Improvement Needed (%)": round(heuristic, 2) if heuristic > 0 else 0,
            "Days Needed to Reach Target": required_days
        }
    # Print report
    print("Attendance Report:")
    for name, data in report.items():
        print(f"{name}: {data['Attendance Percentage']}% attendance, "
              f"Improvement Needed: {data['Improvement Needed (%)']}%, "
              f"Days Needed: {data['Days Needed to Reach Target']}")
    # Write the report to a new CSV file
    report_file_path = "attendance_report.csv"
    with open(report_file_path, mode='w', newline='') as report_file:
        writer = csv.writer(report_file)
        writer.writerow(["Name", "Attendance Percentage", "Improvement Needed (%)", "Days Needed to Reach Target"])
        for name, data in report.items():
            writer.writerow([name, data["Attendance Percentage"], data["Improvement Needed (%)"], data["Days Needed to Reach Target"]])
    return report