import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),
    model_name="llama-3.3-70b-versatile",
    temperature=0.3
)


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