import os
# pyrefly: ignore [missing-import]
import streamlit as st
from member4.report_agent import report_agent
from member4.pdf_generator import create_pdf


def report_ui(
    goal,
    investment,
    years,
    total,
    future,
    profit
):
    st.header("📄 Wealth Planning Report")

    # Determine goal status
    if future >= goal:
        goal_status = "✅ Goal Achievable"
    else:
        remaining = goal - future
        goal_status = f"⚠️ Need ₹{remaining:,.0f} more to achieve the goal"

    # Always maintain active report state
    if "wealth_report" not in st.session_state or st.button("🔄 Refresh Wealth Report", key="generate_report"):
        report = report_agent(
            goal,
            investment,
            years,
            total,
            future,
            profit,
            goal_status
        )
        report["health_score"] = st.session_state.get("health_score", "N/A")
        report["risk_level"] = st.session_state.get("risk_level", "Not Assessed")
        st.session_state["wealth_report"] = report

    report = st.session_state["wealth_report"]

    st.divider()

    # Financial Goal
    st.subheader("🎯 Financial Goal")
    st.metric("Goal Amount", report["goal"])

    st.divider()

    # Investment Details
    st.subheader("💵 Investment Details")
    col1, col2 = st.columns(2)
    col1.metric("Monthly Investment", report["investment"])
    col2.metric("Investment Duration", report["years"])

    st.divider()

    # Wealth Calculation
    st.subheader("📊 Wealth Calculation")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Investment", report["total"])
    c2.metric("Future Wealth", report["future"])
    c3.metric("Estimated Profit", report["profit"])

    st.divider()

    # Goal Status
    st.subheader("🎯 Goal Achievement Status")
    if "Achievable" in report["status"]:
        st.success(report["status"])
    else:
        st.warning(report["status"])

    st.divider()

    # AI Advice
    st.subheader("🤖 AI Wealth Advice")
    st.write(report["advice"])

    st.divider()

    # ---------------- PDF Generation ----------------
    st.subheader("📄 Export Comprehensive PDF Report")

    col_p1, col_p2 = st.columns(2)

    with col_p1:
        if st.button("🔨 Build PDF Report", key="create_pdf_button", use_container_width=True):
            create_pdf(report)
            st.session_state["pdf_built"] = True
            st.success("✅ PDF created successfully!")

    # Ensure download button is persistent and doesn't disappear on click
    if st.session_state.get("pdf_built", False) or os.path.exists("WealthLensAI_Report.pdf"):
        if not os.path.exists("WealthLensAI_Report.pdf"):
            create_pdf(report)
        with open("WealthLensAI_Report.pdf", "rb") as file:
            with col_p2:
                st.download_button(
                    label="⬇️ Download Wealth Report PDF",
                    data=file,
                    file_name="WealthLensAI_Report.pdf",
                    mime="application/pdf",
                    key="download_pdf",
                    use_container_width=True
                )