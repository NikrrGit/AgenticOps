# from backend.chatbot import chatbot


# config = {
#     "configurable": {
#         "thread_id": "test-thread"
#     }
# }


# response = chatbot.invoke(
#     {
#         "messages": [
#             {
#                 "role": "user",
#                 "content": "I am learning Cuda for infrence"
#             }
#         ]
#     },
#     config=config,
# )

# print(response)

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
                "content": "What am I learning for infrence?"
            }
        ]
    },
    config=config,
)

print(response["messages"][-1].content)