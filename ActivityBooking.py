# app.py

# ----------------- Imports ------------------
import streamlit as st
import google.generativeai as genai
from langgraph.graph import StateGraph
from typing import TypedDict


# ----------------- Gemini Setup ------------------
genai.configure(api_key="AIzaSyDI5Hr2zxpxm3ZyfCGgO5iTWeAp_eprUaA")
model = genai.GenerativeModel('gemini-2.5-pro')

# Define schema for LangGraph state
class TravelState(TypedDict):
    user_input: str
    destination: str
    hotel_info: str
    transport_info: str
    itinerary: str

def suggest_destination(user_input):
    prompt = f"Suggest fun travel destinations based on: {user_input}"
    return model.generate_content(prompt).text

def book_hotel(destination):
    return f"Hotel booked in {destination}! (Simulated 🏨)"

def plan_transport(destination):
    return f"Travel route to {destination} planned! (Simulated 🚗)"

def build_itinerary(destination):
    return f"Here's your itinerary for {destination}:\n\n- Day 1: Arrival & Explore 🌆\n- Day 2: Adventure 🚣\n- Day 3: Relax & Return 🏖️"

# ----------------- LangGraph Nodes ------------------
def travel_planner_node(state):
    user_input = state["user_input"]
    destination = suggest_destination(user_input)
    state["destination"] = destination
    return state

def hotel_booking_node(state):
    state["hotel_info"] = book_hotel(state["destination"])
    return state

def transport_node(state):
    state["transport_info"] = plan_transport(state["destination"])
    return state

def itinerary_node(state):
    state["itinerary"] = build_itinerary(state["destination"])
    return state

# ----------------- LangGraph Flow ------------------
def build_graph():
    builder = StateGraph(state_schema=TravelState)
    builder.add_node("TravelPlanner", travel_planner_node)
    builder.add_node("HotelBooking", hotel_booking_node)
    builder.add_node("Transport", transport_node)
    builder.add_node("Itinerary", itinerary_node)

    builder.set_entry_point("TravelPlanner")
    builder.add_edge("TravelPlanner", "HotelBooking")
    builder.add_edge("HotelBooking", "Transport")
    builder.add_edge("Transport", "Itinerary")
    builder.set_finish_point("Itinerary")

    return builder.compile()

# ----------------- Streamlit UI ------------------
st.set_page_config(page_title="AI Travel Booking Planner")
st.title("✈️ AI Travel Booking Planner for Kids")

user_input = st.text_input("Where do you want to go? Tell us your travel dream:")

if st.button("Plan My Trip"):
    graph = build_graph()
    state = {"user_input": user_input}
    result = graph.invoke(state)

    st.success(f"🌍 Destination Suggestion:\n\n{result['destination']}")
    st.info(result["hotel_info"])
    st.info(result["transport_info"])
    st.write("🧳 **Your Travel Plan:**")
    st.write(result["itinerary"])
