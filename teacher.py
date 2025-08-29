# import streamlit as st
# import qrcode
# import uuid   # ✅ to generate unique session id
# from io import BytesIO

# # ✅ Generate a new attendance session
# session_id = str(uuid.uuid4())[:8]   # random 8-digit session id
# base_url = "http://localhost:8501"   # change if you deploy online
# qr_data = f"{base_url}?session_id={session_id}"

# # ✅ Generate QR image
# qr_img = qrcode.make(qr_data)

# # Convert QR to byte stream for Streamlit
# buf = BytesIO()
# qr_img.save(buf, format="PNG")
# buf.seek(0)

# # ✅ Streamlit UI
# st.title("🎓 Teacher's Attendance Panel")
# st.image(buf, caption="📸 Scan this QR to mark attendance", use_column_width=True)
# st.success(f"✅ Current Session ID: {session_id}")

import streamlit as st
import qrcode
import uuid
import io
import urllib.parse
import streamlit.components.v1 as components

st.set_page_config(page_title="Attendance QR Generator", page_icon="📍")

st.title("📚 Teacher - Attendance QR Generator")

# Unique session ID
session_id = str(uuid.uuid4())[:8]

# --- Inject JS to get location and send it back via window.postMessage ---
location_html = """
<script>
function sendLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const coords = lat + "," + lon;
                // Send coords to Streamlit via window.postMessage
                window.parent.postMessage({isStreamlitMessage:true, type:"streamlit:setComponentValue", value: coords}, "*");
            },
            (err) => {
                alert("Error getting location: " + err.message);
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}
</script>
<button onclick="sendLocation()">📍 Get My Location</button>
"""

# This creates a hidden Streamlit component that can receive the message from JS
coords = components.html(location_html, height=60)

# coords will always be None here because components.html does not capture postMessage return value
# So we need a workaround: use a text_input to receive coords manually or use a custom component

# Workaround: ask user to paste coords manually (for demo)
coords_input = st.text_input("Paste your location here as 'lat,lon' after clicking the button above")

lat, lon = "", ""
if coords_input:
    try:
        lat, lon = coords_input.split(",")
    except:
        st.error("Invalid location format. Use 'lat,lon'")

# --- Teacher Input ---
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("Enter Topic / Subject Name")
with col2:
    st.text(f"Lat: {lat}, Lon: {lon}")

# --- Generate QR ---
if st.button("Generate Attendance QR", type="primary"):
    if not topic or not lat or not lon:
        st.warning("⚠️ Please enter all details (topic and location).")
    else:
        student_url = f"https://attendance-studentmarkup.streamlit.app/?session_id={session_id}&topic={urllib.parse.quote(topic)}&lat={lat}&lon={lon}"

        qr = qrcode.make(student_url)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        qr_img = buf.getvalue()

        st.image(qr_img, caption="📲 Scan this QR for Attendance", use_column_width=True)

        st.success(f"✅ Session `{session_id}` created")
        st.write("Topic:", topic)
        st.write("Location:", lat, lon)
        st.write("Student Link:", student_url)


