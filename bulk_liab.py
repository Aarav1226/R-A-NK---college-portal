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

    print("\n--- Assigning Rented Books ---")
    
    # --- Assign exactly 2 books to Aarav ---
    # Give Aarav "Introduction to Algorithms" and "Python Crash Course"
    aarav_books = [b for b in available_books if "Algorithms" in b[1] or "Crash Course" in b[1]][:2]
    for bid, title in aarav_books:
        c.execute("UPDATE bks SET rent=? WHERE bid=?", (AARAV_SAP_ID, bid))
        print(f"🎒 Rented to Aarav Saxena ({AARAV_SAP_ID}): {title}")
        available_books.remove((bid, title)) # Remove from available pool
        
    # --- Assign books to a FEW random students (e.g., 6 other students) ---
    # Remove Aarav from the random selection pool
    other_students = [s for s in all_students if s[0] != AARAV_SAP_ID]
    random.shuffle(other_students)
    lucky_students = other_students[:6] # Pick 6 random students
    
    for uid, name in lucky_students:
        # Give them 1 random book
        if not available_books: break # Stop if library is empty
        
        book_to_rent = random.choice(available_books)
        bid, title = book_to_rent
        
        c.execute("UPDATE bks SET rent=? WHERE bid=?", (uid, bid))
        print(f"📘 Rented to {name} ({uid}): {title}")
        
        available_books.remove(book_to_rent) # Remove from available pool

    con.commit()

    con.commit()
    con.close()