import streamlit as st
from database import get_user_profile, get_default_profile, save_user_profile


def show_profile():

    if "profile" not in st.session_state or not st.session_state.profile:
        if st.session_state.get("logged_in") and st.session_state.get("user_id"):
            db_profile = get_user_profile(st.session_state.user_id)
            st.session_state.profile = db_profile if db_profile else get_default_profile()
        else:
            st.session_state.profile = get_default_profile()

    p = st.session_state.profile

    st.markdown(
        "<h1 style='text-align:center;'>👤 Your Financial Profile</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h5 style='text-align:center; color:#94a3b8;'>Manage your financial profile. All 4 AI agents automatically sync with these details.</h5>",
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
                value=int(p.get("age", 28)),
                step=1
            )

        with col2:
            occupation = st.text_input(
                "Occupation",
                value=str(p.get("occupation", "Software Engineer"))
            )

        st.divider()

        st.subheader("💵 Inflows & Earnings")

        col1, col2 = st.columns(2)

        with col1:
            monthly_income = st.number_input(
                "Primary Monthly Income (₹)",
                min_value=0,
                value=int(p.get("monthly_income", 85000)),
                step=5000
            )

        with col2:
            other_income = st.number_input(
                "Other / Secondary Income (₹)",
                min_value=0,
                value=int(p.get("other_income", 10000)),
                step=1000
            )

        st.divider()

        st.subheader("💸 Monthly Expenses")

        monthly_expenses = st.number_input(
            "Total Monthly Living Expenses (₹)",
            min_value=0,
            value=int(p.get("monthly_expenses", 35000)),
            step=2500
        )

        st.divider()

        st.subheader("🏦 Capital & Savings")

        col1, col2 = st.columns(2)

        with col1:
            current_savings = st.number_input(
                "Current Liquid Savings / Emergency Fund (₹)",
                min_value=0,
                value=int(p.get("current_savings", 250000)),
                step=25000
            )

        with col2:
            monthly_savings = st.number_input(
                "Estimated Monthly Savings (₹)",
                min_value=0,
                value=int(p.get("monthly_savings", 40000)),
                step=2500
            )

        st.divider()

        st.subheader("🏠 Liabilities & Loans")

        col1, col2 = st.columns(2)

        with col1:
            loan_amount = st.number_input(
                "Current Outstanding Loan Balance (₹)",
                min_value=0,
                value=int(p.get("loan_amount", 300000)),
                step=25000
            )

        with col2:
            monthly_emi = st.number_input(
                "Monthly Loan EMI Burden (₹)",
                min_value=0,
                value=int(p.get("monthly_emi", 12000)),
                step=1000
            )

        st.divider()

        st.subheader("🎯 Primary Financial Goal")

        goal_options = [
            "Retirement",
            "Emergency Fund",
            "Buy a House",
            "Education",
            "Travel",
            "Wealth Creation",
            "Other"
        ]
        current_goal = p.get("goal", "Retirement")
        goal_idx = goal_options.index(current_goal) if current_goal in goal_options else 0

        goal = st.selectbox(
            "Select Your Financial Milestone Target",
            goal_options,
            index=goal_idx
        )

        submitted = st.form_submit_button(
            "💾 Save Profile & Analyze Financial Health",
            use_container_width=True
        )

    if submitted:
        new_profile = {
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
        st.session_state.profile = new_profile

        if st.session_state.get("logged_in") and st.session_state.get("user_id"):
            save_user_profile(st.session_state.user_id, new_profile)

        # Clear cached reports so they regenerate fresh with the new profile data
        st.session_state.financial_report = None
        st.session_state.wealth_planning_advice = None
        st.session_state.pdf_built = None
        st.session_state.wealth_report = None
        st.session_state.risk_assessment_result = None

        st.session_state.page = "Financial Dashboard"
        st.success("✅ Profile updated successfully! Redirecting to Financial Dashboard...")
        st.rerun()