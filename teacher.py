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

# --- App Configuration ---
st.set_page_config(
    page_title="Attendance QR Generator",
    page_icon="👨‍�",
    layout="centered"
)

# --- JavaScript to get location ---
# This is a small HTML/JS component that asks for the user's location
# and then sends it back to Streamlit via a button.
components.html(
    """
    <button id="getLocationBtn" style="display: none;">Get Location</button>
    <p id="lat-display" style="display: none;"></p>
    <p id="lon-display" style="display: none;"></p>
    <script>
    const getLocationBtn = document.getElementById('getLocationBtn');
    const latDisplay = document.getElementById('lat-display');
    const lonDisplay = document.getElementById('lon-display');
    
    getLocationBtn.addEventListener('click', () => {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, showError);
        } else {
            alert("Geolocation is not supported by this browser.");
        }
    });

    function showPosition(position) {
        latDisplay.innerText = position.coords.latitude;
        lonDisplay.innerText = position.coords.longitude;
        // Simulate a click on a hidden button in the Streamlit app to pass the data back
        const latInput = window.parent.document.querySelector('[data-testid="stTextInput"] input[type="text"][placeholder*="Latitude"]');
        const lonInput = window.parent.document.querySelector('[data-testid="stTextInput"] input[type="text"][placeholder*="Longitude"]');
        
        if (latInput && lonInput) {
            // Setting the value and dispatching a change event
            latInput.value = position.coords.latitude;
            latInput.dispatchEvent(new Event('input', { bubbles: true }));
            
            lonInput.value = position.coords.longitude;
            lonInput.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }

    function showError(error) {
        switch(error.code) {
            case error.PERMISSION_DENIED:
                alert("User denied the request for Geolocation.");
                break;
            case error.POSITION_UNAVAILABLE:
                alert("Location information is unavailable.");
                break;
            case error.TIMEOUT:
                alert("The request to get user location timed out.");
                break;
            case error.UNKNOWN_ERROR:
                alert("An unknown error occurred.");
                break;
        }
    }

    // Trigger the JS button click when a Streamlit button is clicked
    const stButton = window.parent.document.querySelector('button[kind="secondary"][aria-label="Get My Location"]');
    if (stButton) {
        stButton.addEventListener('click', () => {
            getLocationBtn.click();
        });
    }

    </script>
    """,
    height=0,  # Hide the component itself
    width=0
)

# --- Teacher Panel ---
st.title(" Teacher - Attendance QR Generator")

# Generate unique session
session_id = str(uuid.uuid4())[:8]

st.info(" Click 'Get My Location' to use your current coordinates.")
col1, col2 = st.columns(2)
with col1:
    topic = st.text_input("Enter Topic / Subject Name")
with col2:
    st.button("Get My Location", help="Click to populate Lat/Lon fields with your current location.", type="secondary")

lat = st.text_input("Enter Classroom Latitude (copy from Google Maps)", key="lat_input")
lon = st.text_input("Enter Classroom Longitude (copy from Google Maps)", key="lon_input")

if st.button("Generate Attendance QR", type="primary"):
    if not topic or not lat or not lon:
        st.warning(" Please enter all details")
    else:
        # URL for student portal (Replace localhost with deployment URL if hosted)
        student_url = f"http://localhost:8502/?session_id={session_id}&topic={urllib.parse.quote(topic)}&lat={lat}&lon={lon}"

        # Generate QR
        qr = qrcode.make(student_url)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        qr_img = buf.getvalue()

        # Show QR
        st.image(qr_img, caption="📲 Scan this QR for Attendance", use_column_width=True)

        # Show session details
        st.success(f"QR Generated for session `{session_id}`")
        st.write("Topic:", topic)
        st.write("Location:", lat, lon)
        st.write("Student Link:", student_url)