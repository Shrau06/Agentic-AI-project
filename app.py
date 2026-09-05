import streamlit as st
from streamlit_option_menu import option_menu

from pages.home import show_home
from pages.login import show_login
from pages.signup import show_signup
from pages.profile import show_profile
from pages.dashboard import show_dashboard

from member4.wealth_ui import wealth_dashboard

from tools.stock_tool import (
    get_stock_info,
    get_price_history,
    get_dividends
)


st.set_page_config(
    page_title="WealthLens AI",
    page_icon="💰",
    layout="wide"
)


hide_streamlit = """
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
</style>
"""

st.markdown(hide_streamlit, unsafe_allow_html=True)


if "page" not in st.session_state:
    st.session_state.page = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


pages = ["Home", "Login", "Sign Up"]

if st.session_state.logged_in:
    pages.extend(["Profile", "Dashboard", "Stock Analysis"])


icons = [
    "house",
    "box-arrow-in-right",
    "person-plus",
    "person",
    "speedometer2",
    "graph-up"
]


current_index = (
    pages.index(st.session_state.page)
    if st.session_state.page in pages
    else 0
)


col1, col2 = st.columns([1, 5])

with col1:
    st.image("assets/logo.png", width=75)

with col2:
    selected = option_menu(
        menu_title=None,
        options=pages,
        icons=icons[:len(pages)],
        orientation="horizontal",
        default_index=current_index
    )


st.session_state.page = selected


if st.session_state.page == "Home":
    show_home()

elif st.session_state.page == "Login":
    show_login()

elif st.session_state.page == "Sign Up":
    show_signup()

elif st.session_state.page == "Profile":
    show_profile()

elif st.session_state.page == "Dashboard":
    wealth_dashboard()

elif st.session_state.page == "Stock Analysis":

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