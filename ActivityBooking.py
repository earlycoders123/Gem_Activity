# app.py

import streamlit as st
import google.generativeai as genai
from langgraph.graph import StateGraph
from typing import TypedDict
import datetime

# ------------------ Gemini API Setup ------------------
genai.configure(api_key="AIzaSyDI5Hr2zxpxm3ZyfCGgO5iTWeAp_eprUaA")  # Replace with your actual Gemini key
model = genai.GenerativeModel("gemini-2.5-pro")

# ------------------ LangGraph State ------------------
class TravelState(TypedDict):
    location: str
    budget: str
    travel_date: str
    num_days: str
    itinerary: str

# ------------------ Agent Function ------------------
def itinerary_agent(state):
    location = state["location"]
    budget = state["budget"]
    travel_date = state["travel_date"]
    num_days = state["num_days"]

    prompt = f"""
    Plan a {num_days}-day fun and family-friendly itinerary to {location}, starting from {travel_date}.
    Keep it within a {budget} budget.
    Include exciting activities, meals, and unique experiences for each day.
    Make it engaging and easy to understand for kids.
    """

    itinerary = model.generate_content(prompt).text
    state["itinerary"] = itinerary
    return state

# ------------------ LangGraph Builder ------------------
def build_graph():
    builder = StateGraph(state_schema=TravelState)
    builder.add_node("ItineraryAgent", itinerary_agent)
    builder.set_entry_point("ItineraryAgent")
    builder.set_finish_point("ItineraryAgent")
    return builder.compile()

# ------------------ Streamlit UI ------------------
st.set_page_config(page_title="🧠 AI Travel Itinerary Planner", layout="centered")
st.title("🧳 AI Travel Booking Planner for Kids")

with st.form("travel_form"):
    col1, col2 = st.columns(2)
    location = col1.text_input("🌍 Where do you want to go?")
    budget = col2.selectbox("💰 What's your budget?", ["Low", "Medium", "High"])
    
    col3, col4 = st.columns(2)
    travel_date = col3.date_input("📅 Travel Start Date", value=datetime.date.today())
    num_days = col4.number_input("🔢 Number of Days", min_value=1, max_value=15, value=3)

    submitted = st.form_submit_button("✨ Plan My Itinerary")

if submitted:
    st.info("⏳ Planning your magical journey...")

    graph = build_graph()
    state = {
        "location": location,
        "budget": budget,
        "travel_date": travel_date.strftime("%Y-%m-%d"),
        "num_days": str(num_days),
    }

    result = graph.invoke(state)

    st.success("🎉 Here's your customized travel plan!")
    st.markdown(result["itinerary"])
