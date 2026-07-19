import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from member4.wealth_tool import (
    calculate_sip,
    calculate_growth,
    yearly_report,
    calculate_compound_interest,
    wealth_projection,
)

from member4.database import save_data
from member4.wealth_agent import wealth_planning_agent

def wealth_dashboard():

    st.set_page_config(
        page_title="WealthLensAI",
        page_icon="💰",
        layout="wide",
    )

    st.title("💰 WealthLensAI")
    st.caption("AI Powered Wealth Planner")

    # ===========================
    # Sidebar
    # ===========================

    st.sidebar.header("📥 Investment Details")

    investment = st.sidebar.number_input(
        "Monthly Investment (₹)",
        min_value=500,
        value=5000,
        step=500,
    )

    rate = st.sidebar.number_input(
        "Expected Annual Return (%)",
        min_value=1.0,
        max_value=30.0,
        value=12.0,
        step=0.5,
    )

    years = st.sidebar.number_input(
        "Investment Period (Years)",
        min_value=1,
        max_value=40,
        value=10,
    )

    goal = st.sidebar.number_input(
        "Financial Goal (₹)",
        min_value=100000,
        value=2000000,
        step=100000,
    )

    current_savings = st.sidebar.number_input(
        "Current Savings (₹)",
        min_value=0,
        value=0,
        step=10000,
    )

    risk = st.sidebar.selectbox(
        "Risk Tolerance",
        ["Low", "Moderate", "High"]
    )

    calculate = st.sidebar.button("🚀 Simulate Wealth")

    if calculate:

        total, future, profit = calculate_sip(
            investment,
            rate,
            years,
        )

        save_data(
            investment,
            rate,
            years,
            goal,
            future
        )

        # ===========================
        # Dashboard
        # ===========================

        st.header("📊 Wealth Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "💰 Total Investment",
            f"₹{total:,.0f}"
        )

        col2.metric(
            "📈 Future Wealth",
            f"₹{future:,.0f}"
        )

        col3.metric(
            "💹 Estimated Profit",
            f"₹{profit:,.0f}"
        )

        st.divider()

        # ===========================
        # Wealth Growth Graph
        # ===========================

        st.subheader("📈 Future Wealth Graph")

        growth = calculate_growth(
            investment,
            rate,
            years,
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=list(range(1, years + 1)),
                y=growth,
                mode="lines+markers",
                line=dict(
                    color="green",
                    width=3
                )
            )
        )

        fig.update_layout(
            title="Yearly Wealth Growth",
            xaxis_title="Years",
            yaxis_title="Future Wealth (₹)",
            height=500,
            template="plotly_white"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # ===========================
        # Investment Breakdown
        # ===========================

        st.subheader("🥧 Investment Breakdown")

        pie = go.Figure(
            data=[
                go.Pie(
                    labels=[
                        "Investment",
                        "Profit"
                    ],
                    values=[
                        total,
                        profit
                    ],
                    hole=0.45,
                )
            ]
        )

        pie.update_layout(
            title="Investment vs Profit"
        )

        st.plotly_chart(
            pie,
            use_container_width=True,
        )

        st.divider()

        # ===========================
        # Goal Progress
        # ===========================

        st.subheader("🎯 Goal Progress")

        progress = future / goal

        if progress > 1:
            progress = 1

        st.progress(progress)

        st.write(
            f"Goal Completion : {progress*100:.1f}%"
        )

        st.divider()

        # ===========================
        # Financial Health
        # ===========================

        st.subheader("🏆 Financial Health Score")

        score = 50

        if investment >= 5000:
            score += 15

        if years >= 10:
            score += 20

        if rate >= 12:
            score += 15

        if current_savings >= 100000:
            score += 10

        if risk == "High":
            score -= 5

        if score > 100:
            score = 100

        st.metric(
            "Financial Health",
            f"{score}/100"
        )

        st.divider()

                # ===========================
        # Year-wise Wealth Report
        # ===========================

        st.subheader("📅 Year-wise Wealth Report")

        report = yearly_report(
            investment,
            rate,
            years,
        )

        report_df = pd.DataFrame(report)

        st.dataframe(
            report_df,
            use_container_width=True
        )

        st.divider()

        # ===========================
        # 5 / 10 / 15 Year Projection
        # ===========================

        st.subheader("📊 5 / 10 / 15 Year Projection")

        projection = wealth_projection(
            investment,
            rate
        )

        projection_df = pd.DataFrame(projection)

        st.dataframe(
            projection_df,
            use_container_width=True
        )

        st.divider()

        # ===========================
        # Compound Interest Calculator
        # ===========================

        st.subheader("💰 Compound Interest Calculator")

        principal = st.number_input(
            "Principal Amount (₹)",
            min_value=1000,
            value=500000,
            step=10000,
        )

        compound_rate = st.number_input(
            "Annual Interest Rate (%)",
            min_value=1.0,
            max_value=20.0,
            value=10.0,
        )

        compound_years = st.number_input(
            "Investment Duration (Years)",
            min_value=1,
            max_value=40,
            value=15,
        )

        if st.button("Calculate Compound Interest"):

            p, future_value, interest = calculate_compound_interest(
                principal,
                compound_rate,
                compound_years,
            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Principal",
                f"₹{p:,.0f}"
            )

            c2.metric(
                "Future Value",
                f"₹{future_value:,.0f}"
            )

            c3.metric(
                "Interest Earned",
                f"₹{interest:,.0f}"
            )

        st.divider()

        # ===========================
        # Wealth Simulator
        # ===========================

        st.header("💰 Wealth Simulator")

        st.write(
            "Try different investment values and compare your future wealth."
        )

        sim_col1, sim_col2 = st.columns(2)

        with sim_col1:

            sim_investment = st.number_input(
                "Simulation Monthly Investment (₹)",
                min_value=500,
                value=int(investment),
                step=500,
            )

            sim_rate = st.number_input(
                "Simulation Annual Return (%)",
                min_value=1.0,
                max_value=30.0,
                value=float(rate),
            )

        with sim_col2:

            sim_years = st.number_input(
                "Simulation Investment Years",
                min_value=1,
                max_value=40,
                value=int(years),
            )

            sim_goal = st.number_input(
                "Simulation Goal (₹)",
                min_value=100000,
                value=int(goal),
                step=100000,
            )

        if st.button("🚀 Run Wealth Simulation"):

            total2, future2, profit2 = calculate_sip(
                sim_investment,
                sim_rate,
                sim_years,
            )

            st.success("Simulation Completed Successfully")

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Investment",
                f"₹{total2:,.0f}"
            )

            col2.metric(
                "Future Wealth",
                f"₹{future2:,.0f}"
            )

            col3.metric(
                "Profit",
                f"₹{profit2:,.0f}"
            )

            sim_progress = future2 / sim_goal

            if sim_progress > 1:
                sim_progress = 1

            st.progress(sim_progress)

            st.write(
                f"Goal Achievement : {sim_progress*100:.1f}%"
            )

        st.divider()

                # ===========================
        # Goal Status
        # ===========================

        st.header("🎯 Goal Status")

        if future >= goal:

            st.success(
                "🎉 Congratulations! Your financial goal is achievable."
            )

        else:

            remaining = goal - future

            st.error(
                "❌ Your goal has not been achieved yet."
            )

            st.write(
                f"💰 You need approximately ₹{remaining:,.0f} more to achieve your goal."
            )

        st.divider()

        # ===========================
        # AI Suggestions (Temporary)
        # ===========================

        st.header("🤖 AI Wealth Planning Agent")

        with st.spinner("Analyzing your financial profile..."):

            advice = wealth_planning_agent(
                investment,
                rate,
                years,
                goal,
                current_savings,
                risk,
                future,
                profit
            )

        st.success("Analysis Completed!")

        st.markdown(advice)

        st.divider()
        st.divider()

        # ===========================
        # Investment Summary
        # ===========================

        st.header("📋 Investment Summary")

        summary = pd.DataFrame({

            "Field": [

                "Monthly Investment",
                "Expected Return",
                "Investment Period",
                "Current Savings",
                "Risk Level",
                "Financial Goal",
                "Future Wealth",
                "Estimated Profit"

            ],

            "Value": [

                f"₹{investment:,.0f}",
                f"{rate} %",
                f"{years} Years",
                f"₹{current_savings:,.0f}",
                risk,
                f"₹{goal:,.0f}",
                f"₹{future:,.0f}",
                f"₹{profit:,.0f}"

            ]

        })

        st.dataframe(
            summary,
            use_container_width=True
        )

        st.divider()

        # ===========================
        # Next Module Placeholder
        # ===========================

        st.info("""
📄 Final Report Page

This section will generate an AI-powered financial report
using the Report Generation Agent.

(Coming in the next phase.)
""")

        st.success("✅ Wealth Planning Completed Successfully!")

    else:

        st.info(
            "👈 Enter your investment details from the sidebar and click **🚀 Simulate Wealth**."
        )