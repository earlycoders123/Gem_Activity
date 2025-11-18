import streamlit as st
from langgraph.graph import StateGraph

st.set_page_config(page_title="Friendly LangGraph ChatBot")
st.title("Friendly LangGraph ChatBot")

if "step" not in st.session_state:
  st.session_state.step = "greet"
if "name" not in st.session_state:
  st.session_state.name = ""

def greet(state):
  st.success("Hello! Welcome to our session")
  return state

def ask_name(state):
  name = st.text_input("What is your name?",key="name_input")
  if name:
    state["name"] = name
  return state  

def goodbye(state):
  if state.get("name"):
    st.success(f"Good bye! {state['name']}! Have a lovely Day!")
  else:
    st.success("Good bye! Have a lovely Day!")
  return state 

state_schema = dict
graph = StateGraph(state_schema) #craeted a blank graph
graph.add_node("greet",greet)  
graph.add_node("ask_name",ask_name)
graph.add_node("goodbye",goodbye)

graph.set_entry_point("greet")
graph.add_edge("greet","ask_name")
graph.add_edge("ask_name","goodbye")

chatbot = graph.compile()

state = {"name":st.session_state.name}

if st.session_state.step == "greet":
  chatbot.invoke({"name":""})
  if st.button("Start chatting"):
    st.session_state.step = "ask_name"

elif st.session_state.step == "ask_name": 
  chatbot.invoke({"name":st.session_state.name}) 
  if st.text_input("Type your name again to continue",key="final_input"):
    st.session_state.step = "goodbye"

elif st.session_state.step == "goodbye": 
  chatbot.invoke({"name":st.session_state.name}) 
  if st.button("Restart"):
    st.session_state.step = "greet" 
    st.session_state.name = ""    


