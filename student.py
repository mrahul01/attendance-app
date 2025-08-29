import streamlit as st
from streamlit_geolocation import streamlit_geolocation
from math import radians, sin, cos, sqrt, atan2

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth radius in meters
    phi1 = radians(lat1)
    phi2 = radians(lat2)
    dphi = radians(lat2 - lat1)
    dlambda = radians(lon2 - lon1)
    a = sin(dphi/2)**2 + cos(phi1) * cos(phi2) * sin(dlambda/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

params = st.query_params  
session_id = params.get("session_id", [""])[0]
topic = params.get("topic", [""])[0]
teacher_lat = float(params.get("lat", ["0"])[0])
teacher_lon = float(params.get("lon", ["0"])[0])

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

        if st.button("Mark Attendance"):
            if not student_name:
                st.warning("⚠️ Please enter your name")
            else:
                distance = haversine(lat, lon, teacher_lat, teacher_lon)
                if distance <= 55:
                    if "attendance" not in st.session_state:
                        st.session_state.attendance = set()

                    if student_name in st.session_state.attendance:
                        st.error("❌ Attendance already marked!")
                    else:
                        st.session_state.attendance.add(student_name)
                        st.success(f"✅ Attendance marked for {student_name}")
                else:
                    st.error("❌ You are outside the 55 meter range of the classroom")
    else:
        st.info("Waiting for location permission...")
else:
    st.info("Click the button above to allow location access.")
