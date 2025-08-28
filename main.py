import streamlit as st
import teacher
import student

st.title("📚 Smart Attendance System")

choice = st.sidebar.radio("Choose Role", ["Teacher", "Student"])

if choice == "Teacher":
    teacher.run()   # call teacher app
elif choice == "Student":
    student.run()   # call student app

