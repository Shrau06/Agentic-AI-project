import streamlit as st 
from LLM_service import financial_advice

st.title("WealthLens AI")
st.header("See your Fianances Clearly")
st.subheader("Fill out your all Details")

user_name = st.text_input("Username")
income = st.number_input("Your Income")
expense = st.number_input("Your Expense")
Risk = st.selectbox(
    "Risk Level You can Tolerate",
    ["Low","Medium","High"]
)

Goal = st.text_area("Financial Goal")

if st.button("Submit"):
    
    user_data = {
        "name": user_name,
        "income": income,
        "expenses": expense,
        "risk": Risk,
        "goal": Goal
    }

    advice = financial_advice(user_data)

    st.subheader("AI Financial Advice")

    st.write(advice)


