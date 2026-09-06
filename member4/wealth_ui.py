import streamlit as st
import plotly.graph_objects as go
import pandas as pd

from member4.wealth_tool import (
    calculate_sip,
    calculate_growth,
    yearly_report,
)

from member4.database import save_data
from member4.wealth_agent import wealth_planning_agent

from member4.compound_ui import compound_interest_ui
from member4.simulator_ui import simulator_ui
from member4.sip_ui import sip_calculator_ui
from member4.report_ui import report_ui

def wealth_dashboard():
    st.title("💰 WealthLensAI")
    st.caption("AI Powered Wealth Planner")

    # ---------------- Sidebar ----------------

    profile = st.session_state.get("profile", {})
    saved_monthly = int(profile.get("monthly_savings", 5000)) if profile.get("monthly_savings", 0) > 0 else 5000
    saved_current = int(profile.get("current_savings", 0)) if profile.get("current_savings", 0) > 0 else 0
    
    # Map risk level from Agent 2 if available
    risk_level_stored = st.session_state.get("risk_level", "Moderate")
    risk_map = {"Conservative": "Low", "Moderate": "Moderate", "Aggressive": "High"}
    default_risk = risk_map.get(risk_level_stored, "Moderate")
    risk_options = ["Low", "Moderate", "High"]
    risk_idx = risk_options.index(default_risk) if default_risk in risk_options else 1

    st.sidebar.header("📥 Investment Details")

    investment = st.sidebar.number_input(
        "Monthly Investment (₹)",
        min_value=500,
        value=saved_monthly,
        step=500,
    )

    rate = st.sidebar.number_input(
        "Expected Annual Return (%)",
        min_value=1.0,
        max_value=30.0,
        value=12.0,
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
        value=saved_current,
        step=10000,
    )

    risk = st.sidebar.selectbox(
        "Risk Tolerance",
        risk_options,
        index=risk_idx
    )

    if "dashboard" not in st.session_state:
        st.session_state.dashboard = True

    if st.sidebar.button("🚀 Re-calculate Wealth", use_container_width=True):
        st.session_state.dashboard = True
        st.session_state.wealth_planning_advice = None
        st.rerun()

    st.info(f"🔗 **Synced Profile:** Monthly Investment: **₹{investment:,.0f}** | Risk Level: **{risk}** | Target Goal: **₹{goal:,.0f}**")

    # ---------------- Calculations ----------------

    total, future, profit = calculate_sip(
        investment,
        rate,
        years
    )

    save_data(
        investment,
        rate,
        years,
        goal,
        future,
        user_id=st.session_state.get("user_id", 0)
    )

    # ---------------- Dashboard ----------------

    st.header("📊 Wealth Dashboard")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "💰 Total Investment",
        f"₹{total:,.0f}"
    )

    c2.metric(
        "📈 Future Wealth",
        f"₹{future:,.0f}"
    )

    c3.metric(
        "💹 Estimated Profit",
        f"₹{profit:,.0f}"
    )

    st.divider()

    # ---------------- Wealth Graph ----------------

    st.subheader("📈 Future Wealth Graph")

    growth = calculate_growth(
        investment,
        rate,
        years
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=list(range(1, years + 1)),
            y=growth,
            mode="lines+markers",
        )
    )

    fig.update_layout(
        title="Yearly Wealth Growth",
        xaxis_title="Years",
        yaxis_title="Future Wealth (₹)",
        template="plotly_white",
        height=500,
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.divider()

    # ---------------- Investment Breakdown ----------------

    st.subheader("🥧 Investment Breakdown")

    pie = go.Figure(
        data=[
            go.Pie(
                labels=["Investment", "Profit"],
                values=[total, profit],
                hole=0.45,
            )
        ]
    )

    pie.update_layout(title="Investment vs Profit")

    st.plotly_chart(
        pie,
        use_container_width=True,
    )

    st.divider()

    # ---------------- Goal Progress ----------------

    st.subheader("🎯 Goal Progress")

    progress = min(future / goal, 1.0)

    st.progress(progress)

    st.write(
        f"Goal Completion : {progress * 100:.1f}%"
    )

    st.divider()

    # ---------------- Financial Health ----------------

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

    score = min(score, 100)

    st.metric(
        "Financial Health",
        f"{score}/100"
    )

    st.divider()

    # ---------------- Year-wise Wealth Report ----------------

    st.subheader("📅 Year-wise Wealth Report")

    report = yearly_report(
        investment,
        rate,
        years,
    )

    report_df = pd.DataFrame(report)

    st.dataframe(
        report_df,
        use_container_width=True,
    )

    st.divider()

        # ---------------- 5 / 10 / 15 Year Projection ----------------

    st.subheader("📊 Wealth Projection")

    projection = yearly_report(
        investment,
        rate,
        min(years, 15)
    )

    projection_df = pd.DataFrame(projection)

    st.dataframe(
        projection_df.tail(3),
        use_container_width=True,
    )

    st.divider()

    # ---------------- Goal Status ----------------

    st.header("🎯 Goal Status")

    if future >= goal:

        st.success(
            "🎉 Congratulations! Your financial goal is achievable."
        )

    else:

        remaining = goal - future

        st.warning(
            f"You need approximately ₹{remaining:,.0f} more to reach your goal."
        )

    st.divider()

    # ---------------- SIP Calculator ----------------

    sip_calculator_ui()

    st.divider()

    # ---------------- Compound Interest Calculator ----------------

    compound_interest_ui()

    st.divider()

    simulator_ui()

    st.divider()

    # ---------------- AI Wealth Planning Agent ----------------
    st.header("🤖 AI Wealth Planning Agent")

    if "wealth_planning_advice" not in st.session_state:
        st.session_state.wealth_planning_advice = None

    if st.session_state.wealth_planning_advice is None:
        if st.button("🚀 Generate AI Wealth Strategy Roadmap", use_container_width=True, key="generate_wealth_advice_btn"):
            with st.spinner("Analyzing your profile & generating strategic wealth roadmap..."):
                st.session_state.wealth_planning_advice = wealth_planning_agent(
                    investment,
                    rate,
                    years,
                    goal,
                    current_savings,
                    risk,
                    future,
                    profit,
                )
            st.success("Analysis Completed!")
            st.rerun()
    else:
        with st.container(border=True):
            st.markdown(st.session_state.wealth_planning_advice)
        if st.button("🔄 Re-generate AI Wealth Strategy", key="regen_wealth_advice_btn"):
            st.session_state.wealth_planning_advice = None
            st.rerun()

    st.divider()

        # ---------------- Wealth Report ----------------

    report_ui(
    goal,
    investment,
    years,
    total,
    future,
    profit
)