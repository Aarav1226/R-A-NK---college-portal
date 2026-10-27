import sqlite3
import random

# Realistic college textbooks matching your subjects
NEW_BOOKS = [
    "Introduction to Algorithms - Thomas H. Cormen",
    "Data Structures and Algorithms in Python - Goodrich",
    "Python Crash Course, 3rd Edition - Eric Matthes",
    "Fluent Python - Luciano Ramalho",
    "Artificial Intelligence: A Modern Approach - Russell",
    "Hands-On Machine Learning - Aurélien Géron",
    "Digital Design - M. Morris Mano",
    "Advanced Engineering Mathematics - Erwin Kreyszig",
    "Higher Engineering Mathematics - B.S. Grewal",
    "Environmental Studies - Erach Bharucha",
    "Time Management from the Inside Out - Julie Morgenstern",
    "The Pragmatic Programmer - David Thomas",
    "Deep Learning with Python - François Chollet",
    "Fundamentals of Digital Logic - Brown & Vranesic",
    "Grokking Algorithms - Aditya Bhargava"
]

AARAV_SAP_ID = "590023538"


def setup_library():
    con = sqlite3.connect("col.db")
    c = con.cursor()
    
    # Ensure table exists
    c.execute('''CREATE TABLE IF NOT EXISTS bks (bid INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, rent TEXT)''')
    
    # 1. Clear old books and reset the ID counter back to 1
    c.execute("DELETE FROM bks")
    c.execute("DELETE FROM sqlite_sequence WHERE name='bks'")
    
    # 2. Add the new books (initially available, rent = '')
    print("--- Stocking the Library ---")
    for title in NEW_BOOKS:
        c.execute("INSERT INTO bks (title, rent) VALUES (?, '')", (title,))
        print(f"📚 Added: {title}")
        
    con.commit()
    
    # 3. Fetch all available books with their new IDs
    c.execute("SELECT bid, title FROM bks")
    available_books = c.fetchall() # List of (bid, title)
    
    # 4. Fetch all students
    c.execute("SELECT uid, name FROM usr WHERE role='stu'")
    all_students = c.fetchall()
    
    if not all_students:
        print("❌ No students found! Run bulk_upload.py first.")
        con.close()
        return

