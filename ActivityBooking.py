import streamlit as st
import google.generativeai as genai

# Step 1: Configure Gemini API Key
genai.configure(api_key="AIzaSyDI5Hr2zxpxm3ZyfCGgO5iTWeAp_eprUaA")

# Step 2: Load Gemini Model
model = genai.GenerativeModel('gemini-2.5-pro')

# Step 3: Dummy dataset of activities (replace with real data later)
activities = {
    "art": "🎨 Art Class at Rainbow Arts Center - [Book Now](https://example.com/art-class)",
    "football": "⚽ Football Coaching at Sports Hub - [Book Now](https://example.com/football)",
    "dance": "💃 Dance Workshop at Star Studio - [Book Now](https://example.com/dance)",
    "music": "🎸 Music Lessons at Melody Academy - [Book Now](https://example.com/music)"
}

# Step 4: Streamlit UI Setup
st.set_page_config(page_title="🎉 Kids Activity Booking Buddy")
st.title("🎉 Kids Activity Booking Buddy")
st.write("Tell me what fun activity you'd like to join, and I'll help you book it!")

# Step 5: Get User Query
user_input = st.text_input("🎈 What activity are you looking for? (Example: I want football classes)")

# Step 6: AI Processing & Response
if st.button("🎟️ Find Activities"):
    if user_input.strip():
        with st.spinner("Finding activities for you..."):
            # Gemini generates structured response
            prompt = f"""
            A child said: {user_input}.
            Which activity matches this from: {list(activities.keys())}?
            Reply with just the key like art, football, dance, or music.
            """
            response = model.generate_content(prompt)
            detected_activity = response.text.strip().lower()

            if detected_activity in activities:
                st.success("🎉 Here's something fun for you!")
                st.markdown(activities[detected_activity], unsafe_allow_html=True)
            else:
                st.warning("Oops! I couldn't find a matching activity. Please try again.")
    else:
        st.warning("Please type something first.")

st.caption("Made with ❤️ using Gemini AI and Streamlit.")
