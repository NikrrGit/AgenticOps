import uuid

import streamlit as st

from backend.chatbot import chatbot


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="LangGraph Chatbot",
    page_icon="🤖",
)

st.title("🤖 LangGraph Chatbot")


# ============================================================
# Session State Initialization
# ============================================================

if "threads" not in st.session_state:
    st.session_state.threads = []


if "thread_id" not in st.session_state:
    thread_id = str(uuid.uuid4())

    st.session_state.threads.append(thread_id)
    st.session_state.thread_id = thread_id


# ============================================================
# Thread Management
# ============================================================

def create_thread():
    """
    Create a new conversation thread and make it active.
    """

    thread_id = str(uuid.uuid4())

    st.session_state.threads.append(thread_id)
    st.session_state.thread_id = thread_id


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("Conversations")

    # New conversation
    if st.button(
        "➕ New Chat",
        use_container_width=True,
    ):
        create_thread()
        st.rerun()

    st.divider()

    # Existing conversations
    for index, thread_id in enumerate(st.session_state.threads):

        is_current = thread_id == st.session_state.thread_id

        label = f"Chat {index + 1}"

        if st.button(
            label,
            key=f"thread_{thread_id}",
            use_container_width=True,
            type="primary" if is_current else "secondary",
        ):
            st.session_state.thread_id = thread_id
            st.rerun()


# ============================================================
# LangGraph Configuration
# ============================================================

config = {
    "configurable": {
        "thread_id": st.session_state.thread_id,
    },
    "metadata": {
        "environment": "development",
        "application": "agentic-chatbot",
    },
    "tags": [
        "streamlit",
        "development",
    ],
}


# ============================================================
# Load Existing Conversation
# ============================================================

state = chatbot.get_state(config)

messages = (
    state.values.get("messages", [])
    if state and state.values
    else []
)


# ============================================================
# Display Conversation
# ============================================================

for message in messages:

    message_type = getattr(message, "type", "")

    if message_type == "human":

        with st.chat_message("user"):
            st.markdown(message.content)

    elif message_type == "ai":

        with st.chat_message("assistant"):

            # Some AI messages can contain structured content.
            # For normal text responses, display directly.
            if isinstance(message.content, str):
                st.markdown(message.content)


# ============================================================
# User Input
# ============================================================

if prompt := st.chat_input("Ask me anything..."):

    # --------------------------------------------------------
    # Display user message immediately
    # --------------------------------------------------------

    with st.chat_message("user"):
        st.markdown(prompt)


    # --------------------------------------------------------
    # Stream AI response
    # --------------------------------------------------------

    with st.chat_message("assistant"):

        response_placeholder = st.empty()

        full_response = ""


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

            message_type = getattr(
                message_chunk,
                "type",
                "",
            )

            # We only want AI message chunks.
            if message_type in ["AIMessageChunk", "ai"]:

                token = message_chunk.content

                # Normal text token
                if isinstance(token, str) and token:

                    full_response += token

                    response_placeholder.markdown(
                        full_response
                    )