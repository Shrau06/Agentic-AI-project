import streamlit as st
import plotly.graph_objects as go
from sentiment.sentiment_analyzer import analyze_sentiment

from tools.stock_tool import (
    get_stock_info,
    get_price_history,
    get_dividends,
    get_company_summary
)

from tools.news_tool import get_news
from agents.research_agent import generate_research_report


def stock_page():

    st.title("📈 Stock Research Dashboard")

    # ---------- Search Section ----------

    col1, col2, col3 = st.columns([4, 2, 1])

    with col1:
        symbol = st.text_input(
            "Stock Symbol",
            value="TCS.NS"
        )

    with col2:
        period = st.selectbox(
            "Period",
            ["1mo", "3mo", "6mo", "1y", "5y"],
            index=3
        )

    with col3:
        st.write("")
        st.write("")
        search = st.button(
            "🔍 Analyze",
            use_container_width=True
        )

    if not search:
        return

    # ---------- Fetch Data ----------

    with st.spinner("Fetching market data..."):
        info = get_stock_info(symbol)

    if "error" in info:
        st.error(info["error"])
        return

    # ---------- Company Header ----------

    st.markdown("---")

    st.subheader(
        f"🏢 {info.get('company_name')}"
    )

    # ---------- Metrics ----------

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Price",
        info.get("current_price")
    )

    col2.metric(
        "P/E",
        info.get("pe_ratio")
    )

    col3.metric(
        "Market Cap",
        info.get("market_cap")
    )

    col4.metric(
        "52W High",
        info.get("52_week_high")
    )

    col5.metric(
        "52W Low",
        info.get("52_week_low")
    )

    st.markdown("---")

    # ---------- Chart ----------

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
                name="Close Price"
            )
        )

        fig.update_layout(
            title=f"{symbol} Price Chart",
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
            "Historical data unavailable."
        )

    st.markdown("---")

    # ---------- Company + News ----------

    left, right = st.columns([2, 1])

    with left:

        st.subheader("🏢 Company Summary")

        summary = get_company_summary(symbol)

        st.write(summary)

    with right:

        st.subheader("📋 Details")

        st.write(
            "**Sector:**",
            info.get("sector")
        )

        st.write(
            "**Industry:**",
            info.get("industry")
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

    # ---------- Volume ----------

    if history is not None and not history.empty:

        st.subheader(
            "📊 Trading Volume"
        )

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

    # ---------- Returns ----------

    if history is not None and not history.empty:

        history["Daily Return (%)"] = (
            history["Close"].pct_change() * 100
        )

        st.subheader(
            "📅 Recent Returns"
        )

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

    # ---------- Dividends ----------

    st.subheader(
        "💰 Dividend History"
    )

    dividends = get_dividends(symbol)

    if dividends is not None and len(dividends) > 0:

        st.dataframe(
            dividends.tail(10),
            use_container_width=True
        )

    else:
        st.info(
            "No dividend data available."
        )

    st.markdown("---")

    # ---------- News ----------

    st.subheader("📰 Latest News")

    company_name = info.get(
        "company_name",
        symbol
    )

    articles = get_news(company_name)

    news_text = ""
    positive = 0
    negative = 0
    neutral = 0

    if articles:
        for article in articles[:5]:
            title = article.get("title", "No Title")
            description = article.get("description", "")
            text = f"{title} {description}"

            sentiment = analyze_sentiment(text)

            if sentiment == "Positive":
                positive += 1
            elif sentiment == "Negative":
                negative += 1
            else:
                neutral += 1

        st.subheader("📊 News Sentiment")

        col1, col2, col3 = st.columns(3)

        col1.metric("🟢 Positive", positive)
        col2.metric("🟡 Neutral", neutral)
        col3.metric("🔴 Negative", negative)

        if positive > negative:
            st.success("Overall Sentiment: Positive")
        elif negative > positive:
            st.error("Overall Sentiment: Negative")
        else:
            st.info("Overall Sentiment: Neutral")

        st.markdown("---")

        for article in articles[:5]:
            title = article.get("title", "No Title")
            description = article.get("description", "")
            text = f"{title} {description}"
            sentiment = analyze_sentiment(text)
            url = article.get("url", "")

            with st.container(border=True):
                st.markdown(f"### {title}")
                if sentiment == "Positive":
                   st.success("🟢 Positive")

                elif sentiment == "Negative":
                   st.error("🔴 Negative")

                else:
                    st.info("🟡 Neutral")
                if description:
                    st.write(description)

                if url:
                    st.link_button(
                        "Read Article",
                        url
                    )

            news_text += f"""
Title: {title}

Description: {description}

"""
    else:
        st.info("No recent news found.")

    # ---------- AI Report ----------

    stock_text = f"""
Company Name: {info.get('company_name')}
Current Price: {info.get('current_price')}
Market Cap: {info.get('market_cap')}
PE Ratio: {info.get('pe_ratio')}
Sector: {info.get('sector')}
Industry: {info.get('industry')}
52 Week High: {info.get('52_week_high')}
52 Week Low: {info.get('52_week_low')}
"""

    st.subheader(
        "🤖 AI Research Report"
    )

    with st.spinner(
        "Generating AI analysis..."
    ):

        report = generate_research_report(
            investment_type="Stock",
            investment_info=stock_text,
            news_text=news_text
        )

    st.markdown(report)