from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
import streamlit as st

load_dotenv()

st.title("Agentic chatbot with Langgraph")

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    return {"messages": [llm.invoke(state["messages"])]}


llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)
chatbot = graph.compile(checkpointer=MemorySaver())

CONFIG = {'configurable': {'thread_id':'thread_1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Laoding the conevrsation history

for message in st.session_state['message_history']:
    with st.chat_message(message["role"]):
        st.text(message['content'])


user_input = st.chat_input('Type here')

if user_input:
    # first add the message to message_history
    st.session_state["message_history"].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)

    ai_message = response['messages'][-1].content
    # add the message to the message histroy
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
    with st.chat_message("assistant"):
        st.text(ai_message)
