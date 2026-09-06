import os
from dotenv import load_dotenv

load_dotenv()


def get_wealth_llm():
    groq_key = os.getenv("GROQ_API_KEY") or os.getenv("Groq_API")
    if groq_key:
        try:
            from langchain_groq import ChatGroq
            return ChatGroq(
                groq_api_key=groq_key,
                model_name="llama-3.3-70b-versatile",
                temperature=0.3,
                timeout=15
            )
        except Exception:
            pass

    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            for model_name in ["gemini-2.5-flash", "gemini-1.5-flash"]:
                try:
                    return ChatGoogleGenerativeAI(
                        model=model_name,
                        google_api_key=gemini_key,
                        temperature=0.3,
                        timeout=15
                    )
                except Exception:
                    continue
        except Exception:
            pass

    return None


def wealth_planning_agent(
    investment,
    rate,
    years,
    goal,
    current_savings,
    risk,
    future_wealth,
    profit
):
    prompt = f"""You are WealthLens AI, an expert certified financial advisor.

Analyze the following wealth profile and generate a strategic roadmap:
- Monthly Investment: ₹{investment:,.0f}
- Expected Annual Return: {rate}%
- Investment Horizon: {years} years
- Target Financial Goal: ₹{goal:,.0f}
- Current Liquid Savings: ₹{current_savings:,.0f}
- Risk Tolerance Level: {risk}
- Projected Future Wealth: ₹{future_wealth:,.0f}
- Estimated Wealth Profit: ₹{profit:,.0f}

Provide a structured, clean markdown analysis covering:
# 💎 Wealth Strategy & Growth Roadmap
## 1. Financial Health & Capability Analysis
## 2. Goal Feasibility Assessment
## 3. Risk-Adjusted Allocation Guidance
## 4. Wealth Acceleration Strategies
## 5. Final Strategic Recommendation
"""

    llm = get_wealth_llm()
    if llm is not None:
        try:
            response = llm.invoke(prompt)
            if hasattr(response, "content") and response.content:
                return response.content
        except Exception as e:
            print(f"Wealth agent LLM invocation failed, using analytical fallback: {e}")

    # Deterministic analytical fallback
    goal_met = future_wealth >= goal
    gap = goal - future_wealth if not goal_met else 0

    return f"""# 💎 Wealth Strategy & Growth Roadmap

## 1. Financial Health & Capability Analysis
- **Monthly Commitment:** Investing **₹{investment:,.0f}/month** with an expected annual compounding rate of **{rate}%**.
- **Horizon & Reserve:** Over **{years} years**, total capital invested will reach **₹{(investment * years * 12):,.0f}** alongside your **₹{current_savings:,.0f}** liquid reserve.

## 2. Goal Feasibility Assessment
- **Target Goal:** ₹{goal:,.0f}
- **Projected Value:** ₹{future_wealth:,.0f} (Estimated Profit: ₹{profit:,.0f})
- **Feasibility Verdict:** {"✅ **On Track to Achieve Goal**" if goal_met else f"⚠️ **Funding Gap:** Approximately ₹{gap:,.0f} deficit to reach target."}

## 3. Risk-Adjusted Allocation Guidance
- **Risk Tolerance:** {risk}
- **Suggested Strategy:** {"Equities: 70%, Debt: 20%, Gold/Cash: 10%" if risk == "High" else ("Equities: 50%, Debt: 35%, Gold/Cash: 15%" if risk == "Moderate" else "Equities: 25%, Debt: 60%, Cash: 15%")}

## 4. Wealth Acceleration Strategies
- **Annual Step-Up SIP:** Increase monthly investment by 10% annually to potentially double compounding velocity.
- **Rebalance Periodically:** Review and rebalance asset allocation annually to protect accrued gains.

## 5. Final Strategic Recommendation
- Maintain systematic monthly discipline, automate contributions, and protect against inflation with growth-oriented assets.
"""