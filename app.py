import streamlit as st 
import uuid

from backend.chatbot import chatbot

# Page config
st.set_page_config(
    page_title="LangGraph chatbot",  # Fixed typo in "LangGraph"
    page_icon="🤖",
)

st.title("🤖 LangGraph Chatbot")

# Initialize conversation tracking
if "threads" not in st.session_state:
    st.session_state.threads = []
    new_thread_id = str(uuid.uuid4())
    st.session_state.threads.append(new_thread_id)
    st.session_state.thread_id = new_thread_id

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    },
    "metadata": {
        "environment": "development",
        "application": "agentic-chatbot",
    },
    "tags": [
        "streamlit",
        "development"
    ],
}

# Load existing state from LangGraph
state = chatbot.get_state(config)
# Safely handle if state or state.values is None
messages = state.values.get("messages", []) if state and state.values else []

# Display Conversation
for message in messages:
    # Use hasattr or lower() check since message types can sometimes be uppercase depending on the LangChain/LangGraph version
    if getattr(message, "type", "") == "human":
        with st.chat_message("user"):
            st.markdown(message.content)
    elif getattr(message, "type", "") == "ai":
        with st.chat_message("assistant"):
            st.markdown(message.content)

# User input
if prompt := st.chat_input("Ask me anything..."):

    # Display User message immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream AI response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        # Use chatbot.stream
        for message_chunk, metadata in chatbot.stream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ]
            },
            config=config,
            stream_mode="messages",
        ):
            
            if getattr(message_chunk, "type", "") in ["AIMessageChunk", "ai"]:
                token = message_chunk.content
                if token:
                    # LangGraph content tokens can sometimes arrive as a string or list of dicts (for tool calls)
                    if isinstance(token, str):
                        full_response += token
                        response_placeholder.markdown(full_response)

# Add new chat feature
with st.sidebar:
    st.header("Conversations")
    if st.button("➕ New Chat"):
        new_id = str(uuid.uuid4())
        st.session_state.threads.append(new_id)
        st.session_state.thread_id = new_id
        st.rerun()
