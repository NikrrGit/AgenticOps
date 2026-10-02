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
)
print("\nInitial result:")
print(result)


# Resume after human response

human_response = input("\nHuman response: ")

results = chatbot.invoke(
    Command(
        resume={
            "data": human_response,
        }
    ),
    config=config
)


print("\nFinal result:")
print(result)