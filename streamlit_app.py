import streamlit as st
import requests

# =========================
# CONFIG
# =========================
API_URL = "http://localhost:8000/chat"  
# For deployment, we will change this later

st.set_page_config(
    page_title="Loan-Agent | NBFC Personal Loan Assistant",
    page_icon="🤖",
    layout="centered"
)

# =========================
# SESSION STATE
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_data" not in st.session_state:
    st.session_state.user_data = {
        "income": 30000,
        "credit_score": 780,
        "kyc_done": True
    }

# =========================
# UI
# =========================
st.title("🤖 Loan-Agent")
st.subheader("AI-powered Personal Loan Assistant")

st.markdown(
    """
    Welcome! I can help you check eligibility, assess risk, and apply for a personal loan.
    """
)

# =========================
# CHAT DISPLAY
# =========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# =========================
# USER INPUT
# =========================
user_input = st.chat_input("Type your message here...")

if user_input:
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call FastAPI backend
    response = requests.post(
        API_URL,
        json={
            "message": user_input,
            "user_data": st.session_state.user_data
        }
    )

    if response.status_code == 200:
        agent_reply = response.json()["reply"]
    else:
        agent_reply = "⚠️ Sorry, something went wrong."

    # Show agent reply
    st.session_state.messages.append({
        "role": "assistant",
        "content": agent_reply
    })

    with st.chat_message("assistant"):
        st.markdown(agent_reply)
