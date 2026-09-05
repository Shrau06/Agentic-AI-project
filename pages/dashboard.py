import streamlit as st
import pandas as pd
import plotly.express as px

from tools.financial_tool import calculate_financial_metrics
from agents.financial_health_agent import generate_financial_report


def show_dashboard():

    if "profile" not in st.session_state:
        st.warning("Please complete your financial profile first.")
        return

    data = st.session_state.profile

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

    st.markdown(
        """
        <h1 style='text-align:center;'>
            📊 Financial Dashboard
        </h1>
        """,
        unsafe_allow_html=True
    )

    st.success(f"Welcome {st.session_state.name}")

    st.caption(
        f"Age: {data['age']} | Occupation: {data['occupation']} | Goal: {data['goal']}"
    )

    st.divider()

        c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Income",
        f"₹{income:,.0f}"
    )

    c2.metric(
        "💸 Expense",
        f"₹{expense:,.0f}"
    )

    c3.metric(
        "🏦 Monthly Savings",
        f"₹{savings:,.0f}"
    )

    c4.metric(
        "⭐ Health Score",
        f"{health_score}/100"
    )

    st.write("")

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
            title="Expense vs Savings"
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
            title="Financial Overview"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.divider()

        st.subheader("📋 Financial Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.info(f"🎯 Goal : {data['goal']}")
        st.info(f"🏦 Current Savings : ₹{current_savings:,.0f}")
        st.info(f"🏠 Loan Amount : ₹{loan:,.0f}")

    with col2:

        st.info(f"💳 Monthly EMI : ₹{emi:,.0f}")
        st.info(f"💰 Monthly Income : ₹{income:,.0f}")
        st.info(f"💸 Monthly Expense : ₹{expense:,.0f}")

    st.divider()

    if health_score >= 80:

        st.success("🟢 Excellent Financial Health")

    elif health_score >= 60:

        st.warning("🟡 Good Financial Health")

    else:

        st.error("🔴 Financial Health Needs Improvement")

    st.subheader("💡 Quick Insights")

    if savings_rate < 20:
        st.write("• Increase your monthly savings to improve your financial health.")

    if expense_ratio > 70:
        st.write("• Your monthly expenses are quite high compared to your income.")

    if debt_ratio > 40:
        st.write("• Try reducing your debt or EMI burden.")

    if current_savings < expense * 6:
        st.write("• Build an emergency fund covering at least 6 months of expenses.")

    if (
        savings_rate >= 20
        and expense_ratio <= 70
        and debt_ratio <= 40
        and current_savings >= expense * 6
    ):
        st.success("✅ Your financial health looks excellent!")

    
    st.divider()

    st.subheader("🤖 AI Financial Analysis")

    if "financial_report" not in st.session_state:
    st.session_state.financial_report = None

if "show_report" not in st.session_state:
    st.session_state.show_report = False

st.divider()

st.subheader("🤖 AI Financial Analysis")

    if st.session_state.financial_report is None:

        if st.button(
           "📄 Generate Financial Health Summary",
           use_container_width=True
        ):

          with st.spinner("Analyzing your financial profile..."):

             st.session_state.financial_report = generate_financial_report(
                metrics,
                data["goal"]
             )

            st.success("✅ Report generated successfully!")

            st.rerun()

    else:

        if st.button(
           "👀 View Financial Health Summary",
           use_container_width=True
        ):

         st.session_state.show_report = True

    if st.session_state.show_report:

      st.divider()

      with st.container(border=True):

          st.subheader("📋 AI Financial Health Summary")

          st.markdown(st.session_state.financial_report)

    
        st.divider()


    