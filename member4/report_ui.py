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


    # ---------------- Generate Report ----------------

    if st.button(
        "Generate Wealth Report",
        key="generate_report"
    ):

        if future >= goal:

            goal_status = "✅ Goal Achievable"

        else:

            remaining = goal - future

            goal_status = (
                f"⚠️ Need ₹{remaining:,.0f} more to achieve the goal"
            )


        report = report_agent(
            goal,
            investment,
            years,
            total,
            future,
            profit,
            goal_status
        )


        # Store dictionary report
        st.session_state["wealth_report"] = report



    # ---------------- Display Report ----------------

    if "wealth_report" in st.session_state:


        st.success(
            "Report Generated Successfully!"
        )


        report = st.session_state["wealth_report"]


        st.divider()


        # Financial Goal

        st.subheader("🎯 Financial Goal")

        st.metric(
            "Goal Amount",
            report["goal"]
        )


        st.divider()


        # Investment Details

        st.subheader("💵 Investment Details")


        col1, col2 = st.columns(2)


        col1.metric(
            "Monthly Investment",
            report["investment"]
        )


        col2.metric(
            "Investment Duration",
            report["years"]
        )


        st.divider()


        # Wealth Calculation

        st.subheader("📊 Wealth Calculation")


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Total Investment",
            report["total"]
        )


        col2.metric(
            "Future Wealth",
            report["future"]
        )


        col3.metric(
            "Estimated Profit",
            report["profit"]
        )


        st.divider()


        # Goal Status

        st.subheader("🎯 Goal Achievement Status")


        if "Achievable" in report["status"]:

            st.success(
                report["status"]
            )

        else:

            st.warning(
                report["status"]
            )


        st.divider()


        # AI Advice

        st.subheader("🤖 AI Wealth Advice")


        st.write(
            report["advice"]
        )


        st.divider()


        # ---------------- PDF Generation ----------------

        st.subheader("📄 Export Report")


        if st.button(
            "Create PDF",
            key="create_pdf_button"
        ):


            pdf_file = create_pdf(
                report
            )


            with open(pdf_file, "rb") as file:


                st.download_button(
                    label="⬇️ Download Wealth Report PDF",
                    data=file,
                    file_name="WealthLensAI_Report.pdf",
                    mime="application/pdf",
                    key="download_pdf"
                )