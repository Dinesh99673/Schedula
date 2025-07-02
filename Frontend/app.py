import streamlit as st
import requests

st.title("🧵 TailorTalk: Appointment Assistant")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("""
📅 [📖 View Calendar](https://calendar.google.com/calendar/embed?src=a0d154558211246ed1397ca00f91f66b2bc057f54832ce82f427266d971142c4@group.calendar.google.com)
""", unsafe_allow_html=True)

user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state.chat_history.append(("You", user_input))
    res = requests.post("https://schedula-fm3p.onrender.com/chat", json={"message": user_input})
    
    # Print raw response for debugging
    st.write("🔁 RAW RESPONSE:", res.text)
    st.write("✅ STATUS CODE:", res.status_code)

    if res.status_code == 200:
        reply = res.json().get("response")
    else:
        reply = "❌ Error from server. Please check backend logs."
    
    st.session_state.chat_history.append(("Bot", reply))


for sender, msg in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {msg}")
