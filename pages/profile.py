import streamlit as st


def show_profile():

    st.markdown(
        "<h1 style='text-align:center;'>Your Financial Details</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h4 style='text-align:center;'>Enter your financial details to analyze your financial health.</h4>",
        unsafe_allow_html=True
    )

    st.divider()

    with st.form("financial_profile"):

        st.subheader("👤 Personal Information")

        col1, col2 = st.columns(2)

        with col1:
            age = st.number_input(
                "Age",
                min_value=18,
                max_value=100,
                step=1
            )

        with col2:
            occupation = st.text_input("Occupation")

        st.divider()

        st.subheader("💵 Income")

        col1, col2 = st.columns(2)

        with col1:
            monthly_income = st.number_input(
                "Monthly Income (₹)",
                min_value=0,
                step=1000
            )

        with col2:
            other_income = st.number_input(
                "Other Income (₹)",
                min_value=0,
                step=500
            )

        st.divider()

        st.subheader("💸 Expenses")

        monthly_expenses = st.number_input(
            "Total Monthly Expenses (₹)",
            min_value=0,
            step=1000
        )

        st.divider()

        st.subheader("🏦 Savings")

        col1, col2 = st.columns(2)

        with col1:
            current_savings = st.number_input(
                "Current Savings (₹)",
                min_value=0,
                step=1000
            )

        with col2:
            monthly_savings = st.number_input(
                "Monthly Savings (₹)",
                min_value=0,
                step=500
            )

        st.divider()

        st.subheader("🏠 Loans")

        col1, col2 = st.columns(2)

        with col1:
            loan_amount = st.number_input(
                "Current Loan Amount (₹)",
                min_value=0,
                step=1000
            )

        with col2:
            monthly_emi = st.number_input(
                "Monthly EMI (₹)",
                min_value=0,
                step=500
            )

        st.divider()

        st.subheader("🎯 Financial Goal")

        goal = st.selectbox(
            "Select Your Financial Goal",
            [
                "Emergency Fund",
                "Buy a House",
                "Retirement",
                "Education",
                "Travel",
                "Other"
            ]
        )

        submitted = st.form_submit_button(
            "Analyze Financial Health",
            use_container_width=True
        )

    if submitted:

        st.session_state.profile = {
            "age": age,
            "occupation": occupation,
            "monthly_income": monthly_income,
            "other_income": other_income,
            "monthly_expenses": monthly_expenses,
            "current_savings": current_savings,
            "monthly_savings": monthly_savings,
            "loan_amount": loan_amount,
            "monthly_emi": monthly_emi,
            "goal": goal
        }

        st.session_state.page = "Dashboard"
        st.rerun()