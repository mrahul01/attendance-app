# import streamlit as st
# import qrcode
# import uuid
# import io
# import urllib.parse
# from streamlit_geolocation import streamlit_geolocation

# st.set_page_config(
#     page_title="Attendance QR Generator",
#     page_icon="👨‍🏫",
#     layout="centered"
# )

# st.title("👨‍🏫 Teacher - Attendance QR Generator")

# # Generate unique session id once per app run
# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())[:8]
# session_id = st.session_state.session_id

# topic = st.text_input("Enter Topic / Subject Name")

# # Button to trigger location request
# if st.button("Get My Location"):
#     st.session_state.get_location = True

# # Request location if triggered
# if st.session_state.get_location if "get_location" in st.session_state else False:
#     location = streamlit_geolocation()
#     if location:
#         lat = location.get("latitude")
#         lon = location.get("longitude")
#         if lat is not None and lon is not None:
#             st.success(f"Got location: {lat:.6f}, {lon:.6f}")
#             st.session_state.lat = lat
#             st.session_state.lon = lon
#             st.session_state.get_location = False  # reset trigger
#         else:
#             st.error("Could not get location coordinates.")
#     else:
#         st.info("Waiting for location permission...")
# else:
#     st.info("Click 'Get My Location' to allow location access.")

# # Show lat/lon fields with stored values if any
# lat_val = st.session_state.get("lat", "")
# lon_val = st.session_state.get("lon", "")
# lat = st.text_input("Classroom Latitude", value=str(lat_val), placeholder="Latitude")
# lon = st.text_input("Classroom Longitude", value=str(lon_val), placeholder="Longitude")

# if st.button("Generate Attendance QR"):
#     if not topic or not lat or not lon:
#         st.warning("Please enter all details")
#     else:
#         try:
#             lat_f = float(lat)
#             lon_f = float(lon)
#         except ValueError:
#             st.error("Please enter valid numeric latitude and longitude")
#             st.stop()

#         # Construct student URL (replace with your deployed student app URL)
#         student_url = f"https://attendance-studentmarkup.streamlit.app/?session_id={session_id}&topic={urllib.parse.quote(topic)}&lat={lat_f}&lon={lon_f}"

#         # Generate QR code
#         qr = qrcode.make(student_url)
#         buf = io.BytesIO()
#         qr.save(buf, format="PNG")
#         qr_img = buf.getvalue()

#         st.image(qr_img, caption="📲 Scan this QR for Attendance", use_column_width=True)
#         st.success(f"QR Generated for session `{session_id}`")
#         st.write("Topic:", topic)
#         st.write("Location:", lat_f, lon_f)
#         st.write("Student Link:", student_url)


import streamlit as st
import qrcode
import uuid
import io
import urllib.parse
import pandas as pd
from streamlit_geolocation import streamlit_geolocation
from google.cloud import firestore
import json

# --- Firebase Initialization and Auth ---
# Note: These global variables are provided by the canvas environment.
app_id = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';
firebaseConfig = JSON.parse(typeof __firebase_config !== 'undefined' ? __firebase_config : '{}');
initialAuthToken = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;

# Use the Firebase JS SDK from CDN
st.components.v1.html("""
    <script src="https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js"></script>
    <script src="https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js"></script>
    <script src="https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js"></script>
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-app.js";
        import { getAuth, signInAnonymously, signInWithCustomToken } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-auth.js";
        import { getFirestore, doc, addDoc, collection, onSnapshot, query, where, getDocs } from "https://www.gstatic.com/firebasejs/11.6.1/firebase-firestore.js";

        // Global variables from the Streamlit environment
        const firebaseConfig = window.parent.__firebase_config ? JSON.parse(window.parent.__firebase_config) : {};
        const initialAuthToken = window.parent.__initial_auth_token || null;
        
        // Initialize Firebase
        const app = initializeApp(firebaseConfig);
        const db = getFirestore(app);
        const auth = getAuth(app);
        
        // Expose to a global variable for Python to access
        window.firebaseData = {
            db: db,
            auth: auth,
            onSnapshot: onSnapshot,
            query: query,
            where: where,
            collection: collection,
            getDocs: getDocs,
            signInAnonymously: signInAnonymously,
            signInWithCustomToken: signInWithCustomToken
        };
        
        // Sign in anonymously or with custom token
        if (initialAuthToken) {
            signInWithCustomToken(auth, initialAuthToken)
                .then(() => console.log("Signed in with custom token"))
                .catch(error => console.error("Error signing in with custom token:", error));
        } else {
            signInAnonymously(auth)
                .then(() => console.log("Signed in anonymously"))
                .catch(error => console.error("Error signing in anonymously:", error));
        }
    </script>
    """, height=0, width=0)


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

if st.button("Get My Location"):
    st.session_state.get_location = True

if st.session_state.get_location if "get_location" in st.session_state else False:
    location = streamlit_geolocation()
    if location:
        lat = location.get("latitude")
        lon = location.get("longitude")
        if lat is not None and lon is not None:
            st.success(f"Got location: {lat:.6f}, {lon:.6f}")
            st.session_state.lat = lat
            st.session_state.lon = lon
            st.session_state.get_location = False
        else:
            st.error("Could not get location coordinates.")
    else:
        st.info("Waiting for location permission...")
else:
    st.info("Click 'Get My Location' to allow location access.")

lat_val = st.session_state.get("lat", "")
lon_val = st.session_state.get("lon", "")
lat = st.text_input("Classroom Latitude", value=str(lat_val), placeholder="Latitude")
lon = st.text_input("Classroom Longitude", value=str(lon_val), placeholder="Longitude")

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
        
        # NOTE: Replace with your deployed student app URL
        student_url = f"https://attendance-app-student.streamlit.app/?session_id={session_id}&topic={urllib.parse.quote(topic)}&lat={lat_f}&lon={lon_f}"

        qr = qrcode.make(student_url)
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        qr_img = buf.getvalue()

        st.image(qr_img, caption="📲 Scan this QR for Attendance", use_column_width=True)
        st.success(f"QR Generated for session `{session_id}`")
        st.write("Topic:", topic)
        st.write("Location:", lat_f, lon_f)
        st.write("Student Link:", student_url)

# Display Attendance Data
st.subheader("Live Attendance Records")
st.markdown(f"Attendance for **Topic: `{topic}`** and **Session: `{session_id}`**")

if "attendance_data" not in st.session_state:
    st.session_state.attendance_data = []

# Fetch data from Firestore and update the session state
@st.cache_data(show_spinner=False)
def get_attendance_records(session_id, topic):
    # This is a hacky way to get data from JS to Python in Streamlit
    js_code = f"""
        (async () => {{
            const db = window.firebaseData.db;
            const collection = window.firebaseData.collection;
            const query = window.firebaseData.query;
            const where = window.firebaseData.where;
            const getDocs = window.firebaseData.getDocs;
            const appId = '{app_id}';
            
            const path = `artifacts/${appId}/public/data/attendance`;
            const attendanceQuery = query(collection(db, path), where("session_id", "==", "{session_id}"), where("topic", "==", "{topic}"));
            
            const querySnapshot = await getDocs(attendanceQuery);
            const data = [];
            querySnapshot.forEach((doc) => {{
                data.push(doc.data());
            }});
            
            // Send the data back to Streamlit
            Streamlit.setComponentValue("attendance_data", JSON.stringify(data));
        }})();
    """
    st.components.v1.html(f"<script>{js_code}</script>", height=0, width=0)

get_attendance_records(session_id, topic)

# Get the data from the component value
component_value = st.components.v1.html_component_value("attendance_data", default="[]")
attendance_records = json.loads(component_value)
df = pd.DataFrame(attendance_records)

if not df.empty:
    st.dataframe(df)

    # Convert DataFrame to CSV for download
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df_to_csv(df)
    st.download_button(
        label="Download Attendance as CSV",
        data=csv,
        file_name=f"Attendance_{topic}_{session_id}.csv",
        mime="text/csv",
    )
else:
    st.info("No attendance records found for this session.")
