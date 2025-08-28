# import streamlit as st
# import pandas as pd
# import os
# from datetime import datetime

# # ========= Get Session ID from URL =========
# query_params = st.query_params  # ✅ Streamlit 1.31+ supports this
# session_id = query_params.get("session_id", [""])[0]

# if not session_id:
#     st.error("❌ No session active. Please scan the latest QR code from your teacher.")
#     st.stop()

# st.title("📲 Student Attendance")
# st.info(f"✅ You are marking attendance for Session: {session_id}")

# # ========= Student Input =========
# student_name = st.text_input("Enter Your Name / Roll Number")

# if st.button("Mark Attendance"):
#     if not student_name.strip():
#         st.warning("⚠️ Please enter your name/roll number")
#     else:
#         filename = f"Attendance_{session_id}.csv"

#         # If file doesn't exist, create with headers
#         if not os.path.exists(filename):
#             df = pd.DataFrame(columns=["Name", "Timestamp"])
#             df.to_csv(filename, index=False)

#         # Load existing attendance
#         df = pd.read_csv(filename)

#         # Check if student already marked
#         if student_name in df["Name"].values:
#             st.warning("⚠️ Attendance already marked for you in this session!")
#         else:
#             now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#             new_entry = pd.DataFrame([[student_name, now]], columns=["Name", "Timestamp"])
#             df = pd.concat([df, new_entry], ignore_index=True)
#             df.to_csv(filename, index=False)

#             st.success(f"✅ Attendance marked for {student_name} at {now}")

import streamlit as st
from math import radians, sin, cos, sqrt, atan2

# ===== Helper: Distance Calculation (Haversine formula) =====
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# ===== Student App =====
st.title("👩‍🎓 Student Attendance Portal")

# ✅ use new API
params = st.query_params  

session_id = params.get("session_id", [""])[0]
topic = params.get("topic", [""])[0]
teacher_lat = float(params.get("lat", ["0"])[0])
teacher_lon = float(params.get("lon", ["0"])[0])

if not session_id:
    st.error("⚠️ Invalid or missing QR code link")
else:
    st.success(f"📚 Topic: {topic}")
    st.write(f"🆔 Session: {session_id}")

    # Student enters name and current GPS
    student_name = st.text_input("Enter your Name")
    my_lat = st.number_input("Enter your Latitude (from Google Maps)", format="%.6f")
    my_lon = st.number_input("Enter your Longitude (from Google Maps)", format="%.6f")

    if st.button("Mark Attendance"):
        if not student_name:
            st.warning("⚠️ Please enter your name")
        else:
            distance = haversine(my_lat, my_lon, teacher_lat, teacher_lon)
            if distance <= 55:
                # ✅ Only one attendance per student
                if "attendance" not in st.session_state:
                    st.session_state.attendance = set()

                if student_name in st.session_state.attendance:
                    st.error("❌ Attendance already marked!")
                else:
                    st.session_state.attendance.add(student_name)
                    st.success(f"✅ Attendance marked for {student_name}")
            else:
                st.error("❌ You are outside the 55 meter range of the classroom")
