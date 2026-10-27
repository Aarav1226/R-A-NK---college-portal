import sqlite3

# --- FEE STRUCTURE DATA ---
# Transcribed exactly from your provided screenshot
# Format: Semester -> Total Amount (Semester Fee + Other Fees)
SEMESTER_FEES = {
    1: 277600,
    2: 243600,
    3: 258100,
    4: 257600,
    5: 302600,
    6: 272600,
    7: 301600,
    8: 288100
}

def apply_bulk_fees():
    con = sqlite3.connect("col.db")
    c = con.cursor()
    
    # Ensure the stu table exists
    c.execute('''CREATE TABLE IF NOT EXISTS stu (uid TEXT PRIMARY KEY, bat TEXT, sem INTEGER, att INTEGER, fee INTEGER)''')
    
    print("\n--- Applying Semester-wise Fees ---")
    
    total_students_updated = 0
    
    # Apply the specific fee to all students based on their current semester
    for sem, fee_amount in SEMESTER_FEES.items():
        # Find how many students are in this semester
        c.execute("SELECT COUNT(*) FROM stu WHERE sem=?", (sem,))
        student_count = c.fetchone()[0]
        
        if student_count > 0:
            # Overwrite the fee due with the exact semester fee from the table
            c.execute("UPDATE stu SET fee=? WHERE sem=?", (fee_amount, sem))
            total_students_updated += student_count
            print(f"✅ Semester {sem}: Applied Rs. {fee_amount:,} to {student_count} student(s).")
        else:
            print(f"ℹ️ Semester {sem}: No students currently in this semester. (Fee: Rs. {fee_amount:,} saved for future)")

    # Save changes and close
    con.commit()
    con.close()
    

    con.commit()
    con.close()