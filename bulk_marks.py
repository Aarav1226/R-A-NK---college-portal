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


# Aarav's specific SAP ID based on your previous data
AARAV_SAP_ID = "590023538"
AARAV_FIXED_SCORE = 92

def upload_marks():
    con = sqlite3.connect("col.db")
    c = con.cursor()
    
    # Ensure the marks table exists
    c.execute('''CREATE TABLE IF NOT EXISTS mrk (uid TEXT, sem INTEGER, sub TEXT, mrk INTEGER)''')
    
    # Clear existing marks for Sem 1 and Sem 2 to prevent duplicates if run multiple times
    c.execute("DELETE FROM mrk WHERE sem IN (1, 2)")
    print("🧹 Cleared old marks data for Semesters 1 and 2.")
    
    # Fetch all students from the database
    c.execute("SELECT uid FROM stu")
    students = c.fetchall()
    
    if not students:
        print("❌ No students found in the database! Please run bulk_upload.py first.")
        con.close()
        return


    con.close()