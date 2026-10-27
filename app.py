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

    con.commit()
    con.close()