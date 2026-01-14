from PIL import Image
import streamlit as st
import requests
import uuid

API_BASE = "http://127.0.0.1:8000"

# -----------------------
# Session state
# -----------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# Page UI
# -----------------------
st.set_page_config(page_title="Bhagavad Gita Assistant", page_icon="🕉️")

st.image(Image.open("assets/krishna_arjuna.jpeg"), use_container_width=True)

st.title("🕉️ Bhagavad Gita Chatbot")
st.caption("LangGraph-powered • Grounded in Bhagavad Gita (TTD)")

# -----------------------
# Display chat history
# -----------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------
# Chat input
# -----------------------
prompt = st.chat_input("Ask something about the Bhagavad Gita...")

if prompt:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call backend
    response = requests.post(
        f"{API_BASE}/chat",
        json={
            "message": prompt,
            "session_id": st.session_state.session_id
        }
    )

    data = response.json()

    # -----------------------
    # Extract reply safely
    # -----------------------
    reply = (
        data.get("answer")
        or data.get("verse")
        or "No response generated."
    )

    confidence = data.get("confidence", 0)

    formatted = f"{reply}\n\n🧠 Confidence: {confidence}%"

    # Store + render assistant
    st.session_state.messages.append({
        "role": "assistant",
        "content": formatted
    })

    with st.chat_message("assistant"):
        st.markdown(reply)
        st.caption(f"🧠 Confidence: {confidence}%")
