# LangChain
from langchain_core.messages import AnyMessage, SystemMessage, ToolMessage

# LangGraph
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver


# General
import operator
from typing import TypedDict, Annotated
from IPython.display import Image, display

class AgentState(TypedDict):
  conversation: Annotated[list[AnyMessage], operator.add]

class Agent:
  def __init__(self, model, tools, system_prompt):

    self.model = model.bind_tools(tools)
    self.system_prompt = system_prompt
    self.tools = {tool.name: tool for tool in tools}

    memory = MemorySaver()

    graph = StateGraph(state_schema=AgentState)
    
    graph.add_node('LLM', self.use_model)
    graph.add_node('ToolBox', self.use_tools)

    graph.add_conditional_edges('LLM', self.validate_tools, {True:'ToolBox', False: END})
    graph.add_edge('ToolBox', 'LLM')
    graph.set_entry_point('LLM')

    self.graph = graph.compile(checkpointer=memory)
    display(Image(self.graph.get_graph().draw_mermaid_png()))
  
  ## Talk to the model
  def use_model(self, state: AgentState):

    messages = [SystemMessage(content=self.system_prompt)] + state['conversation']
    ai_response = self.model.invoke(messages)

    return {'conversation': [ai_response]}
  
  ## Checks if model wants to use tools
  def validate_tools(self, state: AgentState):
    if len(state['conversation'][-1].tool_calls) > 0:
      return True
    else:
      return False
  
  ## Checks if tools exist. If yes, uses them. Otherwise, tells the LLM to retry
  def use_tools(self, state: AgentState):
    
    tool_calls = state['conversation'][-1].tool_calls
    results = []
  
    for tool in tool_calls:
      # Use the tool
      if tool['name'] in self.tools:
        print(f"---- Calling: {tool['name']}")
        result = self.tools[tool['name']].invoke(tool['args'])

      # Tell the LLM to retry    
      else:
        print(f"---- Error, tool name not found: {tool['name']}")
        result = "tool name not found in list of tools. retry your tool use."

      # Save the returned output
      results.append(ToolMessage(name=tool['name'], tool_call_id=tool['id'], content=str(result)))

    return {'conversation': results}
  