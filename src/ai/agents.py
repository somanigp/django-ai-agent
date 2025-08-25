from langgraph.prebuilt import create_react_agent  # React here is just a type of ai agent
from ai.llms import get_google_model
from ai.tools import (  # Use () for readability
    document_tools
)

def get_document_agent(model=None, checkpointer=None):
    llm_model = get_google_model(model=model)
    
    agent = create_react_agent(
        model=llm_model,
        tools=document_tools,
        prompt="You are a helpful assistant in managing a User's documents within this app", # prompt is a system instruction given to the LLM. It defines how the AI should behave and sets the context for the agent. Its here not the user prompt.The LLM will answer as an assistant specifically focused on document management.
        checkpointer=checkpointer  # To allow multi-turn conversations with an agent, you need to enable persistence by providing a checkpointer when creating an agent. At runtime, you need to provide a config containing thread_id — a unique identifier for the conversation (session). When you enable the checkpointer, it stores agent state at every step in the provided checkpointer database. when the agent is invoked the second time with the same thread_id, the original message history from the first conversation is automatically included, together with the new user input.
    )
    return agent



# create_react_agent implements the ReAct pattern (Reason + Act):
# LLM reasons about what to do.
# Then acts by calling tools (like document_tools).
# The prompt helps define:
# Role of the agent (document assistant).
# Tone of responses.
# Constraints (e.g., "only talk about documents").

# Architecture:
# The agent consists of a language model (LLM) and a set of tools (document_tools).
# The LLM is responsible for understanding user queries and generating responses.
# The tools are used to perform specific actions, such as retrieving documents or updating metadata.

# ** One agent shouldn't have too many tools attached, you can have multiple agents for different tasks.
# ** Then have a tool to manage the interaction between agents, or a central orchestrator to coordinate complex workflows.