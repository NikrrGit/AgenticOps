from backend.chatbot import chatbot


config = {
    "configurable": {
        "thread_id": "test-thread"
    }
}


response = chatbot.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "What I am learning?"
            }
        ]
    },
    config=config,
)

print(response["messages"][-1].content)