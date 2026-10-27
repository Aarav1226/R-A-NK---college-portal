import streamlit as st
import sqlite3
import pandas as pd
from datetime import date

# --- CONFIGURATION ---
st.set_page_config(page_title="R(A)NK University Portal", page_icon="🎓", layout="wide")

SUBJECTS = [
    "DSA", "Python", "Maths", "Time & Priority Management", 
    "EVS", "Digital Electronics", "Elements of AI/ML"
]

SEMESTER_FEES = {
    1: 277600, 2: 243600, 3: 258100, 4: 257600,
    5: 302600, 6: 272600, 7: 301600, 8: 288100
}

# Mapping to sort days chronologically instead of alphabetically
DAY_ORDER_MAP = {"Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6, "Sun": 7}
DAYS_ORDER_LIST = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# --- DATABASE HELPER ---
def init_db():
    # CRUD: CREATE tables if they don't already exist
    con = sqlite3.connect("col.db")
    c = con.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usr (uid TEXT PRIMARY KEY, psw TEXT, role TEXT, name TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS stu (uid TEXT PRIMARY KEY, bat TEXT, sem INTEGER, att INTEGER, fee INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS tch (uid TEXT PRIMARY KEY, bat TEXT, sub TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS bks (bid INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, rent TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS mrk (uid TEXT, sem INTEGER, sub TEXT, mrk INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ttb (id INTEGER PRIMARY KEY AUTOINCREMENT, bat TEXT, day TEXT, tim TEXT, sub TEXT, rm TEXT, tid TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS att_data (uid TEXT, sub TEXT, attended INTEGER, total INTEGER, UNIQUE(uid, sub))''')
    c.execute('''CREATE TABLE IF NOT EXISTS class_conducted (ttb_id INTEGER, dt TEXT, UNIQUE(ttb_id, dt))''')
    
    # Inject default ADMIN account on first run
    c.execute("SELECT * FROM usr WHERE uid='ADMIN'")
    if not c.fetchone():
        c.execute("INSERT INTO usr VALUES ('ADMIN', '1234567890', 'admin', 'System Admin')")
    con.commit()
    con.close()

def run_q(q, vals=(), fetch=True):
    # Centralized database query runner to handle connections safely
    con = sqlite3.connect("col.db")
    c = con.cursor()
    try:
        c.execute(q, vals)
        if fetch:
            res = c.fetchall()
        else:
            con.commit()
            res = True
        return res
    except sqlite3.IntegrityError as e:
        return e
    finally:
        con.close()

# Initialize DB on startup
init_db()

# --- SESSION STATE ---
# Streamlit reruns the script on every interaction. 
# We use st.session_state to securely remember the logged-in user across reruns.
if 'uid' not in st.session_state: st.session_state.uid = None
if 'role' not in st.session_state: st.session_state.role = None
if 'name' not in st.session_state: st.session_state.name = None

