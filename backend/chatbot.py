from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages

import sqlite3 
from langgraph.checkpoint.sqlite import SqliteSaver

from backend.tools import tools

# Sql DB 
conn = sqlite3.connect(
    "chatbot.db",
    check_same_thread=False,
)
# Langgraph CheckPointer
checkpointer = SqliteSaver(conn)


load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    messages = state['messages']
    response = llm_with_tools(state["messages"])
    return {"messages": [response]}

tool_node = ToolNode(tools)
checkpoint = MemorySaver()
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "chat_node")

graph.add_conditional_edges(
    "chat_node",
    tools_condition,
)
graph.add_edge('tools', 'chat_node')


chatbot = graph.compile(checkpointer=checkpoint)
