import sqlite3


# --- STUDENT DATA ---
# Format: (Name, SAP_ID, Batch, Password)
student_data = [
    # Previous Data
    ("Tanishq Kumar", "590021506", "A", "TA1506"),
    ("Samrata", "590021799", "A", "SA1799"),
    ("Vidhi Somraan Somraan", "590021981", "A", "VI1981"),
    ("Sakshi Dubey", "590022022", "A", "SA2022"),
    ("Arjun Bhargav", "590022275", "A", "AR2275"),
    ("Ayush Kumar Singh", "590022334", "A", "AY2334"),
    ("Aaradhya Saxena", "590022489", "A", "AA2489"),
    ("Prince Raj Rawat", "590022507", "A", "PR2507"),
    ("NISHHIKA SHARMA", "590022566", "A", "NI2566"),
    ("Prakhar Shukla", "590022600", "A", "PR2600"),
    ("Siddharth Solanki", "590022620", "A", "SI2620"),
    ("Rudraksh Sharma", "590022672", "A", "RU2672"),
    ("VANSH RATHI", "590022713", "A", "VA2713"),
    ("Jahnvi Kanyal", "590022824", "A", "JA2824"),
    ("Riddhi Saxena", "590022853", "A", "RI2853"),
    ("Pralav Goyal", "590023121", "B", "PR3121"),
    ("Anushka Singh", "590023224", "B", "AN3224"),
    ("Nandini Joshi", "590023287", "B", "NA3287"),
    ("Yashdeep Lamba", "590023466", "B", "YA3466"),
    ("Aarav Saxena", "590023538", "B", "AA3538"),
    ("Shaurya Gautam", "590023696", "B", "SH3696"),
    ("Krishna Pipraiya", "590023740", "B", "KR3740"),
    ("Atharva Maithani", "590024379", "B", "AT4379"),
    ("NIKHIL NISHANT KAMBLE", "590024383", "B", "NI4383"),
    ("HARSIMAR SINGH SALUJA", "590024470", "B", "HA4470"),
    ("Tanisha Singh", "590024674", "B", "TA4674"),
    ("Shiva Vashisth", "590025394", "B", "SH5394"),
    ("Aditya", "590025474", "B", "AD5474"),
    ("Raghav Bansal", "590026647", "B", "RA6647"),
    
    # New Data from Screenshot 2
    ("Aditya Aditya", "590021696", "C", "AD1696"),
    ("Viraj Varma", "590022322", "C", "VV2322"),
    ("DEVAM YADAV", "590022492", "C", "DE2492"),
    ("Hardik Bansal", "590022662", "C", "HA2662"),
    ("EKTA BHARDWAJ", "590022698", "C", "EK2698"),
    ("Shorya Bhardwaj", "590023597", "C", "SH3597"),
    ("Priyanshi Rana", "590024089", "C", "PR4089"),
    ("Dhruv Dhruv", "590024139", "C", "DH4139"),
    ("Yash Dhondiyal", "590024289", "C", "YA4289"),
    ("Aksh Aswal", "590024622", "C", "AK4622"),
    ("GARVIT JUNEJA", "590024669", "C", "GA4669"),
    ("Anjali Kalra", "590024902", "D", "AN4902"),
    ("Tushveen Kaur Bhatia", "590025028", "D", "TU5028"),
    ("Lovish Goyal", "590025138", "D", "LO5138"),
    ("Jiya Singh", "590025179", "D", "JI5179"),
    ("Ankit Sah", "590025270", "D", "AN5270"),
    ("Nikhil Pant", "590025383", "D", "NI5383"),
    ("Vedans Rawat", "590025450", "D", "VE5450"),
    ("Devyansh Deopa", "590025479", "D", "DE5479"),
    ("Bhoovi Verma", "590025848", "D", "BH5848"),
    ("Krish Gupta", "590025919", "D", "KR5919"),
    ("Atulya Singh", "590025932", "D", "AT5932"),
    ("Divyanshu Raman Pandey", "590026079", "D", "DI6079"),
    ("Sahaj Parikh", "590026086", "D", "SA6086"),
    ("Vibha Dubey", "590026089", "D", "VI6089"),
    ("SAYRA SOOD", "590026248", "D", "SA6248"),
    ("Apoorv Mishra", "590026560", "D", "AP6560"),
    ("Aakashi jain", "590026568", "D", "AA6568")
]

# --- TEACHER DATA ---
# Format: (Name, SAP_ID, Subject, Password)
teacher_data = [
    ("Nelson", "1000", "DSA", "NE1000"),
    ("Prasanthi", "1001", "Python", "PR1001"),
    ("Goutam", "1002", "Elements of AI/ML", "GO1002"),
    ("Manju", "1003", "Digital Electronics", "MA1003"),
    ("Taruni", "1004", "Time & Priority Management", "TA1004"),
    ("Aarav", "1005", "EVS", "AA1005"),
    ("Debashish", "1006", "Maths", "DE1006")
]

def init_db(c):
    # Ensure all tables exist before trying to upload data
    c.execute('''CREATE TABLE IF NOT EXISTS usr (uid TEXT PRIMARY KEY, psw TEXT, role TEXT, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS stu (uid TEXT PRIMARY KEY, bat TEXT, sem INTEGER, att INTEGER, fee INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tch (uid TEXT PRIMARY KEY, bat TEXT, sub TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bks (bid INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, rent TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS mrk (uid TEXT, sem INTEGER, sub TEXT, mrk INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ttb (id INTEGER PRIMARY KEY AUTOINCREMENT, bat TEXT, day TEXT, tim TEXT, sub TEXT, rm TEXT, tid TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS att_data (uid TEXT, sub TEXT, attended INTEGER, total INTEGER, UNIQUE(uid, sub))''')
    c.execute('''CREATE TABLE IF NOT EXISTS class_conducted (ttb_id INTEGER, dt TEXT, UNIQUE(ttb_id, dt))''')

def bulk_upload():
    con = sqlite3.connect("col.db")
    c = con.cursor()
    
    # Initialize the database schema first!
    init_db(c)
    
    s_success = 0
    t_success = 0
    skip_count = 0
    
    print("--- Uploading Students ---")
    for name, sap_id, batch, psw in student_data:
        try:
            # Insert into the Users table (role: stu)
            c.execute("INSERT INTO usr VALUES (?, ?, 'stu', ?)", (sap_id, psw, name))
            # Insert into the Students table
            c.execute("INSERT INTO stu VALUES (?, ?, 1, 0, 0)", (sap_id, batch))
            s_success += 1
            print(f"✅ Student added: {name} ({sap_id})")
        except sqlite3.IntegrityError:
            skip_count += 1
            print(f"⚠️ Skipped: {name} ({sap_id}) - ID already exists!")


    con.commit()
    con.close()