
import streamlit as st

st.title("Risk Assessment")



age = st.number_input(
    "Age",
    min_value=18,
    max_value=80,
    value=25
)

investment_experience = st.selectbox(
    "Investment Experience",
    [
        "Beginner",
        "Intermediate",
        "Expert"
    ]
)

investment_goal = st.selectbox(
    "Investment Goal",
    [
        "Wealth Creation",
        "Retirement",
        "Buying a House",
        "Child Education"
    ]
)

risk_tolerance = st.selectbox(
    "Risk Tolerance",
    [
        "Low",
        "Medium",
        "High"
    ]
)

investment_horizon = st.slider(
    "Investment Horizon (Years)",
    min_value=1,
    max_value=30,
    value=10
)



if st.button("Calculate Risk"):

    risk_score = 0

    # Age
    if age < 30:
        risk_score += 3
    elif age < 45:
        risk_score += 2
    else:
        risk_score += 1

    if investment_experience == "Expert":
        risk_score += 3
    elif investment_experience == "Intermediate":
        risk_score += 2
    else:
        risk_score += 1

   
    if risk_tolerance == "High":
        risk_score += 3
    elif risk_tolerance == "Medium":
        risk_score += 2
    else:
        risk_score += 1

   
    if investment_goal == "Wealth Creation":
        risk_score += 3
    else:
        risk_score += 1

    if investment_horizon >= 10:
        risk_score += 3
    elif investment_horizon >= 5:
        risk_score += 2
    else:
        risk_score += 1


    if risk_score <= 7:
        risk_level = "Conservative"
    elif risk_score <= 11:
        risk_level = "Moderate"
    else:
        risk_level = "Aggressive"

    st.success(f"Risk Score: {risk_score}")
    st.info(f"Risk Profile: {risk_level}")