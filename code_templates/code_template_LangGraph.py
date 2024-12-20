# Install Packages
# !pip install langgraph==0.2.4
# !pip install langchain-community==0.2.12
# !pip install langchain-openai==0.1.22
# !pip install langchain-experimental==0.0.64

from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage

# Placeholder to import tools and create tool list. Example:
# from tools.tool_x import tool_x
# from existing_agent_tool_library import tool_y
# …
# tool_list = [tool_x, tool_y, …]

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

class Agent:

    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)

        # Placeholder to create agent nodes and action nodes. Example:
        # graph.add_node("agent_node_1", self.call_agent_node_1_function)
        # graph.add_node("action_node_1", self.take_action_function)

        # Placeholder to create edges (simple edge and conditional edge). Example:
        # graph.add_conditional_edges(
        #     "agent_node",
        #     self.exists_action,
        #     {True: "action_node_1", False: END}
        # )
        # graph.add_edge("action_node_1", "agent_node_1")

        # Placeholder to set entry_point. Example:
        # graph.set_entry_point("agent_node_1")

        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    # Placeholder to define the function to call agent. Example:
    # def call_agent_node_1_function (self, state: AgentState):
    #     messages = state['messages']
    #     if self.system:
    #         messages = [SystemMessage(content=self.system)] + messages
    #     message = self.model.invoke(messages)
    #     return {'messages': [message]}

    def take_action_function (self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}

# Placeholder for system prompt. Example:
# prompt = """You are a smart building energy analysis. You can generate and debug code to do analysis and modeling based on users’ requests"""

# Placeholder to define LLM foundation model and setup API keys. Example:
# from langchain_openai import ChatOpenAI
# model = ChatOpenAI(model="gpt-3.5-turbo", api_key="...")

abot = Agent(model, tool_list, system=prompt)

# Placeholder to define LLM foundation model. Example:
# user_input = "Help me generate an energy usage trend line plots for the building data stored locally: data/building_data.csv"

messages = [HumanMessage(content= user_input)]
result = abot.graph.invoke({"messages": messages})