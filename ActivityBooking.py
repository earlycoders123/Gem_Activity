# --- Imports ---
import streamlit as st
from langgraph.graph import StateGraph
import google.generativeai as genai
from datetime import date

# --- Gemini API Key ---
genai.configure(api_key="YOUR_API_KEY_HERE")  # Replace with your Gemini API Key
model = genai.GenerativeModel("gemini-2.5-pro")

# --- Agent Functions ---

def extract_user_intent(state):
    return {
        "location": state["location"],
        "budget": state["budget"],
        "days": state["days"],
        "date": state["date"]
    }

def suggest_places(state):
    location = state["location"]
    prompt = f"Suggest top 5 family-friendly tourist attractions in {location} with short descriptions."
    response = model.generate_content(prompt)
    return {**state, "places": response.text}

def suggest_budget_options(state):
    raw_budget = str(state["budget"]).lower().replace(",", "").strip()

    # Convert to number
    if "lakh" in raw_budget:
        try:
            number_part = float(raw_budget.split("lakh")[0].strip())
            budget = int(number_part * 100000)
        except:
            budget = 0
    elif "k" in raw_budget:
        try:
            number_part = float(raw_budget.replace("k", ""))
            budget = int(number_part * 1000)
        except:
            budget = 0
    else:
        try:
            budget = int(raw_budget)
        except:
            budget = 0

    state["numeric_budget"] = budget

    # Suggestion
    if budget < 10000:
        options = "🏕️ Budget stay, street food, shared transport."
    elif budget < 30000:
        options = "🏨 3-star hotels, local restaurants, guided tours."
    elif budget < 100000:
        options = "🏝️ Luxury hotels, private tours, domestic flights."
    else:
        options = "🛳️ Premium vacation with concierge and custom experiences."

    return {**state, "budget_tips": options}

def recommend_hotels(state):
    location = state["location"]
    budget = state["numeric_budget"]

    prompt = f"""
    Recommend 3 good hotels in {location} for a family trip.
    Budget is around ₹{budget}. Include hotel name, price per night, and a short description.
    """
    response = model.generate_content(prompt)
    return {**state, "hotels": response.text}

def create_itinerary(state):
    location = state["location"]
    days = int(state["days"])

    prompt = f"""
    Create a unique {days}-day itinerary for a family trip to {location}.
    Each day should include morning, afternoon, and evening activities.
    Highlight fun, food, culture, and relaxation.
    """
    response = model.generate_content(prompt)
    return {**state, "itinerary": response.text}

def generate_checklist(state):
    checklist = (
        "✅ Travel Checklist:\n"
        "- ID proof & tickets\n"
        "- Clothes & toiletries\n"
        "- Comfortable shoes\n"
        "- Phone & charger\n"
        "- Emergency medicines\n"
        "- Sunglasses, sunscreen\n"
        "- Power bank & snacks\n"
    )
    return {**state, "checklist": checklist}

# --- LangGraph Setup ---
state_schema = dict
builder = StateGraph(state_schema)

builder.add_node("UserIntent", extract_user_intent)
builder.add_node("DestinationAgent", suggest_places)
builder.add_node("BudgetAgent", suggest_budget_options)
builder.add_node("HotelAgent", recommend_hotels)
builder.add_node("ItineraryAgent", create_itinerary)
builder.add_node("ChecklistAgent", generate_checklist)

builder.set_entry_point("UserIntent")
builder.add_edge("UserIntent", "DestinationAgent")
builder.add_edge("DestinationAgent", "BudgetAgent")
builder.add_edge("BudgetAgent", "HotelAgent")
builder.add_edge("HotelAgent", "ItineraryAgent")
builder.add_edge("ItineraryAgent", "ChecklistAgent")
builder.set_finish_point("ChecklistAgent")

travel_graph = builder.compile()

# --- Streamlit Frontend ---
st.set_page_config(page_title="AI Travel Planner", page_icon="🌍")
st.title("🌍 AI Travel Booking Planner (Agentic AI)")
st.markdown("Let **Agentic AI** plan your dream trip with smart itineraries and hotel suggestions!")

with st.form("travel_form"):
    location = st.text_input("📍 Enter Destination:")
    budget = st.text_input("💸 Enter Budget (e.g., 5 lakhs, 30000):")
    days = st.number_input("📅 Number of Days:", min_value=1, max_value=15, step=1)
    date_plan = st.date_input("🗓️ Start Date", min_value=date.today())
    submitted = st.form_submit_button("🚀 Plan My Trip")

if submitted:
    state = {
        "location": location,
        "budget": budget,
        "days": days,
        "date": str(date_plan)
    }

    st.info("⏳ Letting Agentic AI craft your trip...")
    result = travel_graph.invoke(state)

    st.success("✅ Trip Planned Successfully!")

    st.subheader("📌 Top Places to Visit")
    st.markdown(result["places"])

    st.subheader("🏨 Hotel Recommendations")
    st.markdown(result["hotels"])

    st.subheader("💰 Budget Suggestions")
    st.markdown(result["budget_tips"])

    st.subheader("🗓️ Day-wise Itinerary")
    st.code(result["itinerary"], language="markdown")

    st.subheader("📋 Travel Checklist")
    st.code(result["checklist"], language="markdown")
