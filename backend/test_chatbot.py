from backend.chatbot import chatbot

config = { 
    "configurable": {
        "thread_id" : "test_thread"
    }
}

response = chatbot.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": "I am learning cuda"
            }
        ]
    },
    config=config
)

print(response)
