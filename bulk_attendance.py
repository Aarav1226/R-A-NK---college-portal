import sqlite3
import random

# Predefined list of Subjects matching your portal
SUBJECTS = [
    "DSA", 
    "Python", 
    "Maths", 
    "Time & Priority Management", 
    "EVS", 
    "Digital Electronics", 
    "Elements of AI/ML"
]

# Aarav's specific SAP ID
AARAV_SAP_ID = "590023538"

# FIXED Total classes conducted for EVERY student
TOTAL_CLASSES = {
    "DSA": 53,
    "Python": 40,
    "Digital Electronics": 31,
    "Time & Priority Management": 3,
    "EVS": 7,
    "Maths": 45,             # Realistic mock data
    "Elements of AI/ML": 30  # Realistic mock data
}

# Exact attended classes transcribed from Aarav's screenshot
AARAV_ATTENDED = {
    "DSA": 39,
    "Python": 29,
    "Digital Electronics": 24,
    "Time & Priority Management": 3,
    "EVS": 7,
    "Maths": 42,             
    "Elements of AI/ML": 26  
}

def upload_attendance():
    con = sqlite3.connect("col.db")
    c = con.cursor()
    
    # Ensure the attendance table exists
    c.execute('''CREATE TABLE IF NOT EXISTS att_data (uid TEXT, sub TEXT, attended INTEGER, total INTEGER, UNIQUE(uid, sub))''')
    
    # Clear existing attendance data to prevent duplicates
    c.execute("DELETE FROM att_data")
    print("🧹 Cleared old subject-wise attendance data.")
    
    # Fetch all students from the database
    c.execute("SELECT uid FROM stu")
    students = c.fetchall()
    
    if not students:
        print("❌ No students found in the database! Please run bulk_upload.py first.")
        con.close()
        return

    total_records_added = 0
    
    print("\n--- Generating & Uploading Attendance ---")
    for (uid,) in students:
        overall_attended = 0 # To track total attended days for the dashboard
        
        for sub in SUBJECTS:
            # Everyone gets the exact same total conducted classes
            total = TOTAL_CLASSES[sub]
            
            # If Aarav, use his exact attended count
            if uid == AARAV_SAP_ID:
                attended = AARAV_ATTENDED[sub]
            else:
                # Generate a random attendance count for others (between 40% and 100%)
                attended = random.randint(int(total * 0.4), total)
            
            # Insert into subject-wise attendance table
            c.execute("INSERT INTO att_data (uid, sub, attended, total) VALUES (?, ?, ?, ?)", (uid, sub, attended, total))
            overall_attended += attended
            total_records_added += 1
            

    con.commit()
    con.close()