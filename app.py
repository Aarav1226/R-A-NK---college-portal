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

def logout():
    st.session_state.uid = None
    st.session_state.role = None
    st.session_state.name = None

# --- LOGIN & REGISTRATION ---
def show_login():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("<h1 style='font-size: 80px; color: #ff007f; margin-bottom: 0px;'>R(A)NK</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='color: #0275d8; margin-top: 0px;'>Rajeev Ankita Network Knowledge</h3>", unsafe_allow_html=True)
        st.markdown("<h2>UNIVERSITY OF TOMORROW</h2>", unsafe_allow_html=True)
        st.write("A Modern Educational Portal.")
        
    with col2:
        st.markdown("### Welcome to the R(A)NK Portal")
        tab1, tab2 = st.tabs(["Secure Login", "Create Account"])
        
        with tab1:
            with st.form("login_form"):
                uid = st.text_input("User Name / SAP ID")
                psw = st.text_input("Password", type="password")
                submit = st.form_submit_button("LOGIN", use_container_width=True)
                
                if submit:
                    # Verify credentials against the database
                    res = run_q("SELECT role, name FROM usr WHERE uid=? AND psw=?", (uid.strip(), psw.strip()))
                    if res and not isinstance(res, Exception):
                        st.session_state.uid = uid.strip()
                        st.session_state.role = res[0][0]
                        st.session_state.name = res[0][1]
                        st.rerun() # Refresh the page to load the correct dashboard
                    else:
                        st.error("Invalid ID or Password")
                        
        with tab2:
            with st.form("reg_form"):
                n_uid = st.text_input("SAP ID")
                n_psw = st.text_input("Password", type="password")
                n_nm = st.text_input("Full Name")
                n_role = st.radio("Role", ["Student", "Teacher"], horizontal=True)
                
                # Default empty subject unless teacher
                n_sub = st.selectbox("Subject Specialisation (Teachers Only)", SUBJECTS) if n_role == "Teacher" else None
                
                reg_submit = st.form_submit_button("REGISTER", use_container_width=True)
                
                if reg_submit:
                    if n_uid == "ADMIN":
                        st.error("Cannot register as ADMIN")
                    elif not n_uid or not n_psw or not n_nm:
                        st.warning("Please fill all fields.")
                    else:
                        rl_code = "stu" if n_role == "Student" else "tch"
                        # CRUD: CREATE new user in the main usr table
                        res = run_q("INSERT INTO usr VALUES (?, ?, ?, ?)", (n_uid, n_psw, rl_code, n_nm), fetch=False)
                        if isinstance(res, Exception):
                            st.error("ID already exists!")
                        else:
                            # Also link them into their specific role table
                            if rl_code == "stu":
                                run_q("INSERT INTO stu VALUES (?, 'A', 1, 0, 0)", (n_uid,), fetch=False)
                            else:
                                run_q("INSERT INTO tch VALUES (?, 'A', ?)", (n_uid, n_sub), fetch=False)
                            st.success("Account Created! Please Login.")

# --- ADMIN PORTAL ---
def show_admin():
    st.sidebar.title("🔧 Admin Dashboard")
    menu = st.sidebar.radio("Navigation", ["Timetable Manager", "Library & Admissions", "User Directory"])
    st.sidebar.button("⏻ Logout", on_click=logout)
    
    if menu == "Timetable Manager":
        st.header("Weekly Timetable Builder")
        with st.form("ttb_form"):
            c1, c2, c3, c4 = st.columns(4)
            bat = c1.selectbox("Batch", ["A", "B", "C", "D"])
            day = c2.selectbox("Day", ["Mon", "Tue", "Wed", "Thu", "Fri"])
            tim = c3.text_input("Time (e.g. 08:00 AM - 09:00 AM)", "08:00 AM - 09:00 AM")
            sub = c4.selectbox("Subject", SUBJECTS)
            
            c5, c6 = st.columns(2)
            rm = c5.text_input("Room", "101")
            
            tch_list = run_q("SELECT uid, name FROM usr WHERE role='tch'")
            tch_options = {f"{t[0]} - {t[1]}": t[0] for t in tch_list}
            tch = c6.selectbox("Teacher", options=tch_options.keys())
            
            if st.form_submit_button("Add Session"):
                tid = tch_options[tch]
                run_q("INSERT INTO ttb (bat, day, tim, sub, rm, tid) VALUES (?, ?, ?, ?, ?, ?)", 
                      (bat, day, tim, sub, rm, tid), fetch=False)
                st.success("Session Added!")
                
        st.subheader("Weekly Timetable Matrix View")
        view_bat = st.selectbox("Select Batch to View:", ["A", "B", "C", "D"])
        sessions = run_q("SELECT day, tim, sub, rm, u.name FROM ttb t LEFT JOIN usr u ON t.tid=u.uid WHERE bat=?", (view_bat,))
        if not sessions:
            st.info("No sessions scheduled for this batch.")
        else:
            df_mat = pd.DataFrame(sessions, columns=["Day", "Time", "Subject", "Room", "Teacher"])
            # Format multi-line content for Matrix cells
            df_mat["Details"] = df_mat["Subject"] + "\nRoom: " + df_mat["Room"] + "\nProf. " + df_mat["Teacher"]
            
            # Pivot table converts vertical database list into Horizontal Mon-Sun Matrix!
            pivot_df = df_mat.pivot_table(index="Time", columns="Day", values="Details", aggfunc=lambda x: '\n---\n'.join(x)).fillna("-")
            
            # Ensure chronological days (Columns)
            existing_days = [d for d in DAYS_ORDER_LIST if d in pivot_df.columns]
            pivot_df = pivot_df[existing_days]
            
            # Ensure chronological times (Rows) by converting start-time string to an actual Datetime object
            # This fixes the issue where "01:00 PM" sorts above "08:00 AM" alphabetically
            try:
                sorted_idx = sorted(pivot_df.index, key=lambda t: pd.to_datetime(t.split('-')[0].strip(), format='%I:%M %p'))
                pivot_df = pivot_df.loc[sorted_idx]
            except Exception:
                pivot_df = pivot_df.sort_index()
                
            st.table(pivot_df)

        st.markdown("---")
        st.subheader("Manage / Delete Records")
        ttbs = run_q("SELECT t.id, t.bat, t.day, t.tim, t.sub, t.rm, u.name FROM ttb t LEFT JOIN usr u ON t.tid=u.uid")
        if ttbs:
            df = pd.DataFrame(ttbs, columns=["ID", "Batch", "Day", "Time", "Subject", "Room", "Teacher"])
            df["Day_Num"] = df["Day"].map(DAY_ORDER_MAP)
            
            try:
                df["Sort_Time"] = pd.to_datetime(df["Time"].apply(lambda x: x.split('-')[0].strip()), format='%I:%M %p')
                df = df.sort_values(["Batch", "Day_Num", "Sort_Time"]).drop(columns=["Day_Num", "Sort_Time"])
            except:
                df = df.sort_values(["Batch", "Day_Num", "Time"]).drop(columns=["Day_Num"])
            
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            del_id = st.number_input("Enter Session ID to delete:", step=1, min_value=0)
            if st.button("Delete Session"):
                # CRUD: DELETE session
                run_q("DELETE FROM ttb WHERE id=?", (del_id,), fetch=False)
                st.rerun()

    elif menu == "Library & Admissions":
        c1, c2 = st.columns(2)
        with c1:
            st.header("📚 Library Management")
            new_bk = st.text_input("New Book Title")
            if st.button("Add Book to Library"):
                # CRUD: CREATE new book
                run_q("INSERT INTO bks (title, rent) VALUES (?, '')", (new_bk,), fetch=False)
                st.success("Book Added!")
                
            st.subheader("Inventory (Update & Delete)")
            bks = run_q("SELECT bid, title, rent FROM bks")
            if bks:
                df_b = pd.DataFrame(bks, columns=["ID", "Title", "Rented To (UID)"])
                # Editable data frame for updating book titles
                edited_bks = st.data_editor(df_b, disabled=["ID", "Rented To (UID)"], use_container_width=True, hide_index=True, key="bks_editor")
                if st.button("Save Book Updates"):
                    for index, row in edited_bks.iterrows():
                        b_id = df_b.at[index, "ID"]
                        new_title = row["Title"]
                        run_q("UPDATE bks SET title=? WHERE bid=?", (new_title, b_id), fetch=False)
                    st.success("Book records updated!")
                    st.rerun()
                
                st.markdown("---")
                # Section for deleting a book
                del_bk_id = st.number_input("Enter Book ID to delete:", step=1, min_value=0)
                if st.button("Delete Book"):
                    run_q("DELETE FROM bks WHERE bid=?", (del_bk_id,), fetch=False)
                    st.success("Book deleted!")
                    st.rerun()
            else:
                st.info("Library is empty.")
            
        with c2:
            st.header("🎓 Admissions & Fees")
            st.subheader("Batch Promotion")
            promo_bat = st.selectbox("Promote Batch to Next Semester:", ["A", "B", "C", "D", "ALL"])
            if st.button("Promote & Apply New Dues"):
                stus = run_q("SELECT uid, sem, fee FROM stu") if promo_bat == "ALL" else run_q("SELECT uid, sem, fee FROM stu WHERE bat=?", (promo_bat,))
                count = 0
                for u, s, f in stus:
                    if s < 8:
                        ns = s + 1
                        nf = f + SEMESTER_FEES[ns] # Automates fee increments perfectly
                        run_q("UPDATE stu SET sem=?, fee=? WHERE uid=?", (ns, nf, u), fetch=False)
                        count += 1
                st.success(f"Promoted {count} students and applied automated dues!")
                
            st.subheader("Manual Fine")
            f_uid = st.text_input("Target SAP ID")
            f_amt = st.number_input("Fine Amount (Rs)", min_value=0, step=100)
            if st.button("Apply Penalty"):
                res = run_q("SELECT uid FROM stu WHERE uid=?", (f_uid.strip(),))
                if res:
                    run_q("UPDATE stu SET fee = fee + ? WHERE uid=?", (f_amt, f_uid.strip()), fetch=False)
                    st.success(f"Applied Rs. {f_amt} fine to {f_uid.strip()}")
                else:
                    st.error("Student SAP ID not found.")

    elif menu == "User Directory":
        st.header("👥 User Directory")
        tabs = st.tabs(["Manage Teachers", "Manage Students"])
        
        with tabs[0]:
            st.subheader("Teacher Records (Update)")
            st.info("Edit teacher details directly in the table. Changing an ID will automatically migrate all their linked data.")
            tchs = run_q("SELECT t.uid, u.name, t.sub FROM tch t JOIN usr u ON t.uid = u.uid")
            
            if tchs:
                df_tch = pd.DataFrame(tchs, columns=["SAP ID", "Name", "Subject"])
                edited_tch = st.data_editor(df_tch, use_container_width=True, hide_index=True, key="tch_editor")
                
                if st.button("Save Teacher Changes", type="primary"):
                    for index, row in edited_tch.iterrows():
                        old_uid = df_tch.at[index, "SAP ID"]
                        new_uid = row["SAP ID"]
                        new_name = row["Name"]
                        new_sub = row["Subject"]
                        
                        if old_uid != new_uid:
                            # CASCADING UPDATE: If the Primary Key (SAP ID) is changed, migrate all linked data!
                            res = run_q("UPDATE usr SET uid=?, name=? WHERE uid=?", (new_uid, new_name, old_uid), fetch=False)
                            if isinstance(res, Exception):
                                st.error(f"Cannot change ID {old_uid} to {new_uid}: ID already in use!")
                            else:
                                run_q("UPDATE tch SET uid=?, sub=? WHERE uid=?", (new_uid, new_sub, old_uid), fetch=False)
                                run_q("UPDATE ttb SET tid=? WHERE tid=?", (new_uid, old_uid), fetch=False)
                        else:
                            run_q("UPDATE usr SET name=? WHERE uid=?", (new_name, old_uid), fetch=False)
                            run_q("UPDATE tch SET sub=? WHERE uid=?", (new_sub, old_uid), fetch=False)
                            
                    st.success("Teacher directory updated successfully!")
                    st.rerun()


        with tabs[1]: pass