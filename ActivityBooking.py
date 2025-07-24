# AI Travel Planner & Booker using LangGraph + Gemini + Streamlit

import streamlit as st
import google.generativeai as genai
from langgraph.graph import StateGraph

# Set your Gemini API key
genai.configure(api_key="AIzaSyDI5Hr2zxpxm3ZyfCGgO5iTWeAp_eprUaA")  # Replace with your actual API key

# 🧠 Step 1: Define how the agent will process your trip plan
def plan_trip(state):
    user_input = state["user_input"]

    prompt = f"""
    You're an expert AI travel planner. Help the user plan a trip with the following:
    - Destination: {user_input['place']}
    - Budget: {user_input['budget']}
    - Travel Date: {user_input['date']}

    Give them:
    - A fun trip plan (3-4 days if not specified)
    - Flight/train idea
    - Hotel recommendations
    - 2-3 local attractions
    - One cool tip or local dish to try
    """

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    trip_plan = response.text.strip()

    return {"result": trip_plan}

# 🗺️ Step 2: Define the graph state (what data flows through)
class State(dict):
    pass

# 🌐 Step 3: Build the LangGraph
builder = StateGraph(State)

# Add our single step node: TripPlanner
builder.add_node("TripPlanner", plan_trip)

# Entry and exit points of our graph
builder.set_entry_point("TripPlanner")
builder.set_finish_point("TripPlanner")

# Compile the graph
graph = builder.compile()

# 🎨 Step 4: Streamlit UI for user input
st.title("🌍 AI Travel Planner & Booker ✈️")
st.write("Plan your dream vacation in seconds!")

place = st.text_input("Enter destination:")
budget = st.text_input("Enter budget (in ₹ or $):")
date = st.date_input("Pick a travel date:")

if st.button("Plan My Trip"):
    if place and budget and date:
        user_input = {
            "user_input": {
                "place": place,
                "budget": budget,
                "date": str(date)
            }
        }

        # Run the LangGraph with input
        result = graph.invoke(user_input)
        st.success("✅ Trip Plan Ready!")
        st.markdown(result["result"])
    else:
        st.warning("Please fill all the fields above.")
