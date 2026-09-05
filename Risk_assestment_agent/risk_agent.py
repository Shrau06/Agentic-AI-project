
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from risk_tool import risk_tool
from portfolio_tool import portfolio_tool
from prompts import AGENT_SYSTEM_PROMPT


def run_risk_assessment(llm, user_data):
    """Run the autonomous tool-calling WealthLens agent using native tool binding."""

    tools = [risk_tool, portfolio_tool]
    risk_result = None
    tools_by_name = {t.name: t for t in tools}

    # Bind tools directly to the LLM model
    llm_with_tools = llm.bind_tools(tools)

    user_message = f"""
Analyze this user's financial profile:

{user_data}

Perform a complete risk assessment.
Use risk_tool first.
Then use portfolio_tool if portfolio allocation is needed.
Finally generate the complete WealthLens AI report.
"""

    messages = [
        SystemMessage(content=AGENT_SYSTEM_PROMPT),
        HumanMessage(content=user_message),
    ]

    # Initial LLM call
    response = llm_with_tools.invoke(messages)
    messages.append(response)

    # Process tool calls in a loop until completion
    while hasattr(response, "tool_calls") and response.tool_calls:
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            selected_tool = tools_by_name[tool_name]

            # Execute tool call
            tool_output = selected_tool.invoke(tool_call["args"])

            # Capture risk assessment result
            if tool_name == "risk_tool":
                risk_result = tool_output

            # Append execution result back to messages
            messages.append(
                ToolMessage(
                    content=str(tool_output),
                    tool_call_id=tool_call["id"],
                    name=tool_name,
                )
            )

        # Get next model response after tools executed
        response = llm_with_tools.invoke(messages)
        messages.append(response)

    return {
        "user_profile": user_data,
        "agent_response": messages[-1].content,
        "messages": messages,
        "risk_result": risk_result,
    }