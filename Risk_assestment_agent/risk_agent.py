
# from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
# from risk_tool import risk_tool
# from portfolio_tool import portfolio_tool
# from prompts import AGENT_SYSTEM_PROMPT


# def run_risk_assessment(llm, user_data):
#     """Run the autonomous tool-calling WealthLens agent using native tool binding."""

#     tools = [risk_tool, portfolio_tool]
#     risk_result = None
#     tools_by_name = {t.name: t for t in tools}

#     # Bind tools directly to the LLM model
#     llm_with_tools = llm.bind_tools(tools)

#     user_message = f"""
# Analyze this user's financial profile:

# {user_data}

# Perform a complete risk assessment.
# Use risk_tool first.
# Then use portfolio_tool if portfolio allocation is needed.
# Finally generate the complete WealthLens AI report.
# """

#     messages = [
#         SystemMessage(content=AGENT_SYSTEM_PROMPT),
#         HumanMessage(content=user_message),
#     ]

#     # Initial LLM call
#     response = llm_with_tools.invoke(messages)
#     messages.append(response)

#     # Process tool calls in a loop until completion
#     while hasattr(response, "tool_calls") and response.tool_calls:
#         for tool_call in response.tool_calls:
#             tool_name = tool_call["name"]
#             selected_tool = tools_by_name[tool_name]

#             # Execute tool call
#             tool_output = selected_tool.invoke(tool_call["args"])

#             # Capture risk assessment result
#             if tool_name == "risk_tool":
#                 risk_result = tool_output

#             # Append execution result back to messages
#             messages.append(
#                 ToolMessage(
#                     content=str(tool_output),
#                     tool_call_id=tool_call["id"],
#                     name=tool_name,
#                 )
#             )

#         # Get next model response after tools executed
#         response = llm_with_tools.invoke(messages)
#         messages.append(response)

#     return {
#         "user_profile": user_data,
#         "agent_response": messages[-1].content,
#         "messages": messages,
#         "risk_result": risk_result,
#     }


import os
import ast
import json
from dotenv import load_dotenv
from langchain.agents import create_agent

load_dotenv()

try:
    from .risk_tool import risk_tool
    from .portfolio_tool import portfolio_tool
    from .prompts import AGENT_SYSTEM_PROMPT
except ImportError:
    from Risk_assestment_agent.risk_tool import risk_tool
    from Risk_assestment_agent.portfolio_tool import portfolio_tool
    from Risk_assestment_agent.prompts import AGENT_SYSTEM_PROMPT


def get_risk_llm():
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model="gemini-3.6-flash",
        google_api_key=gemini_key,
        temperature=0.2,
    )


def create_risk_agent(llm=None):
    if llm is None:
        llm = get_risk_llm()

    return create_agent(
        model=llm,
        tools=[
            risk_tool,
            portfolio_tool
        ],
        system_prompt=AGENT_SYSTEM_PROMPT,
    )


def run_risk_assessment(llm, user_data):
    if llm is None:
        llm = get_risk_llm()

    agent = create_risk_agent(llm)

    user_message = f"""
Analyze this user's financial profile:

{user_data}

Perform a complete risk assessment.

First use risk_tool to calculate:
- risk score
- risk percentage
- risk profile
- financial factors

Then use portfolio_tool using the risk result to generate:
- portfolio type
- asset allocation
- expected return
- investment horizon

Finally generate a complete WealthLens AI report.
"""

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_message,
                }
            ]
        }
    )

    risk_result = None
    portfolio_result = None
    for msg in result.get("messages", []):
        msg_name = getattr(msg, "name", None)
        if not msg_name and isinstance(msg, dict):
            msg_name = msg.get("name")
        msg_content = getattr(msg, "content", "") if hasattr(msg, "content") else msg.get("content", "")

        if msg_name == "risk_tool":
            try:
                if isinstance(msg_content, dict):
                    risk_result = msg_content
                elif isinstance(msg_content, str):
                    risk_result = ast.literal_eval(msg_content)
            except Exception:
                pass
        elif msg_name == "portfolio_tool":
            try:
                if isinstance(msg_content, dict):
                    portfolio_result = msg_content
                elif isinstance(msg_content, str):
                    portfolio_result = ast.literal_eval(msg_content)
            except Exception:
                pass

    return {
        "user_profile": user_data,
        "agent_response": result["messages"][-1].content,
        "messages": result["messages"],
        "risk_result": risk_result,
        "portfolio_result": portfolio_result,
    }
