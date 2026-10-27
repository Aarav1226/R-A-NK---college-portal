import sqlite3

# --- TIMETABLE DATA TRANSCRIBED FROM IMAGES ---
# Format: (Day, Time, Subject, Room, Teacher_SAP_ID)
# Note: Subjects map to the predefined SUBJECTS list in your portal
# Teacher IDs match what was created in bulk_upload.py


# Timetable for Batches A & B
timetable_data_ab = [
    # --- MONDAY ---
    ("Mon", "08:00 AM - 09:55 AM", "DSA", "AB-11 L-007", "1000"),
    ("Mon", "10:00 AM - 10:55 AM", "Elements of AI/ML", "1201", "1002"),
    ("Mon", "12:00 PM - 12:55 PM", "Python", "3003", "1001"),
    ("Mon", "02:00 PM - 02:55 PM", "Maths", "3003", "1006"),
    ("Mon", "03:00 PM - 03:55 PM", "Elements of AI/ML", "5001", "1002"),


]