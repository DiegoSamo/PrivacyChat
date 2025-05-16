from dotenv import load_dotenv

load_dotenv()

from langchain_core.messages import HumanMessage
import os
from langgraph.graph import StateGraph
from schemas import MessagesState
from langgraph.checkpoint.memory import MemorySaver
from nodes import chat_node,random_node,ramdom_pathFinder,recognition_node,recognition_pathFinder

RECON="RecognitionAgent"
CHAT="ChatBotAgent"
RAMDOM="RandomizationAgent"

builder=StateGraph(MessagesState)
builder.add_node(RECON,recognition_node)
builder.add_node(RAMDOM,random_node)
builder.add_node(CHAT,chat_node)
builder.add_conditional_edges(RECON,recognition_pathFinder)
builder.add_conditional_edges(RAMDOM,ramdom_pathFinder)
builder.add_edge(CHAT,RAMDOM)
builder.set_entry_point(RECON)

memory = MemorySaver()
graph=builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "1"}}


if __name__ == "__main__":
    while True:
        text=input("Myself#>")
        if "/bye" in text:
            break
        inputMessage=HumanMessage(content=text)
        messages=graph.invoke({"messages":[inputMessage],"state":RECON},config=config)
        print("PrivacyChat#>"+messages["messages"][-1].content)


  

  