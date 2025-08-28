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

# --- Get location using JS and return to Streamlit ---
location_html = """
<script>
function sendLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => {
                const lat = pos.coords.latitude;
                const lon = pos.coords.longitude;
                const streamlitMsg = {"isStreamlitMessage":true,"type":"streamlit:setComponentValue","value": lat + "," + lon};
                window.parent.postMessage(streamlitMsg, "*");
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

coords = components.html(location_html, height=50)

lat, lon = "", ""
if coords:
    try:
        lat, lon = coords.split(",")
    except:
        pass

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
        student_url = f"http://localhost:8502/?session_id={session_id}&topic={urllib.parse.quote(topic)}&lat={lat}&lon={lon}"

        qr = qrcode.make(student_url)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        qr_img = buf.getvalue()

        st.image(qr_img, caption="📲 Scan this QR for Attendance", use_column_width=True)

        st.success(f"✅ Session `{session_id}` created")
        st.write("Topic:", topic)
        st.write("Location:", lat, lon)
        st.write("Student Link:", student_url)
