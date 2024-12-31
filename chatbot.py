import streamlit as st
import requests
from streamlit_chat import message
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
LLAMA_URL = os.getenv("LLAMA_URL", "http://localhost:8000")  # Default fallback
GEN_RESPONSE_ENDPOINT = os.getenv("GEN_RESPONSE_ENDPOINT", "/gen_response")

# Function to send a request to the FastAPI server and get a response
def generate_response(conversation_history):
    try:
        response = requests.post(LLAMA_URL+GEN_RESPONSE_ENDPOINT, json={"conversation_history": conversation_history})
        response.raise_for_status()
        data = response.json()

        # Ensure the response is a string
        response_text = data.get("response", "No response received")
        if isinstance(response_text, str):
            return response_text
        else:
            return "Unexpected response format from the server."

    except requests.exceptions.RequestException as e:
        return f"Error: {e}"


# Title for the chatbot
st.title("Enhanced Pirate Chatbot: Streamlit + FastAPI (Llama3.2 Backend)")

# Initialize the conversation history
if "conversation_history" not in st.session_state:
    st.session_state["conversation_history"] = [
        {"role": "system", "content": "You are a pirate chatbot. Respond in 50 words or less. Make controversial statements."}
    ]

# User input section
user_input = st.text_input("Enter your message:")

# "Send" button to submit input
if st.button("Send"):
    if user_input.strip():
        # Add the user's input to the conversation history
        st.session_state["conversation_history"].append({"role": "user", "content": user_input})

        # Generate a response using the FastAPI backend
        output = generate_response(st.session_state["conversation_history"])

        # Check if the response is valid
        if isinstance(output, str) and output.startswith("Error:"):
            st.error(output)
        elif isinstance(output, str):
            # Add the assistant's response to the conversation history
            st.session_state["conversation_history"].append({"role": "assistant", "content": output})
        else:
            st.error(f"Unexpected response format: {output}")


# Display the conversation history
st.subheader("Chat Interface")
for msg in st.session_state["conversation_history"]:
    if msg["role"] == "assistant":
        message(msg["content"], key=str(st.session_state["conversation_history"].index(msg)))
    elif msg["role"] == "user":
        message(msg["content"], is_user=True, key=str(st.session_state["conversation_history"].index(msg)) + "_user")

# Option to display raw conversation history for debugging
if st.checkbox("Show raw conversation history (debug)"):
    st.subheader("Raw Conversation History")
    st.json(st.session_state["conversation_history"])
