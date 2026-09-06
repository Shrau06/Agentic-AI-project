import streamlit as st
import plotly.graph_objects as go
from member4.wealth_tool import calculate_sip


def simulator_ui():
    st.header("🚀 Wealth Simulator")
    st.write("Compare different investment strategies and see future wealth.")

    col1, col2, col3 = st.columns(3)
    with col1:
        monthly_investment = st.number_input(
            "Monthly Investment (₹)",
            min_value=500,
            value=5000,
            step=500,
            key="sim_investment"
        )
    with col2:
        return_rate = st.number_input(
            "Expected Return (%)",
            min_value=1.0,
            max_value=30.0,
            value=12.0,
            key="sim_rate"
        )
    with col3:
        years = st.number_input(
            "Investment Period (Years)",
            min_value=1,
            max_value=40,
            value=10,
            key="sim_years"
        )

    # Always compute and render live simulation
    total, future, profit = calculate_sip(
        monthly_investment,
        return_rate,
        years
    )

    st.subheader("📊 Simulation Result")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Investment", f"₹{total:,.0f}")
    c2.metric("Future Wealth", f"₹{future:,.0f}")
    c3.metric("Profit", f"₹{profit:,.0f}")

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=["Investment", "Profit", "Future Wealth"],
            y=[total, profit, future],
            marker_color=["#3b82f6", "#10b981", "#8b5cf6"]
        )
    )
    fig.update_layout(title="Investment Growth Comparison", height=380)
    st.plotly_chart(fig, use_container_width=True)