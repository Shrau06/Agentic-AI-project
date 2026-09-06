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
    """Retrieve candidate LLM for the risk assessment agent with provider fallbacks."""
    groq_key = os.getenv("GROQ_API_KEY") or os.getenv("Groq_API")
    if groq_key:
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(
                model="llama-3.3-70b-versatile",
                api_key=groq_key,
                temperature=0.2,
                timeout=15
            )
        except Exception:
            pass

    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        from langchain_google_genai import ChatGoogleGenerativeAI
        for model_name in ["gemini-2.5-flash", "gemini-1.5-flash"]:
            try:
                return ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=gemini_key,
                    temperature=0.2,
                    timeout=15
                )
            except Exception:
                continue

    return None


def create_risk_agent(llm=None):
    if llm is None:
        llm = get_risk_llm()

    if llm is None:
        return None

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

    # If LLM is available, invoke agent
    if llm is not None:
        try:
            agent = create_risk_agent(llm)
            if agent is not None:
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
        except Exception as e:
            print(f"Risk agent LLM invocation failed, falling back to direct tool calculations: {e}")

    # Deterministic fallback calculation via direct tools
    try:
        r_res = risk_tool.invoke(user_data)
        p_res = portfolio_tool.invoke({
            "risk_level": r_res.get("risk_level", "Moderate"),
            "goal": user_data.get("goal", "Wealth Creation"),
            "time_horizon": user_data.get("time_horizon", 5)
        })

        fallback_report = f"""# ⚖️ WealthLens AI Risk & Allocation Diagnostic

## 1. Risk Profile Overview
- **Calculated Risk Score:** {r_res.get('risk_score', 'N/A')}/100 ({r_res.get('risk_percentage', 0)}%)
- **Assessed Risk Level:** **{r_res.get('risk_level', 'Moderate')}**

## 2. Recommended Portfolio Structure
- **Portfolio Strategy:** {p_res.get('portfolio_type', 'Balanced Growth')}
- **Target Asset Allocation:**
{chr(10).join([f"  - **{k.title()}:** {v}%" for k, v in p_res.get('allocation', {}).items()])}
- **Expected Return Range:** {p_res.get('expected_return', '10-12%')} per annum
- **Recommended Investment Horizon:** {p_res.get('investment_horizon', '5+ Years')}

## 3. Advisory Guidance
- Maintain disciplined asset rebalancing every 6 to 12 months.
- Align high-equity exposure with long-term financial horizons to mitigate market volatility.
"""

        return {
            "user_profile": user_data,
            "agent_response": fallback_report,
            "messages": [],
            "risk_result": r_res,
            "portfolio_result": p_res
        }
    except Exception as err:
        print(f"Direct fallback error: {err}")
        return None
