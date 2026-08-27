import streamlit as st 

from backend.chatbot import chatbot

# Page config
st.set_page_config(
    page_title = "LangGaph chatbot",
    page_icon="🤖",
    )

st.title("🤖 LangGraph Chatbot")

# Session/conversation config

if "thread_id" not in st.session_state:
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
    if message.type == "human":

        with st.chat_message("user"):
            st.markdown(message.content)

    elif message.type == "ai":
        with st.chat_message("assistant"):
            st.markdown(message.content)


# User input

if prompt := st.chat_input("Ask me anything..."):

    # Display User message immedietley:
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream AI response
    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        full_response = ""

        for message_chunk, metadata in chatbot.stream(
            {
                "messages" : [
                    {
                        "role" : "user",
                        "content": prompt,
                    }
                ]
            },
            config=config,
            stream_mode="messages",
        ):

            # Only process AI messages
            if message_chunk.type == "AIMessageChunk":

                token = message_chunk.content

                if token:
                    full_response += token

                    response_placeholder.markdown(
                        full_response
                    )

