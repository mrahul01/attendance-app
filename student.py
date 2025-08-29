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

# import streamlit as st
# import datetime
# import pandas as pd
# import urllib.parse
# import os
# from streamlit_geolocation import streamlit_geolocation

# # Constants
# ALLOWED_DISTANCE_METERS = 100 # Students must be within 100 meters of the classroom

# st.set_page_config(
#     page_title="Attendance Marker",
#     page_icon="👨‍🎓",
#     layout="centered"
# )

# st.title("👨‍🎓 Student - Mark Attendance")

# # Get query parameters from the QR code URL
# query_params = st.experimental_get_query_params()
# session_id = query_params.get("session_id", [None])[0]
# topic = query_params.get("topic", [None])[0]
# lat_classroom = query_params.get("lat", [None])[0]
# lon_classroom = query_params.get("lon", [None])[0]

# # Decode topic if it's URL-encoded
# if topic:
#     topic = urllib.parse.unquote(topic)

# st.subheader("Attendance Details")
# st.write(f"**Session ID:** `{session_id}`")
# st.write(f"**Topic:** `{topic}`")

# # Check if all required parameters are available
# if not all([session_id, topic, lat_classroom, lon_classroom]):
#     st.error("Invalid QR code. Please scan a valid QR code from your teacher.")
#     st.stop()

# # Convert classroom coordinates to floats
# try:
#     lat_classroom_f = float(lat_classroom)
#     lon_classroom_f = float(lon_classroom)
# except ValueError:
#     st.error("Invalid QR code. Location data is corrupted.")
#     st.stop()

# # Get student's location
# st.info("Click 'Get My Location' and allow location access to mark your attendance.")
# location = streamlit_geolocation()

# if location and location.get("latitude") is not None and location.get("longitude") is not None:
#     student_lat = location.get("latitude")
#     student_lon = location.get("longitude")

#     st.success(f"Your Location: {student_lat:.6f}, {student_lon:.6f}")

#     # Calculate distance using Haversine formula
#     # This is a simplified calculation for demonstration
#     def haversine_distance(lat1, lon1, lat2, lon2):
#         R = 6371000 # Radius of Earth in meters
#         phi1 = lat1 * 3.14159 / 180
#         phi2 = lat2 * 3.14159 / 180
#         delta_phi = (lat2 - lat1) * 3.14159 / 180
#         delta_lambda = (lon2 - lon1) * 3.14159 / 180

#         a = (delta_phi / 2)**2 + (delta_lambda / 2)**2 * ((phi1+phi2)/2)**2
#         c = 2 * (a)**0.5
#         d = R * c
#         return d

#     distance = haversine_distance(lat_classroom_f, lon_classroom_f, student_lat, student_lon)

#     # Check if student is within the allowed distance
#     if distance > ALLOWED_DISTANCE_METERS:
#         st.error(f"You are too far from the classroom. Your location is {distance:.2f} meters away.")
#     else:
#         st.success(f"You are within {distance:.2f} meters of the classroom.")

#         # Get student's name
#         student_name = st.text_input("Enter your full name")

#         # Mark attendance button
#         if st.button("Mark My Attendance"):
#             if not student_name:
#                 st.warning("Please enter your name to mark attendance.")
#             else:
#                 st.write("---")
                
#                 # Use current date to create a filename
#                 today_date = datetime.date.today().strftime("%Y-%m-%d")
                
#                 # Create the attendance record
#                 attendance_record = {
#                     "student_name": student_name,
#                     "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#                     "latitude": student_lat,
#                     "longitude": student_lon,
#                     "distance_meters": round(distance, 2)
#                 }

#                 # Construct the filename and path
#                 filename = f"{topic}_{today_date}.csv"
#                 filepath = os.path.join(os.path.dirname(__file__), filename)

#                 # Check if file exists to determine if we need to write headers
#                 file_exists = os.path.exists(filepath)
                
#                 # Append to the file
#                 with open(filepath, 'a' if file_exists else 'w') as f:
#                     if not file_exists:
#                         f.write("student_name,timestamp,latitude,longitude,distance_meters\n")
                    
#                     record_line = ",".join([
#                         f'"{attendance_record["student_name"]}"',
#                         attendance_record["timestamp"],
#                         str(attendance_record["latitude"]),
#                         str(attendance_record["longitude"]),
#                         str(attendance_record["distance_meters"])
#                     ])
#                     f.write(record_line + "\n")
                
#                 st.success("🎉 Attendance marked successfully!")
#                 st.balloons()
#                 st.info(f"Your attendance for topic '{topic}' has been saved.")
#                 st.write("Your location has been logged.")
#                 st.write(attendance_record)

# else:
#     st.info("Waiting for location coordinates...")




import streamlit as st
import datetime
import urllib.parse
import os
import pandas as pd
from streamlit_geolocation import streamlit_geolocation

# Constants
ALLOWED_DISTANCE_METERS = 100 # Students must be within 100 meters of the classroom

st.set_page_config(
    page_title="Attendance Marker",
    page_icon="👨‍🎓",
    layout="centered"
)

st.title("👨‍🎓 Student - Mark Attendance")

# Get query parameters from the QR code URL
query_params = st.experimental_get_query_params()
session_id = query_params.get("session_id", [None])[0]
topic = query_params.get("topic", [None])[0]
lat_classroom = query_params.get("lat", [None])[0]
lon_classroom = query_params.get("lon", [None])[0]

# Decode topic if it's URL-encoded
if topic:
    topic = urllib.parse.unquote(topic)

st.subheader("Attendance Details")
st.write(f"**Session ID:** `{session_id}`")
st.write(f"**Topic:** `{topic}`")

# Check if all required parameters are available
if not all([session_id, topic, lat_classroom, lon_classroom]):
    st.error("Invalid QR code. Please scan a valid QR code from your teacher.")
    st.stop()

# Convert classroom coordinates to floats
try:
    lat_classroom_f = float(lat_classroom)
    lon_classroom_f = float(lon_classroom)
except ValueError:
    st.error("Invalid QR code. Location data is corrupted.")
    st.stop()

# Get student's location
st.info("Click 'Get My Location' and allow location access to mark your attendance.")
location = streamlit_geolocation()

if location and location.get("latitude") is not None and location.get("longitude") is not None:
    student_lat = location.get("latitude")
    student_lon = location.get("longitude")

    st.success(f"Your Location: {student_lat:.6f}, {student_lon:.6f}")

    # Haversine distance calculation
    def haversine_distance(lat1, lon1, lat2, lon2):
        R = 6371000 # Radius of Earth in meters
        phi1 = lat1 * 3.14159 / 180
        phi2 = lat2 * 3.14159 / 180
        delta_phi = (lat2 - lat1) * 3.14159 / 180
        delta_lambda = (lon2 - lon1) * 3.14159 / 180

        a = (delta_phi / 2)**2 + (delta_lambda / 2)**2 * ((phi1+phi2)/2)**2
        c = 2 * (a)**0.5
        d = R * c
        return d

    distance = haversine_distance(lat_classroom_f, lon_classroom_f, student_lat, student_lon)

    # Check if student is within the allowed distance
    if distance > ALLOWED_DISTANCE_METERS:
        st.error(f"You are too far from the classroom. Your location is {distance:.2f} meters away.")
    else:
        st.success(f"You are within {distance:.2f} meters of the classroom.")
        
        student_name = st.text_input("Enter your full name")

        if st.button("Mark My Attendance"):
            if not student_name:
                st.warning("Please enter your name to mark attendance.")
            else:
                st.write("---")
                
                # Use current date to create a filename
                today_date = datetime.date.today().strftime("%Y-%m-%d")
                
                # Create the attendance record
                attendance_record = {
                    "student_name": student_name,
                    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "latitude": student_lat,
                    "longitude": student_lon,
                    "distance_meters": round(distance, 2)
                }

                # Construct the filename and path
                filename = f"Attendance_{topic}_{today_date}.csv"
                filepath = os.path.join(os.path.dirname(__file__), filename)

                # Check if file exists to determine if we need to write headers
                file_exists = os.path.exists(filepath)
                
                # Append to the file
                with open(filepath, 'a' if file_exists else 'w') as f:
                    if not file_exists:
                        f.write("student_name,timestamp,latitude,longitude,distance_meters\n")
                    
                    record_line = ",".join([
                        f'"{attendance_record["student_name"]}"',
                        attendance_record["timestamp"],
                        str(attendance_record["latitude"]),
                        str(attendance_record["longitude"]),
                        str(attendance_record["distance_meters"])
                    ])
                    f.write(record_line + "\n")
                
                st.success("🎉 Attendance marked successfully!")
                st.balloons()
                st.info(f"Your attendance for topic '{topic}' has been saved to the CSV file.")
                st.write("Your location has been logged.")
                st.write(attendance_record)
else:
    st.info("Waiting for location coordinates...")

