import streamlit as st
import plotly.graph_objects as go

from member4.wealth_tool import calculate_sip


def sip_calculator_ui():

    st.header("💰 SIP Calculator")

    st.write(
        "Calculate how your monthly investment can grow over time."
    )


    monthly_investment = st.number_input(
        "Monthly SIP Amount (₹)",
        min_value=500,
        value=5000,
        step=500,
        key="sip_amount"
    )


    return_rate = st.number_input(
        "Expected Annual Return (%)",
        min_value=1.0,
        max_value=30.0,
        value=12.0,
        key="sip_return"
    )


    years = st.number_input(
        "Investment Duration (Years)",
        min_value=1,
        max_value=40,
        value=10,
        key="sip_years"
    )


    if st.button(
        "Calculate SIP",
        key="sip_button"
    ):


        total, future, profit = calculate_sip(
            monthly_investment,
            return_rate,
            years
        )


        st.subheader("📊 SIP Result")


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Total Investment",
            f"₹{total:,.0f}"
        )


        col2.metric(
            "Future Value",
            f"₹{future:,.0f}"
        )


        col3.metric(
            "Estimated Profit",
            f"₹{profit:,.0f}"
        )


        st.divider()


        fig = go.Figure()


        fig.add_trace(
            go.Pie(
                labels=[
                    "Invested Amount",
                    "Profit"
                ],
                values=[
                    total,
                    profit
                ],
                hole=0.45
            )
        )


        fig.update_layout(
            title="Investment vs Profit"
        )


        st.plotly_chart(
            fig,
            use_container_width=True
        )