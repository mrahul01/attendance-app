import streamlit as st
import qrcode
import uuid
import io
import urllib.parse

st.set_page_config(
    page_title="Attendance QR Generator",
    page_icon="👨‍🏫",
    layout="centered"
)

st.title("👨‍🏫 Teacher - Attendance QR Generator")

# Generate unique session id
session_id = str(uuid.uuid4())[:8]

st.info("Click 'Get My Location' to automatically fill classroom coordinates.")

# Inject JS + button to get location and fill inputs
st.markdown("""
<script>
async function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            const latInput = window.parent.document.querySelector('input[placeholder="Latitude"]');
            const lonInput = window.parent.document.querySelector('input[placeholder="Longitude"]');
            if (latInput && lonInput) {
                latInput.value = position.coords.latitude.toFixed(6);
                latInput.dispatchEvent(new Event('input', { bubbles: true }));
                lonInput.value = position.coords.longitude.toFixed(6);
                lonInput.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }, function(error) {
            alert("Error getting location: " + error.message);
        });
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}
</script>
<button onclick="getLocation()">Get My Location</button>
""", unsafe_allow_html=True)

topic = st.text_input("Enter Topic / Subject Name")
lat = st.text_input("Latitude", placeholder="Latitude")
lon = st.text_input("Longitude", placeholder="Longitude")

if st.button("Generate Attendance QR"):
    if not topic or not lat or not lon:
        st.warning("Please enter all details")
    else:
        # Construct student URL (replace with your deployed student app URL)
        student_url = f"https://attendance-studentmarkup.streamlit.app/?session_id={session_id}&topic={urllib.parse.quote(topic)}&lat={lat}&lon={lon}"

        # Generate QR code
        qr = qrcode.make(student_url)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        qr_img = buf.getvalue()

        st.image(qr_img, caption="📲 Scan this QR for Attendance", use_column_width=True)
        st.success(f"QR Generated for session `{session_id}`")
        st.write("Topic:", topic)
        st.write("Location:", lat, lon)
        st.write("Student Link:", student_url)
