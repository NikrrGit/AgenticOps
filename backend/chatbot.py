import sqlite3
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain_core.messages import BaseMessage
from langchain_groq import ChatGroq
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import START, StateGraph
from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode, tools_condition


load_dotenv()

from backend.tools import tools


# SQL database
conn = sqlite3.connect(
    "chatbot.db",
    check_same_thread=False,
)
# LangGraph checkpointer
checkpointer = SqliteSaver(conn)

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)

llm_with_tools = llm.bind_tools(tools)

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}


tool_node = ToolNode(tools)
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)
graph.add_edge(START, "chat_node")

graph.add_conditional_edges(
    "chat_node",
    tools_condition,
)
graph.add_edge('tools', 'chat_node')


chatbot = graph.compile(checkpointer=checkpointer)
