# import streamlit as st
# from streamlit_geolocation import streamlit_geolocation
# from math import radians, sin, cos, sqrt, atan2

# def haversine(lat1, lon1, lat2, lon2):
#     R = 6371000  # Earth radius in meters
#     phi1 = radians(lat1)
#     phi2 = radians(lat2)
#     dphi = radians(lat2 - lat1)
#     dlambda = radians(lon2 - lon1)
#     a = sin(dphi/2)**2 + cos(phi1) * cos(phi2) * sin(dlambda/2)**2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))
#     return R * c

# params = st.query_params  
# session_id = params.get("session_id", [""])
# topic = params.get("topic", [""])
# teacher_lat = float(params.get("lat", ["0"]))
# teacher_lon = float(params.get("lon", ["0"]))

# if not session_id:
#     st.error("⚠️ Invalid or missing QR code link")
#     st.stop()

# st.title("👩‍🎓 Student Attendance Portal")
# st.success(f"📚 Topic: {topic}")
# st.write(f"🆔 Session: {session_id}")

# location = streamlit_geolocation()

# if location:
#     lat = location.get("latitude")
#     lon = location.get("longitude")
#     if lat is not None and lon is not None:
#         st.write(f"Your current location: {lat:.9f}, {lon:.9f}")

#         student_name = st.text_input("Enter your Name")

#         if st.button("Mark Attendance"):
#             if not student_name:
#                 st.warning("⚠️ Please enter your name")
#             else:
#                 distance = haversine(lat, lon, teacher_lat, teacher_lon)
#                 if distance <= 55:
#                     if "attendance" not in st.session_state:
#                         st.session_state.attendance = set()

#                     if student_name in st.session_state.attendance:
#                         st.error("❌ Attendance already marked!")
#                     else:
#                         st.session_state.attendance.add(student_name)
#                         st.success(f"✅ Attendance marked for {student_name}")
#                 else:
#                     st.error("❌ You are outside the 55 meter range of the classroom")
#     else:
#         st.info("Waiting for location permission...")

# st.info("Click the button above to allow location access.")
# st.write(f"Teacher location: {teacher_lat}, {teacher_lon}")
# st.write(f"Your location: {lat}, {lon}")
# distance = haversine(lat, lon, teacher_lat, teacher_lon)
# st.write(f"Distance: {distance:.2f} meters")



import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from math import radians, sin, cos, sqrt, atan2
import pandas as pd
from datetime import datetime
from github import Github, InputGitTreeElement

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1) * cos(phi2) * sin(dlambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Use Streamlit secrets for GitHub token
github_token = st.secrets["github"]["token"]
repo_name = "mrahul01/attendance-app"

# Initialize GitHub object with your token
g = Github(github_token)
repo = g.get_repo(repo_name)

# --- Existing code ---
params = st.query_params
session_id = params.get("session_id", [""])
topic = params.get("topic", [""])
teacher_lat = float(params.get("lat", ["0"]))
teacher_lon = float(params.get("lon", ["0"]))

if not session_id:
    st.error("⚠️ Invalid or missing QR code link")
    st.stop()

st.title("👩‍🎓 Student Attendance Portal")
st.success(f"📚 Topic: {topic}")
st.write(f"🆔 Session: {session_id}")

location = streamlit_geolocation()

if location:
    lat = location.get("latitude")
    lon = location.get("longitude")
    if lat is not None and lon is not None:
        st.write(f"Your current location: {lat:.9f}, {lon:.9f}")
        student_name = st.text_input("Enter your Name")
        
        # Additional input for phone information
        # Note: You need to decide how to get this info from the user or device.
        # This is just an example placeholder.
        phone_info = "iPhone 14" # Placeholder for phone info

        if st.button("Mark Attendance"):
            if not student_name:
                st.warning("⚠️ Please enter your name")
            else:
                distance = haversine(lat, lon, teacher_lat, teacher_lon)
                if distance <= 55:
                    
                    # Create a new attendance record
                    attendance_data = {
                        "name": [student_name],
                        "phone_info": [phone_info],
                        "date": [datetime.now().strftime("%Y-%m-%d")],
                        "time": [datetime.now().strftime("%H:%M:%S")],
                        "latitude": [lat],
                        "longitude": [lon]
                    }
                    
                    # File path in the GitHub repository
                    file_path = f"attendance/{topic.replace(' ', '_')}_{datetime.now().strftime('%Y-%m-%d')}.csv"

                    try:
                        # Check if file exists in the repo
                        contents = repo.get_contents(file_path, ref="main")
                        
                        # If file exists, read it, append new data, and update it.
                        existing_data = pd.read_csv(contents.download_url, encoding='utf-8')
                        new_data = pd.DataFrame(attendance_data)
                        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
                        
                        # Encode the updated content
                        updated_content = updated_df.to_csv(index=False)
                        
                        # Check for duplicate entry before committing
                        if student_name in existing_data['name'].values:
                            st.error("❌ Attendance already marked!")
                        else:
                            # Update file in GitHub
                            repo.update_file(
                                path=file_path,
                                message=f"Added attendance for {student_name} on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                                content=updated_content,
                                sha=contents.sha,
                                branch="main"
                            )
                            st.success(f"✅ Attendance marked for {student_name} and saved to GitHub!")
                            
                    except Exception as e:
                        # If file does not exist, create it.
                        if "Not Found" in str(e):
                            new_df = pd.DataFrame(attendance_data)
                            
                            # Encode the new content
                            new_content = new_df.to_csv(index=False)
                            
                            # Create file in GitHub
                            repo.create_file(
                                path=file_path,
                                message=f"Created attendance file for {topic} on {datetime.now().strftime('%Y-%m-%d')}",
                                content=new_content,
                                branch="main"
                            )
                            st.success(f"✅ Attendance marked for {student_name} and saved to GitHub!")
                        else:
                            st.error(f"❌ An error occurred: {e}")

                else:
                    st.error("❌ You are outside the 55-meter range of the classroom")
    else:
        st.info("Waiting for location permission...")

st.info("Click the button above to allow location access.")
# This part of the code is for debugging and can be removed in the final app.
if location:
    st.write(f"Teacher location: {teacher_lat}, {teacher_lon}")
    st.write(f"Your location: {lat}, {lon}")
    distance = haversine(lat, lon, teacher_lat, teacher_lon)
    st.write(f"Distance: {distance:.2f} meters")
