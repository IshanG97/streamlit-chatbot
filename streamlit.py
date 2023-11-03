import streamlit as st
from streamlit_chat import message

import parse_api_key
import openai

def setup_env(key):
    #openai.api_key = st.secrets["api_secret"] # store your API key in a secrets.toml file
    if key == "openai":
        openai.api_key = parse_api_key.load_api_key("OPENAI_KEY")
    elif key == "anthropic":
        openai.api_key = parse_api_key.load_api_key("ANTHROPIC_KEY")

def setup_ui():
    st.set_page_config(layout="centered")

    # Add title
    #st.title("Jarvis")

    # Add logo with centered layout
    #st.image("assets/logo.jpeg", width=200)
    #st.markdown(
    #    """
    #    <div style="text-align: center">
    #        <img src="assets/jarvis.html" width="200">
    #    </div>
    #    """,
    #    unsafe_allow_html=True,
    #)

    with open("assets/jarvis.html", "r") as f:
        html_string = f.read()

    st.markdown(html_string, unsafe_allow_html=True)

    st.write("Hi, I'm Jarvis, a bot that aims to help you resolve your customer service query.")

def openai_response(prompt):
    completions = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1024,
        n = 1,
        stop = None,
        temperature=0.5,
    )
    message = completions.choices[0].text
    return message

def langchain_response(prompt):
    ###

    ###
    return "Langchain response"

# Get the user's input
def get_text():
    user_input = st.text_input("How can I help you today?", "")
    #user_input = st.text_input("You: ","How can I help you today?", key="input")
    return user_input

if __name__ == "__main__":
    llm_model = "openai" #or "anthropic"
    setup_env(llm_model)
    setup_ui()

    # Initialize chat history
    if 'bot_history' not in st.session_state:
        st.session_state['bot_history'] = []
    if 'user_history' not in st.session_state:
        st.session_state['user_history'] = []

    user_input = get_text()

    if st.button("Send"):
        # Append user input and bot response to chat history
        if llm_model == "openai":
            chatbot_response = openai_response(user_input)
        elif llm_model == "anthropic":
            chatbot_response = langchain_response(user_input)
        #st.session_state.user_history.append(f"You: {user_input}")
        #st.session_state.bot_history.append(f"Jarvis: {response}")
        st.session_state.user_history.append(user_input)
        st.session_state.bot_history.append(chatbot_response)

        # Display chat history
        #for chat in st.session_state['chat_history']:
        #    st.text(chat)
        if st.session_state.bot_history:
            for i in range(len(st.session_state.bot_history)-1, -1, -1):
                message(st.session_state.bot_history[i], key=str(i))
                message(st.session_state.user_history[i], is_user=True, key=str(i) + '_user')