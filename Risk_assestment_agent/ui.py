import streamlit as st


def risk_assessment_ui():
    """
    Displays the Risk Assessment UI and returns the user data
    when the user clicks the Analyze button.
    """
    st.title("💼 WealthLensAI")
    st.subheader("📈 Risk & Investment Assessment")

    st.write(
        "Answer a few questions so we can understand your investment behaviour "
        "and suggest a suitable investment approach."
    )

    st.header("👤 Basic Information")

    age = st.number_input(
        "Your Age",
        min_value=18,
        max_value=100,
        value=25,
    )

    income = st.number_input(
        "Monthly Income (₹)",
        min_value=0,
        value=30000,
    )

    monthly_expense = st.number_input(
        "Monthly Expenses (₹)",
        min_value=0,
        value=15000,
    )

    st.header("💰 Investment Experience")

    investment_category = st.radio(
        "Investment Experience",
        ["Beginner", "Intermediate"],
    )

    if investment_category == "Beginner":
        market_reaction = st.radio(
            "If ₹10,000 becomes ₹8,000 after one month, what will you do?",
            [
                "Withdraw all my money",
                "Withdraw some money",
                "Wait for it to recover",
                "Invest more because prices are lower",
            ],
        )

        goal = st.radio(
            "What is your investment goal?",
            [
                "Saving money safely",
                "Building long-term wealth",
                "Generating higher returns",
                "Protecting money from inflation",
            ],
        )

        investment_period = st.radio(
            "How long can you stay invested?",
            [
                "Less than 1 year",
                "1-3 years",
                "3-5 years",
                "More than 5 years",
            ],
        )

        risk_capacity = st.radio(
            "Maximum temporary loss you can tolerate",
            [
                "Up to 5%",
                "Around 10%",
                "Around 20%",
                "More than 30%",
            ],
        )

        income_stability = st.radio(
            "Income Stability",
            [
                "Unstable",
                "Somewhat stable",
                "Stable",
                "Very stable",
            ],
        )
    else:
        products_used = st.multiselect(
            "Products you've invested in",
            [
                "Fixed Deposits",
                "Gold",
                "Mutual Funds",
                "Stocks",
                "ETFs",
                "Government Bonds",
            ],
        )

        market_reaction = st.radio(
            "If your portfolio falls by 20%, what would you do?",
            [
                "Sell everything",
                "Sell some investments",
                "Hold my investments",
                "Invest more",
            ],
        )

        return_preference = st.radio(
            "Preferred Returns",
            [
                "Stable but lower returns",
                "Balanced growth",
                "Higher returns with higher risk",
            ],
        )

        review_frequency = st.radio(
            "Portfolio Review Frequency",
            [
                "Rarely",
                "Every few months",
                "Monthly",
                "Weekly",
            ],
        )

        investment_period = st.radio(
            "Investment Horizon",
            [
                "1-3 years",
                "3-5 years",
                "5-10 years",
                "More than 10 years",
            ],
        )

        goal = "Building long-term wealth"

    st.divider()

    if st.button("🔍 Analyze My Risk Profile"):
        user_data = {
            "age": age,
            "income": income,
            "monthly_expense": monthly_expense,
            "investment_category": investment_category,
            "goal": goal,
            "investment_period": investment_period,
            "market_reaction": market_reaction,
        }

        if investment_category == "Beginner":
            user_data.update(
                {
                    "risk_capacity": risk_capacity,
                    "income_stability": income_stability,
                }
            )
        else:
            user_data.update(
                {
                    "products_used": products_used,
                    "return_preference": return_preference,
                    "review_frequency": review_frequency,
                }
            )

        return user_data

    return None