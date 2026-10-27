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

]