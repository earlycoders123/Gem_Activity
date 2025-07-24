# --- Imports ---
import streamlit as st
from langgraph.graph import StateGraph
import google.generativeai as genai
from datetime import date

# --- Gemini API Key ---
genai.configure(api_key="AIzaSyDI5Hr2zxpxm3ZyfCGgO5iTWeAp_eprUaA")
model = genai.GenerativeModel("gemini-2.5-pro")

# --- Agent Functions ---

# 1. Extract user input
def extract_user_intent(state):
    return {
        "location": state["location"],
        "budget": state["budget"],
        "days": state["days"],
        "date": state["date"]
    }

# 2. Suggest places using Gemini
def suggest_places(state):
    location = state["location"]
    prompt = f"Suggest top 5 tourist attractions in {location} for a family trip."
    response = model.generate_content(prompt)
    return {**state, "places": response.text}

# 3. Budget advice agent
def suggest_budget_options(state):
    budget = int(state["budget"])
    if budget < 10000:
        options = "Budget stay, street food, shared transport."
    elif budget < 30000:
        options = "3-star hotels, local restaurants, guided tours."
    else:
        options = "Luxury hotels, fine dining, private cabs."
    return {**state, "budget_tips": options}

# 4. Itinerary planner
def create_itinerary(state):
    days = int(state["days"])
    itinerary = ""
    for i in range(1, days + 1):
        itinerary += f"Day {i}:\n - Morning: Visit local attractions\n - Afternoon: Lunch & shopping\n - Evening: Explore culture\n\n"
    return {**state, "itinerary": itinerary}

# 5. Checklist generator
def generate_checklist(state):
    checklist = (
        "✅ Travel Checklist:\n"
        "- ID proof & tickets\n"
        "- Clothes & toiletries\n"
        "- Comfortable shoes\n"
        "- Phone & charger\n"
        "- Emergency medicines\n"
        "- Sunglasses, sunscreen\n"
    )
    return {**state, "checklist": checklist}

# --- LangGraph Setup ---
state_schema = dict  # basic dict for state
builder = StateGraph(state_schema)

# Add all agent nodes
builder.add_node("UserIntent", extract_user_intent)
builder.add_node("DestinationAgent", suggest_places)
builder.add_node("BudgetAgent", suggest_budget_options)
builder.add_node("ItineraryAgent", create_itinerary)
builder.add_node("ChecklistAgent", generate_checklist)

# Set flow of graph
builder.set_entry_point("UserIntent")
builder.add_edge("UserIntent", "DestinationAgent")
builder.add_edge("DestinationAgent", "BudgetAgent")
builder.add_edge("BudgetAgent", "ItineraryAgent")
builder.add_edge("ItineraryAgent", "ChecklistAgent")
builder.set_finish_point("ChecklistAgent")

# Compile the graph
travel_planner_graph = builder.compile()

# --- Streamlit Frontend ---
st.set_page_config(page_title="AI Travel Planner", page_icon="✈️")
st.title("✈️ AI Travel Booking Planner")
st.markdown("Let AI plan your next amazing trip!")

with st.form("travel_form"):
    location = st.text_input("Enter your destination:")
    budget = st.text_input("Enter your budget (INR):")
    date_plan = st.date_input("Planning start date", min_value=date.today())
    days = st.number_input("Number of days:", min_value=1, max_value=30, step=1)
    submitted = st.form_submit_button("Plan My Trip")

if submitted:
    state = {
        "location": location,
        "budget": budget,
        "date": str(date_plan),
        "days": days
    }

    st.info("⏳ Generating your travel plan...")
    result = travel_planner_graph.invoke(state)

    # Output
    st.success("✅ Trip planned successfully!")

    st.subheader("📍 Places to Visit")
    st.write(result["places"])

    st.subheader("💰 Budget Suggestions")
    st.write(result["budget_tips"])

    st.subheader("🗓️ Itinerary Plan")
    st.code(result["itinerary"])

    st.subheader("📋 Travel Checklist")
    st.code(result["checklist"])
