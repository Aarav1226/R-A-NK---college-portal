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

    # --- TUESDAY ---
    ("Tue", "08:00 AM - 08:55 AM", "Maths", "3001", "1006"),
    ("Tue", "09:00 AM - 09:55 AM", "Elements of AI/ML", "1202", "1002"),
    ("Tue", "10:00 AM - 10:55 AM", "DSA", "9205", "1000"),
    ("Tue", "12:00 PM - 12:55 PM", "Python", "1203", "1001"),
    ("Tue", "01:00 PM - 01:55 PM", "DSA", "1203", "1000"),
    ("Tue", "03:00 PM - 03:55 PM", "Digital Electronics", "7103", "1003"),

    # --- WEDNESDAY ---
    ("Wed", "08:00 AM - 09:55 AM", "Python", "AB-11 L-007", "1001"),
    ("Wed", "10:00 AM - 10:55 AM", "Maths", "5201", "1006"),
    ("Wed", "12:00 PM - 12:55 PM", "DSA", "1203", "1000"),
    ("Wed", "01:00 PM - 01:55 PM", "Digital Electronics", "3105", "1003"),
    ("Wed", "03:00 PM - 03:55 PM", "EVS", "MS Teams", "1005"),

    # --- THURSDAY ---
    ("Thu", "08:00 AM - 08:55 AM", "Digital Electronics", "3103", "1003"),
    ("Thu", "09:00 AM - 09:55 AM", "DSA", "1203", "1000"),
    ("Thu", "12:00 PM - 01:55 PM", "Elements of AI/ML", "AB-11 L-003", "1002"),

    # --- FRIDAY ---
    ("Fri", "08:00 AM - 08:55 AM", "Maths", "3101", "1006"),
    ("Fri", "09:00 AM - 09:55 AM", "DSA", "3001", "1000"),
    ("Fri", "10:00 AM - 10:55 AM", "Digital Electronics", "2004", "1003"),
    ("Fri", "12:00 PM - 01:55 PM", "Python", "AB-11 L-003", "1001")
]
