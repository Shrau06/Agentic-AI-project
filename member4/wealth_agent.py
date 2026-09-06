import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

def get_llm():
    groq_key = os.getenv("GROQ_API_KEY") or os.getenv("Groq_API")
    if groq_key:
        try:
            return ChatGroq(
                groq_api_key=groq_key,
                model_name="openai/gpt-oss-120b",
                temperature=0.3
            )
        except Exception:
            pass

    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=gemini_key,
        temperature=0.3
    )

llm = get_llm()


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
    prompt = f"""
You are an expert Financial Advisor.

Analyze the following user details.

Monthly Investment: ₹{investment}

Expected Return: {rate}%

Investment Period: {years} years

Financial Goal: ₹{goal}

Current Savings: ₹{current_savings}

Risk Tolerance: {risk}

Future Wealth: ₹{future_wealth}

Estimated Profit: ₹{profit}

Generate a professional financial report.

Your report must include:

1. Financial Health Analysis

2. Goal Analysis

3. Risk Analysis

4. Investment Suggestions

5. Wealth Improvement Tips

6. Final Recommendation

Keep the answer easy to understand.
"""

    response = llm.invoke(prompt)

    return response.content