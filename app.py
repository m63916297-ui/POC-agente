import os
import json
from typing import Annotated
from typing_extensions import TypedDict

from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import AnyMessage, add_messages
from langgraph.checkpoint.memory import MemorySaver

from tools import *
from prompt import *
from models_llm import *


# --- Estado compartido del grafo ---
class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


# --- Definición del Agente ---
class Agent:
    def __init__(self, model, tools, checkpointer, system_prompt):
        self.model = model
        self.tools = tools
        self.checkpointer = checkpointer
        self.system_prompt = system_prompt

        # Crear grafo de estados
        builder = StateGraph(State)
        builder.add_node("assistant", self.assistant)
        builder.add_node("tools_node", ToolNode(tools))

        builder.set_entry_point("assistant")
        builder.add_conditional_edges("assistant", tools_condition, {
            "tools": "tools_node",
            END: END
        })
        builder.add_edge("tools_node", "assistant")

        self.graph = builder.compile(checkpointer=checkpointer)

    # --- Nodo principal del agente ---
    def assistant(self, state: State):
        llm = self.model.bind_tools(self.tools)
        system_msg = SystemMessage(content=self.system_prompt)
        return {"messages": [llm.invoke([system_msg] + state["messages"])]}

    # --- Ejecución del grafo ---
    def run(self, text, conversation_id):
        config = {"configurable": {"thread_id": conversation_id}}
        result = self.graph.invoke({"messages": [text]}, config)
        return json.loads(result["messages"][-1].content)



memory = MemorySaver()

# --- Instancia del agente ---
agent_cesantias = Agent(
    model=modelo,
    tools=[validardoc, retreival_RAG],
    checkpointer=memory,
    system_prompt=assistant_prompt
)
