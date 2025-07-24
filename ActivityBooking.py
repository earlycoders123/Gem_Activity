# app.py

# ----------------- Imports ------------------
import streamlit as st
import google.generativeai as genai
from langgraph.graph import StateGraph
from typing import TypedDict

# ----------------- API Setup ------------------
genai.configure(api_key="AIzaSyDI5Hr2zxpxm3ZyfCGgO5iTWeAp_eprUaA")  # Replace with your actual Gemini API key
model = genai.GenerativeModel('gemini-2.5-pro')

# ----------------- State Schema ------------------
class TravelState(TypedDict):
    user_input: str
    destination: str
    budget: str
    hotel: str
    transport: str
    itinerary: str

# ----------------- Agent Functions ------------------

def destination_agent(state):
    user_input = state["user_input"]
    prompt = f"Suggest a destination based on: {user_input}"
    destination = model.generate_content(prompt).text
    state["destination"] = destination
    return state

def budget_agent(state):
    destination = state["destination"]
    prompt = f"Estimate the budget needed to travel to {destination}"
    budget = model.generate_content(prompt).text
    state["budget"] = budget
    return state

def hotel_agent(state):
    destination = state["destination"]
    prompt = f"Suggest a hotel in {destination} with good reviews and budget-friendly"
    hotel = model.generate_content(prompt).text
    state["hotel"] = hotel
    return state

def transport_agent(state):
    destination = state["destination"]
    prompt = f"Suggest a travel mode to reach {destination} from user's city"
    transport = model.generate_content(prompt).text
    state["transport"] = transport
    return state

def itinerary_agent(state):
    destination = state["destination"]
    prompt = f"Plan a 3-day itinerary for {destination}"
    itinerary = model.generate_content(prompt).text
    state["itinerary"] = itinerary
    return state

# ----------------- LangGraph Setup ------------------

def build_graph():
    builder = StateGraph(state_schema=TravelState)
    builder.add_node("Destination", destination_agent)
    builder.add_node("Budget", budget_agent)
    builder.add_node("Hotel", hotel_agent)
    builder.add_node("Transport", transport_agent)
    builder.add_node("Itinerary", itinerary_agent)

    builder.set_entry_point("Destination")
    builder.add_edge("Destination", "Budget")
    builder.add_edge("Budget", "Hotel")
    builder.add_edge("Hotel", "Transport")
    builder.add_edge("Transport", "Itinerary")
    builder.set_finish_point("Itinerary")

    return builder.compile()

# ----------------- Streamlit UI ------------------

st.set_page_config(page_title="🧠 AI Travel Booking Planner")
st.title("🗺️ Agentic AI Travel Booking Planner")

user_input = st.text_input("Tell me your dream travel idea (with location, interests, etc):")

if st.button("Plan My Trip"):
    graph = build_graph()
    state = {"user_input": user_input}
    result = graph.invoke(state)

    st.subheader("🌍 Suggested Destination")
    st.write(result["destination"])

    st.subheader("💰 Estimated Budget")
    st.write(result["budget"])

    st.subheader("🏨 Hotel Suggestion")
    st.write(result["hotel"])

    st.subheader("🚗 Travel Mode")
    st.write(result["transport"])

    st.subheader("🧳 Itinerary")
    st.write(result["itinerary"])
