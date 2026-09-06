import streamlit as st
import pandas as pd
import plotly.express as px

from tools.financial_tool import calculate_financial_metrics
from agents.financial_health_agent import generate_financial_report
from database import get_user_profile, get_default_profile, save_user_profile


def show_dashboard():

    # Ensure profile is always initialized with this user's data
    if "profile" not in st.session_state or not st.session_state.profile:
        if st.session_state.get("logged_in") and st.session_state.get("user_id"):
            db_profile = get_user_profile(st.session_state.user_id)
            st.session_state.profile = db_profile if db_profile else get_default_profile()
        else:
            st.session_state.profile = get_default_profile()

    data = st.session_state.profile

    # Allow inline editing of financial parameters directly on the dashboard
    with st.expander("✏️ Customize Your Financial Details", expanded=False):
        col_e1, col_e2, col_e3 = st.columns(3)
        with col_e1:
            e_income = st.number_input("Monthly Income (₹)", min_value=0, value=int(data.get("monthly_income", 0)), step=5000, key="db_income")
            e_other = st.number_input("Other Income (₹)", min_value=0, value=int(data.get("other_income", 0)), step=2000, key="db_other")
        with col_e2:
            e_expense = st.number_input("Monthly Expenses (₹)", min_value=0, value=int(data.get("monthly_expenses", 0)), step=5000, key="db_expense")
            e_savings = st.number_input("Current Savings (₹)", min_value=0, value=int(data.get("current_savings", 0)), step=25000, key="db_savings")
        with col_e3:
            e_loan = st.number_input("Loan Amount (₹)", min_value=0, value=int(data.get("loan_amount", 0)), step=25000, key="db_loan")
            e_emi = st.number_input("Monthly EMI (₹)", min_value=0, value=int(data.get("monthly_emi", 0)), step=2000, key="db_emi")

        if st.button("💾 Update Dashboard Data", key="db_update_btn", use_container_width=True):
            st.session_state.profile.update({
                "monthly_income": e_income,
                "other_income": e_other,
                "monthly_expenses": e_expense,
                "current_savings": e_savings,
                "monthly_savings": max(0, (e_income + e_other) - e_expense - e_emi),
                "loan_amount": e_loan,
                "monthly_emi": e_emi
            })
            if st.session_state.get("logged_in") and st.session_state.get("user_id"):
                save_user_profile(st.session_state.user_id, st.session_state.profile)

            st.session_state.financial_report = None
            st.session_state.wealth_planning_advice = None
            st.session_state.pdf_built = None
            st.session_state.wealth_report = None
            st.session_state.risk_assessment_result = None
            st.rerun()

    metrics = calculate_financial_metrics(data)

    income = metrics["income"]
    expense = metrics["expense"]
    savings = metrics["monthly_savings"]
    current_savings = metrics["current_savings"]
    loan = metrics["loan_amount"]
    emi = metrics["monthly_emi"]

    savings_rate = metrics["savings_rate"]
    expense_ratio = metrics["expense_ratio"]
    debt_ratio = metrics["debt_ratio"]

    # -----------------------------
    # Financial Health Score
    # -----------------------------
    health_score = 100

    if savings_rate < 20:
        health_score -= 20

    if expense_ratio > 70:
        health_score -= 20

    if debt_ratio > 40:
        health_score -= 20

    if current_savings < expense * 6:
        health_score -= 20

    health_score = max(0, health_score)
    st.session_state["health_score"] = health_score

    # -----------------------------
    # Dashboard Header
    # -----------------------------
    st.markdown(
        """
        <h1 style='text-align:center;'>
            📊 Financial Health Dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )

    user_name = st.session_state.get("name", "Investor")
    st.caption(
        f"👤 Account: **{user_name}** | Age: **{data.get('age', 28)}** | "
        f"Occupation: **{data.get('occupation', 'Professional')}** | "
        f"Goal: **{data.get('goal', 'Retirement')}**"
    )

    st.divider()

    # -----------------------------
    # Main Metrics
    # -----------------------------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Total Monthly Income",
        f"₹{income:,.0f}"
    )

    c2.metric(
        "💸 Monthly Expenses",
        f"₹{expense:,.0f}"
    )

    c3.metric(
        "🏦 Monthly Savings",
        f"₹{savings:,.0f}"
    )

    c4.metric(
        "⭐ Financial Health Score",
        f"{health_score}/100"
    )

    st.write("")

    # -----------------------------
    # Financial Ratios
    # -----------------------------
    c5, c6, c7 = st.columns(3)

    c5.metric(
        "📈 Savings Rate",
        f"{savings_rate:.1f}%"
    )

    c6.metric(
        "📉 Expense Ratio",
        f"{expense_ratio:.1f}%"
    )

    c7.metric(
        "💳 Debt Ratio",
        f"{debt_ratio:.1f}%"
    )

    st.divider()

    # -----------------------------
    # Visual Analytics Charts
    # -----------------------------
    st.subheader("📈 Financial Visual Analytics")

    left, right = st.columns(2)

    with left:
        pie = pd.DataFrame(
            {
                "Category": [
                    "Expenses",
                    "Savings"
                ],
                "Amount": [
                    expense,
                    savings
                ]
            }
        )

        fig = px.pie(
            pie,
            names="Category",
            values="Amount",
            hole=0.45,
            title="Expense vs Monthly Savings Breakdown",
            color_discrete_sequence=["#ef4444", "#10b981"]
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:
        bar = pd.DataFrame(
            {
                "Category": [
                    "Income",
                    "Expense",
                    "Monthly Savings",
                    "Current Savings"
                ],
                "Amount": [
                    income,
                    expense,
                    savings,
                    current_savings
                ]
            }
        )

        fig2 = px.bar(
            bar,
            x="Category",
            y="Amount",
            text="Amount",
            title="Capital & Cash Flow Overview",
            color="Category",
            color_discrete_sequence=["#3b82f6", "#ef4444", "#10b981", "#8b5cf6"]
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.divider()

    # -----------------------------
    # Financial Summary
    # -----------------------------
    st.subheader("📋 Financial Position Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"🎯 **Primary Goal:** {data.get('goal', 'Retirement')}")
        st.info(f"🏦 **Current Liquid Savings:** ₹{current_savings:,.0f}")
        st.info(f"🏠 **Outstanding Loans:** ₹{loan:,.0f}")

    with col2:
        st.info(f"💳 **Monthly EMI Burden:** ₹{emi:,.0f}")
        st.info(f"💰 **Total Inflow:** ₹{income:,.0f}")
        st.info(f"💸 **Total Outflow:** ₹{expense:,.0f}")

    st.divider()

    # -----------------------------
    # Financial Health Status
    # -----------------------------
    if health_score >= 80:
        st.success("🟢 **Excellent Financial Health** - Your savings rate and emergency buffer are on track!")
    elif health_score >= 60:
        st.warning("🟡 **Good Financial Health** - Room for improvement in debt management or monthly savings.")
    else:
        st.error("🔴 **Financial Health Needs Improvement** - Focus on reducing debt and building an emergency fund.")

    # -----------------------------
    # Quick Insights
    # -----------------------------
    st.subheader("💡 Key Financial Health Insights")

    if savings_rate < 20:
        st.write("• Increase your monthly savings rate to at least 20% of your income.")
    if expense_ratio > 70:
        st.write("• Your monthly expenses exceed 70% of income. Consider budgeting.")
    if debt_ratio > 40:
        st.write("• Your EMI debt ratio is high (>40%). Aim to prioritize loan prepayments.")
    if current_savings < expense * 6:
        st.write("• Your emergency fund is below 6 months of expenses. Aim to build cash reserves.")
    if savings_rate >= 20 and expense_ratio <= 70 and debt_ratio <= 40 and current_savings >= expense * 6:
        st.success("✅ Your financial fundamentals are strong across all key benchmark indicators!")

    st.divider()

    # -----------------------------
    # AI Financial Analysis
    # -----------------------------
    st.subheader("🤖 AI Financial Health Advisor")

    if "financial_report" not in st.session_state:
        st.session_state.financial_report = None

    if st.session_state.financial_report is None:
        if st.button(
            "📄 Generate AI Financial Health Summary",
            use_container_width=True,
            key="gen_fin_health_btn"
        ):
            with st.spinner("Analyzing your profile & generating comprehensive financial health report..."):
                st.session_state.financial_report = generate_financial_report(
                    metrics,
                    data.get("goal", "Retirement")
                )
            st.success("✅ AI Health Summary Generated!")
            st.rerun()
    else:
        with st.container(border=True):
            st.subheader("📋 AI Financial Health Summary")
            st.markdown(st.session_state.financial_report)

        if st.button("🔄 Re-generate Financial Health Report", key="regen_fin_report_btn"):
            st.session_state.financial_report = None
            st.rerun()
