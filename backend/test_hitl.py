from langgraph.types import Command
from backend.chatbot   import chatbot

thread_id = "hitl-test-1"

config = {
    "configurable" : {
        "thread_id" : thread_id,
    }
}

# First Execution

result = chatbot.invoke(
    {
        "messages" : [
            {
                "role": "user",
                "content": "Ask a human for help with this question",
            }
        ]
    },
    config=config,
)S
print("\nInitial result:")
print(result)