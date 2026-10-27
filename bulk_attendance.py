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
