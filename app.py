import streamlit as st
from tools.stock_tool import (
    get_stock_info,
    get_price_history,
    get_dividends
)

st.set_page_config(
    page_title="Market Research Dashboard",
    layout="wide"
)

st.title("📈 Market Research Dashboard")

symbol = st.text_input(
    "Enter Stock Symbol",
    value="TCS.NS"
)

period = st.selectbox(
    "Select Period",
    ["1mo", "3mo", "6mo", "1y", "5y"],
    index=3
)

if st.button("Search"):

    # Basic Stock Info
    info = get_stock_info(symbol)

    st.header("Stock Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Current Price", info["current_price"])

    with col2:
        st.metric("Market Cap", info["market_cap"])

    with col3:
        st.metric("P/E Ratio", info["pe_ratio"])

    st.write("**Company:**", info["company_name"])
    st.write("**Sector:**", info["sector"])
    st.write("**Industry:**", info["industry"])
    st.write("**52 Week High:**", info["52_week_high"])
    st.write("**52 Week Low:**", info["52_week_low"])

    # Historical Data
    history = get_price_history(symbol, period)

    st.header("Historical Price Chart")
    st.line_chart(history["Close"])

    st.header("Volume Chart")
    st.bar_chart(history["Volume"])

    # Daily Returns
    history["Daily Return (%)"] = (
        history["Close"].pct_change() * 100
    )

    st.header("Daily Returns")

    st.dataframe(
        history[["Close", "Daily Return (%)"]].tail(20)
    )

    # Dividends
    dividends = get_dividends(symbol)

    st.header("Dividend History")

    if len(dividends) > 0:
        st.dataframe(dividends.tail(10))
    else:
        st.write("No dividend data available.")