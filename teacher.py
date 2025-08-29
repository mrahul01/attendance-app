import streamlit as st
from streamlit_geolocation import streamlit_geolocation

st.title("Teacher Location")

# Button to trigger location request
if st.button("Get My Location"):
    st.session_state.get_location = True

if "get_location" in st.session_state and st.session_state.get_location:
    location = streamlit_geolocation()
    if location:
        lat = location.get("latitude")
        lon = location.get("longitude")
        if lat is not None and lon is not None:
            st.success(f"Got location: {lat}, {lon}")
            st.session_state.lat = lat
            st.session_state.lon = lon
            st.session_state.get_location = False  # reset trigger
        else:
            st.error("Could not get location coordinates.")
    else:
        st.info("Waiting for location permission...")
else:
    st.info("Click 'Get My Location' to allow location access.")

# Show lat/lon fields with stored values if any
lat_val = st.session_state.get("lat", "")
lon_val = st.session_state.get("lon", "")
lat = st.text_input("Latitude", value=str(lat_val))
lon = st.text_input("Longitude", value=str(lon_val))
