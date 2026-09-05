import streamlit as st
import plotly.graph_objects as go

from tools.stock_tool import (
    get_stock_info,
    get_price_history,
    get_company_summary
)

from agents.research_agent import generate_research_report


def etf_page():

    st.title("📊 ETF Research Dashboard")

    # ---------------- Search Section ----------------

    col1, col2, col3 = st.columns([4, 2, 1])

    with col1:
        symbol = st.text_input(
            "ETF Symbol",
            value="NIFTYBEES.NS"
        )

    with col2:
        period = st.selectbox(
            "Period",
            ["1mo", "3mo", "6mo", "1y", "5y"],
            index=3,
            key="etf_period"
        )

    with col3:
        st.write("")
        st.write("")
        search = st.button(
            "🔍 Analyze",
            use_container_width=True,
            key="etf_search"
        )

    if not search:
        return

    # ---------------- Fetch ETF Data ----------------

    with st.spinner("Fetching ETF data..."):
        info = get_stock_info(symbol)

    if "error" in info:
        st.error(info["error"])
        return

    st.markdown("---")

    st.subheader(
        f"📊 {info.get('company_name')}"
    )

    # ---------------- Metrics ----------------

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Current Price",
            info.get("current_price")
        )

    with col2:
        st.metric(
            "Market Cap",
            info.get("market_cap")
        )

    with col3:
        st.metric(
            "Expense Ratio",
            info.get(
                "annualReportExpenseRatio",
                "N/A"
            )
        )

    with col4:
        st.metric(
            "52W High",
            info.get("52_week_high")
        )

    with col5:
        st.metric(
            "52W Low",
            info.get("52_week_low")
        )

    st.markdown("---")

    # ---------------- Price Chart ----------------

    history = get_price_history(
        symbol,
        period
    )

    if history is not None and not history.empty:

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=history.index,
                y=history["Close"],
                mode="lines",
                name="ETF Price"
            )
        )

        fig.update_layout(
            title=f"{symbol} Price History",
            height=500,
            xaxis_title="Date",
            yaxis_title="Price"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.warning(
            "No historical ETF data available."
        )

    st.markdown("---")

    # ---------------- ETF Info ----------------

    left, right = st.columns([2, 1])

    with left:

        st.subheader("📝 ETF Summary")

        summary = get_company_summary(symbol)

        st.write(summary)

    with right:

        st.subheader("📋 ETF Details")

        st.write(
            "**Category:**",
            info.get("category", "N/A")
        )

        st.write(
            "**Fund Family:**",
            info.get("fundFamily", "N/A")
        )

        st.write(
            "**Currency:**",
            info.get("currency", "N/A")
        )

        st.write(
            "**Current Price:**",
            info.get("current_price")
        )

        st.write(
            "**Market Cap:**",
            info.get("market_cap")
        )

    st.markdown("---")

    # ---------------- Volume Chart ----------------

    if history is not None and not history.empty:

        st.subheader("📊 Trading Volume")

        volume_fig = go.Figure()

        volume_fig.add_trace(
            go.Bar(
                x=history.index,
                y=history["Volume"]
            )
        )

        volume_fig.update_layout(
            height=350
        )

        st.plotly_chart(
            volume_fig,
            use_container_width=True
        )

    st.markdown("---")

    # ---------------- Daily Returns ----------------

    if history is not None and not history.empty:

        history["Daily Return (%)"] = (
            history["Close"].pct_change() * 100
        )

        st.subheader("📅 Recent Returns")

        st.dataframe(
            history[
                [
                    "Close",
                    "Daily Return (%)"
                ]
            ].tail(20),
            use_container_width=True
        )

    st.markdown("---")

    # ---------------- AI ETF Report ----------------

    etf_text = f"""
ETF Name: {info.get('company_name')}
Current Price: {info.get('current_price')}
Market Cap: {info.get('market_cap')}
Expense Ratio: {info.get('annualReportExpenseRatio', 'N/A')}
Category: {info.get('category', 'N/A')}
Fund Family: {info.get('fundFamily', 'N/A')}
Currency: {info.get('currency', 'N/A')}
52 Week High: {info.get('52_week_high')}
52 Week Low: {info.get('52_week_low')}
"""

    st.subheader("🤖 AI ETF Analysis")

    with st.spinner("Generating AI ETF Report..."):

        report = generate_research_report(
            investment_type="ETF",
            investment_info=etf_text,
            news_text="No recent ETF news available."
        )

    st.markdown(report)