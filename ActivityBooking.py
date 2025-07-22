import streamlit as st
import google.generativeai as genai
import requests

# Configure Gemini API (from your Streamlit secrets)
genai.configure(api_key="AIzaSyDI5Hr2zxpxm3ZyfCGgO5iTWeAp_eprUaA")
model = genai.GenerativeModel('gemini-2.5-pro')

# Streamlit App
st.set_page_config(page_title="Activity Booking Buddy", page_icon="🎉")
st.title("🎉 Activity Booking Buddy (with Gemini + OpenStreetMap)")

st.write("💬 Chat with Gemini to get activity ideas, and search real places nearby!")

# Chat with Gemini for activity ideas
user_question = st.text_input("💡 Ask Gemini: (E.g., Suggest fun outdoor activities for kids)")

if st.button("Ask Gemini"):
    if user_question.strip():
        with st.spinner("Thinking..."):
            response = model.generate_content(user_question)
            st.write("🧠 Gemini says:")
            st.write(response.text)
    else:
        st.warning("Please ask something!")

st.write("---")

# Real Places Search using OpenStreetMap (No API Key Needed)
st.subheader("📍 Find Real Places Nearby")

activity = st.text_input("🎨 What place are you looking for? (e.g. park, museum, swimming pool)")
location = st.text_input("📍 Your City/Location:")

if st.button("🔍 Search Places"):
    if activity.strip() and location.strip():
        st.info("Searching nearby places...")

        url = f"https://nominatim.openstreetmap.org/search?format=json&q={activity} near {location}"
        headers = {"User-Agent": "ActivityBookingBuddyApp"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data:
                st.success(f"Found {len(data)} places!")

                for place in data[:10]:  # Show top 10
                    st.subheader(place.get("display_name"))
                    lat, lon = place.get("lat"), place.get("lon")
                    st.write(f"🌐 [View on Map](https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=16/{lat}/{lon})")
                    st.write("---")
            else:
                st.warning("No places found. Try another search.")
        else:
            st.error("Something went wrong. Try again later.")
    else:
        st.warning("Please enter both activity and location.")

st.caption("Built using Gemini + OpenStreetMap + Streamlit 🎈")
