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
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        from langchain_google_genai import ChatGoogleGenerativeAI
        for model_name in ["gemini-2.5-flash", "gemini-1.5-flash"]:
            try:
                return ChatGoogleGenerativeAI(
                    model=model_name,
                    google_api_key=gemini_key,
                    temperature=0.2,
                    timeout=10
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

    # Pre-calculate deterministic mathematical risk & portfolio metrics
    try:
        r_res = risk_tool.invoke({"user_data": user_data})
    except Exception as e:
        print(f"Error calculating risk_tool: {e}")
        r_res = {
            "risk_score": 60,
            "maximum_score": 115,
            "risk_percentage": 52.0,
            "risk_profile": "Moderate",
            "risk_level": "Moderate",
            "monthly_savings": max(0, user_data.get("income", 50000) - user_data.get("monthly_expense", 20000))
        }

    try:
        p_res = portfolio_tool.invoke({"user_data": user_data, "risk_result": r_res})
    except Exception as e:
        print(f"Error calculating portfolio_tool: {e}")
        p_res = {
            "portfolio_type": r_res.get("risk_level", "Moderate"),
            "allocation": {"Equity": 50, "Debt Funds": 25, "Gold": 10, "ETFs": 10, "Cash": 5},
            "expected_return": "8% - 12% annually",
            "investment_horizon": user_data.get("investment_period", "3-5 years")
        }

    # Attempt agent invocation
    if llm is not None:
        try:
            agent = create_risk_agent(llm)
            if agent is not None:
                user_message = f"""
Analyze this user's financial profile:
{user_data}

Pre-calculated Tool Outputs:
- Risk Tool Assessment: {r_res}
- Portfolio Allocation: {p_res}

Generate a comprehensive, structured WealthLens AI Risk & Allocation Diagnostic report in markdown format.
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

                agent_text = result["messages"][-1].content
                if agent_text and len(str(agent_text).strip()) > 50:
                    return {
                        "user_profile": user_data,
                        "agent_response": agent_text,
                        "messages": result.get("messages", []),
                        "risk_result": r_res,
                        "portfolio_result": p_res,
                    }
        except Exception as e:
            print(f"Risk agent LLM invocation failed, using direct diagnostic report: {e}")

    # Comprehensive fallback report
    risk_lvl = r_res.get("risk_level", "Moderate")
    score = r_res.get("risk_score", 60)
    pct = r_res.get("risk_percentage", 50.0)
    p_type = p_res.get("portfolio_type", risk_lvl)
    alloc = p_res.get("allocation", {})
    exp_ret = p_res.get("expected_return", "8% - 12% annually")
    horizon = p_res.get("investment_horizon", user_data.get("investment_period", "3-5 years"))

    alloc_md = "\n".join([f"- **{k}:** {v}%" for k, v in alloc.items()])

    report = f"""# ⚖️ WealthLens AI Risk & Portfolio Diagnostic

## 1. Risk Profile Assessment
- **Risk Score:** **{score}** / {r_res.get('maximum_score', 115)} ({pct:.1f}%)
- **Assessed Risk Level:** **{risk_lvl}**
- **Monthly Savings Capacity:** **₹{r_res.get('monthly_savings', 0):,.0f}**
- **Investment Horizon:** **{horizon}**

## 2. Recommended Asset Allocation ({p_type})
{alloc_md}

- **Expected Annual Return:** **{exp_ret}**
- **Strategic Horizon:** **{horizon}**

## 3. Behavioral & Market Guidance
- **Market Reaction Posture:** Your indicated response to volatility is aligned with a **{risk_lvl}** strategy.
- **Rebalancing Plan:** Review allocation annually to lock in capital gains from outperforming asset classes.
- **Emergency Protection:** Ensure at least 6 months of living expenses remain liquid before committing to higher-risk equity tranches.

## 4. Professional Disclaimer
*This automated risk evaluation is for educational and strategic planning purposes. Always consult a qualified SEBI-registered financial advisor before executing investment allocations.*
"""

    return {
        "user_profile": user_data,
        "agent_response": report,
        "messages": [],
        "risk_result": r_res,
        "portfolio_result": p_res
    }
