# workflow.py

import functools
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, AIMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from datetime import datetime
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.agents import tool


import operator

from agent.llm_utils import get_llm
from agent.mongodb_utils import vector_store
from config import MONGO_DB

@tool
def lookup_employees(query:str, n=10) -> str:
  "Gathers employee details from the database"
  result = vector_store.similarity_search_with_score(query=query, k=n)
  return str(result)

tools = [lookup_employees]

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage],operator.add]
    sender: str

def create_agent(llm, tools, system_message: str):
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful AI assistant, collaborating with other assistants."
                " Use the provided tools to progress towards answering the question."
                " If you are unable to fully answer, that's OK, another assistant with different tools "
                " will help where you left off. Execute what you can to make progress."
                " If you or any of the other assistants have the final answer or deliverable,"
                " prefix your response with FINAL ANSWER so the team knows to stop."
                " You have access to the following tools: {tool_names}.\n{system_message}."
                "\nCurrent time: {time}."
            ),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )
    prompt = prompt.partial(system_message=system_message)
    prompt = prompt.partial(time=lambda: str(datetime.now()))
    prompt = prompt.partial(tool_names=", ".join([tool.name for tool in tools]))

    return prompt | llm.bind_tools(tools)

def agent_node(state, agent, name):
    result = agent.invoke(state)
    if isinstance(result, ToolMessage):
        pass
    else:
        result = AIMessage(**result.dict(exclude={"type", "name"}), name=name)
    return {
        "messages": [result],
        "sender": name,
    }

chatbot_agent = create_agent(
    get_llm(),
    [lookup_employees],
    system_message="You are helpful HR Chabot Agent."
)

chatbot_node = functools.partial(agent_node, agent=chatbot_agent, name="HR Chatbot")

tool_node = ToolNode([lookup_employees], name="tools")


class WorkflowManager:
    def __init__(self, chatbot_node, tool_node):
        self.chatbot_node = chatbot_node
        self.tool_node = tool_node
        self.workflow = StateGraph(AgentState)
        
    def build_workflow(self):
        """Set up the workflow with nodes and edges."""
        self.workflow.add_node("chatbot", self.chatbot_node)
        self.workflow.add_node("tools", self.tool_node)
        self.workflow.set_entry_point("chatbot")
        self.workflow.add_conditional_edges(
            "chatbot",
            tools_condition,
            {"tools": "tools", END: END}
        )
        self.workflow.add_edge("tools", "chatbot")

    def compile_graph(self):
        """Compile and return the graph."""
        self.build_workflow()
        return self.workflow.compile()

workflow_manager = WorkflowManager(chatbot_node, tool_node)
graph = workflow_manager.compile_graph()