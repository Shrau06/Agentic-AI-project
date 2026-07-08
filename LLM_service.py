from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
print("API Key:", os.getenv("Groq_API"))
print("Current Directory:", os.getcwd())

chatmodel = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    api_key= os.getenv("Groq_API")
)


def financial_advice(user_data):
    prompt = f"""
    Name: {user_data['name']}
    Income: {user_data['income']},
    Expenses: {user_data['expenses']},
    Risk: {user_data['risk']},
    Goal: {user_data['goal']}
    You are a professional financial advisor.

    Analyze the user's financial profile and provide personalized financial advice.

    Your response should include:

    1. Spending Analysis
    Analyze whether the user's spending is healthy.
    Mention if expenses are too high compared to income.

    2. Emergency Fund
    Recommend how much emergency fund the user should maintain.

    3. Savings Plan
    suggest how much the user should save every month.

    4. Investment Suggestions
    Recommend investment options based on the user's risk tolerance.
    Explain why these investments are suitable.

    5. Goal Planning
    Explain how the user can achieve their financial goal.

    6. Financial Tips
    Give two or three  practical tips to improve their financial health.

    Guidelines:
    Use simple English.
    Be practical and realistic.
    Do not recommend risky investments without mentioning the risks.
    If the provided information is insufficient, mention what additional details would help.
    Keep the response under 250 words.
    """

    response = chatmodel.invoke(prompt)
    return response.content


 
