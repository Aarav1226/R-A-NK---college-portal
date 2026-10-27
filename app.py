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
