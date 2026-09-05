import os

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder
)

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("Groq_API")
)

prompt = ChatPromptTemplate.from_messages(

    [

        (
            "system",

            """
You are WealthLens AI, an expert certified financial advisor.

Your responsibilities are:

1. Analyze the user's financial profile.
2. Calculate financial strengths and weaknesses using the provided metrics.
3. Explain the financial health in simple language.
4. Give practical and personalized financial advice.
5. Answer follow-up financial questions using the previous conversation.

Financial Profile

Income : ₹{income}
Monthly Expense : ₹{expense}
Monthly Savings : ₹{monthly_savings}
Current Savings : ₹{current_savings}
Loan Amount : ₹{loan_amount}
Monthly EMI : ₹{monthly_emi}
Savings Rate : {savings_rate}%
Expense Ratio : {expense_ratio}%
Debt Ratio : {debt_ratio}%
Emergency Fund : {emergency_fund} months
Savings Status : {savings_status}
Expense Status : {expense_status}
Debt Status : {debt_status}
Emergency Fund Status : {emergency_status}
Financial Goal : {goal}
If this is the first interaction, generate a report in the following format:
Financial Health Score (0-100)
Overall Financial Health
Strengths
Weaknesses
Top Priorities
Personalized Financial Advice
If the user asks follow-up questions, answer them naturally while considering the financial profile and previous conversation.
"""
        ),

        MessagesPlaceholder(variable_name="chat_history"),

        (
            "human",
            "{input}"
        )

    ]

)

chain = prompt | llm


def generate_financial_report(metrics, goal):

    response = chain.invoke(
        {
            **metrics,
            "goal": goal,
            "chat_history": [],
            "input": "Generate my complete financial analysis report."
        }
    )

    return response.content
