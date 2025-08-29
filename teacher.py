import streamlit as st
import qrcode
import uuid
import io
import urllib.parse
from streamlit_geolocation import streamlit_geolocation

st.set_page_config(
    page_title="Attendance QR Generator",
    page_icon="👨‍🏫",
    layout="centered"
)

st.title("👨‍🏫 Teacher - Attendance QR Generator")

# Generate unique session id once per app run
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())[:8]
session_id = st.session_state.session_id

topic = st.text_input("Enter Topic / Subject Name")

# Button to get teacher location
if st.button("Get My Location"):
    location = streamlit_geolocation()
    if location:
        lat = location.get("latitude")
        lon = location.get("longitude")
        if lat is not None and lon is not None:
            st.session_state.lat = lat
            st.session_state.lon = lon
        else:
            st.error("Could not get location coordinates.")
    else:
        st.info("Waiting for location permission...")

# Show lat/lon if available
lat = st.text_input("Classroom Latitude", value=str(st.session_state.get("lat", "")), placeholder="Latitude")
lon = st.text_input("Classroom Longitude", value=str(st.session_state.get("lon", "")), placeholder="Longitude")

if st.button("Generate Attendance QR"):
    if not topic or not lat or not lon:
        st.warning("Please enter all details")
    else:
        try:
            lat_f = float(lat)
            lon_f = float(lon)
        except ValueError:
            st.error("Please enter valid numeric latitude and longitude")
            st.stop()

        # Construct student URL (replace with your deployed student app URL)
        student_url = f"https://attendance-studentmarkup.streamlit.app/?session_id={session_id}&topic={urllib.parse.quote(topic)}&lat={lat_f}&lon={lon_f}"

        # Generate QR code
        qr = qrcode.make(student_url)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        qr_img = buf.getvalue()

        st.image(qr_img, caption="📲 Scan this QR for Attendance", use_column_width=True)
        st.success(f"QR Generated for session `{session_id}`")
        st.write("Topic:", topic)
        st.write("Location:", lat_f, lon_f)
        st.write("Student Link:", student_url)
