# AI Travel Planner & Booker using LangGraph + Gemini + Streamlit
# This simplified agentic AI helps users plan trips (place, date, budget, etc.)
# We'll use Gemini for responses, LangGraph for workflow logic, Streamlit for UI

import streamlit as st
import google.generativeai as genai
import os

# ------------------ CONFIGURATION ------------------
# Set your Gemini API key from Google
# Visit https://aistudio.google.com/app/apikey to get your key
genai.configure(api_key="AIzaSyDI5Hr2zxpxm3ZyfCGgO5iTWeAp_eprUaA")
model = genai.GenerativeModel("gemini-2.5-pro")

# ------------------ LangGraph STATE SIMULATION ------------------
# We'll simulate LangGraph state using session_state
if 'step' not in st.session_state:
    st.session_state.step = 'get_input'  # Starting point
if 'travel_data' not in st.session_state:
    st.session_state.travel_data = {}

# ------------------ STREAMLIT UI ------------------
st.title("🌍 AI Travel Planner & Booker")
st.markdown("Plan your dream trip with the help of AI agents!")

# 1. Step 1: Get destination, dates, budget
if st.session_state.step == 'get_input':
    with st.form("trip_form"):
        destination = st.text_input("Where do you want to go?")
        dates = st.text_input("When are you planning your trip?")
        budget = st.text_input("What's your budget?")
        submitted = st.form_submit_button("Next")

    if submitted and destination and dates and budget:
        st.session_state.travel_data = {
            "destination": destination,
            "dates": dates,
            "budget": budget
        }
        st.session_state.step = 'ai_recommendation'

# 2. Step 2: AI recommends travel plans
elif st.session_state.step == 'ai_recommendation':
    with st.spinner("Planning your trip with AI magic..."):
        prompt = f"Plan a trip to {st.session_state.travel_data['destination']} on {st.session_state.travel_data['dates']} within a budget of {st.session_state.travel_data['budget']}. Include flight, hotel and 3 things to do."
        response = model.generate_content(prompt)
        st.session_state.ai_plan = response.text
        st.session_state.step = 'show_plan'

# 3. Step 3: Show AI travel plan
elif st.session_state.step == 'show_plan':
    st.subheader("Your Travel Itinerary")
    st.markdown(st.session_state.ai_plan)
    if st.button("Book Now (Simulated)"):
        st.session_state.step = 'booked'

# 4. Step 4: Confirmation
elif st.session_state.step == 'booked':
    st.success("🌟 Your trip is booked! (Not really, but we can dream!)")
    st.balloons()
    if st.button("Plan Another Trip"):
        st.session_state.step = 'get_input'
        st.session_state.travel_data = {}

# ------------------ Notes for Kids ------------------
# - st.session_state keeps track of what step you're on, like memory.
# - gemini-pro is our smart AI that helps write travel plans.
# - We use `model.generate_content(prompt)` to get answers from Gemini.
# - Streamlit forms let us collect input like destination and budget.
# - Each step has its own section, just like a choose-your-own-adventure!

# ------------------ Hosting Tips ------------------
# - Save as travel_planner.py
# - Run using: `streamlit run travel_planner.py`
# - Upload to GitHub
# - Deploy on Streamlit Cloud or Colab with ngrok for public use
