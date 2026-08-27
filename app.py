import streamlit as st 

from backend.chatbot import chabt

# Page config
st.set_page_config(
    page_title = "LangGaph chatbot",
    page_icon="🤖",
    )

st.title("🤖 LangGraph Chatbot")

# Session/conversation config

if thread_id not in st.session_state:
    st.session_state.thread_id = "streamlit-session-1"

    config = {
        "configurable" : {
            "thread_id" : st.session_state.thread_id
        }
    }

# Load existing state from LanGraph

state = chatbot.get_state(config)
messages = state.values.get("messages", [])


# Dispalay Conversation
for message in messages:
    if message.type() == "human":

        with st.chat_message("user"):
            st.markdown(message.content)

    elif message.type() == "AI":
        with st.chat_message("assistance"):
            st.markdown(message.content)