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

# Timetable for Batches C & D
timetable_data_cd = [
    # --- MONDAY ---
    ("Mon", "08:00 AM - 09:55 AM", "Python", "AB-11 L-004", "1001"),
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
    ("Wed", "08:00 AM - 09:55 AM", "Elements of AI/ML", "AB-11 L-004", "1002"),
    ("Wed", "12:00 PM - 12:55 PM", "DSA", "1203", "1000"),
    ("Wed", "01:00 PM - 01:55 PM", "Digital Electronics", "3105", "1003"),
    ("Wed", "03:00 PM - 03:55 PM", "EVS", "MS Teams", "1005"),

    # --- THURSDAY ---
    ("Thu", "08:00 AM - 08:55 AM", "Digital Electronics", "3103", "1003"),
    ("Thu", "09:00 AM - 09:55 AM", "DSA", "1203", "1000"),
    ("Thu", "12:00 PM - 01:55 PM", "Python", "AB-11 L-010", "1001"),

    # --- FRIDAY ---
    ("Fri", "08:00 AM - 08:55 AM", "Maths", "3101", "1006"),
    ("Fri", "09:00 AM - 09:55 AM", "DSA", "3001", "1000"),
    ("Fri", "10:00 AM - 10:55 AM", "Digital Electronics", "2004", "1003"),
    ("Fri", "12:00 PM - 01:55 PM", "DSA", "AB-11 L-010", "1000"),
    ("Fri", "03:00 PM - 03:55 PM", "Maths", "5203", "1006")
]

def upload_timetable():
    # Connect to your existing database
    con = sqlite3.connect("col.db")
    c = con.cursor()
    
    # Ensure the ttb table exists just in case
    c.execute('''CREATE TABLE IF NOT EXISTS ttb (id INTEGER PRIMARY KEY AUTOINCREMENT, bat TEXT, day TEXT, tim TEXT, sub TEXT, rm TEXT, tid TEXT)''')
    
    # Clear existing timetables for all specified batches to prevent duplicates
    c.execute("DELETE FROM ttb WHERE bat IN ('A', 'B', 'C', 'D')")
    print("🧹 Cleared old timetable data for Batches A, B, C, & D.")
    
    # Mapping batches to their respective data sets
    batch_map = [
        ("A", timetable_data_ab),
        ("B", timetable_data_ab),
        ("C", timetable_data_cd),
        ("D", timetable_data_cd)
    ]
    
    total_added = 0
    
    print("\n--- Uploading Timetables ---")
    for batch, data_set in batch_map:
        print(f"\nProcessing Batch {batch}...")
        for day, tim, sub, rm, tid in data_set:
            try:
                c.execute("INSERT INTO ttb (bat, day, tim, sub, rm, tid) VALUES (?, ?, ?, ?, ?, ?)", 
                          (batch, day, tim, sub, rm, tid))
                total_added += 1
                print(f"✅ Added: {day} | {tim} | {sub} | Room {rm}")
            except sqlite3.Error as e:
                print(f"⚠️ Failed to add {sub} on {day}: {e}")

    # Save changes and close
    con.commit()
    con.close()
    
    print("-" * 30)
    print("Bulk Timetable Upload Complete!")
    print(f"Total sessions added across all batches: {total_added}")

if __name__ == "__main__":
    upload_timetable()