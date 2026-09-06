import streamlit as st
from streamlit_option_menu import option_menu

from views.home import show_home
from views.login import show_login
from views.signup import show_signup
from views.profile import show_profile
from views.dashboard import show_dashboard

from Risk_assestment_agent.app import show_risk_assessment
from member4.wealth_ui import wealth_dashboard

from tools.stock_tool import (
    get_stock_info,
    get_price_history,
    get_dividends
)


st.set_page_config(
    page_title="WealthLens AI - Autonomous Financial Intelligence",
    page_icon="💰",
    layout="wide"
)


hide_streamlit = """
<style>
#MainMenu{visibility:hidden;}
footer{visibility:hidden;}
header{visibility:hidden;}
[data-testid="stSidebarNav"] {display: none !important;}
</style>
"""

st.markdown(hide_streamlit, unsafe_allow_html=True)


from database import get_user_profile, get_default_profile


def logout_user():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.name = None
    st.session_state.email = None
    st.session_state.profile = get_default_profile()
    st.session_state.page = "Home"
    st.rerun()


if "page" not in st.session_state:
    st.session_state.page = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "profile" not in st.session_state or not st.session_state.profile:
    if st.session_state.get("logged_in") and st.session_state.get("user_id"):
        user_prof = get_user_profile(st.session_state.user_id)
        st.session_state.profile = user_prof if user_prof else get_default_profile()
    else:
        st.session_state.profile = get_default_profile()


# All 4 Agent pages are always visible in the top navigation bar
pages = [
    "Home",
    "Financial Dashboard",
    "Risk Assessment",
    "Wealth Planner",
    "Stock Analysis",
    "Profile"
]

icons = [
    "house",
    "speedometer2",
    "shield-check",
    "piggy-bank",
    "graph-up",
    "person"
]

if not st.session_state.logged_in:
    pages.append("Login")
    icons.append("box-arrow-in-right")
    pages.append("Sign Up")
    icons.append("person-plus")
else:
    pages.append("Logout")
    icons.append("box-arrow-right")

# Handle any legacy aliases
if st.session_state.page == "Dashboard":
    st.session_state.page = "Financial Dashboard"


current_index = (
    pages.index(st.session_state.page)
    if st.session_state.page in pages
    else 0
)


col1, col2 = st.columns([1, 6])

with col1:
    import os
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", width=75)
    else:
        st.markdown("### 💰")

with col2:
    selected = option_menu(
        menu_title=None,
        options=pages,
        icons=icons,
        orientation="horizontal",
        default_index=current_index,
        key=f"nav_option_menu_{st.session_state.page}"
    )


if selected == "Logout":
    logout_user()
elif selected != st.session_state.page and selected is not None:
    st.session_state.page = selected
    st.rerun()



# Sidebar session status
with st.sidebar:
    if st.session_state.logged_in:
        user_name = st.session_state.get("name", "User")
        st.write(f"👤 **Account:** {user_name}")
        if st.button("🚪 Logout", key="sidebar_logout_btn", use_container_width=True):
            logout_user()
    else:
        st.write("👤 **Account Access**")
        col_sb1, col_sb2 = st.columns(2)
        with col_sb1:
            if st.button("Login", key="sb_login_btn", use_container_width=True):
                st.session_state.page = "Login"
                st.rerun()
        with col_sb2:
            if st.button("Sign Up", key="sb_signup_btn", use_container_width=True):
                st.session_state.page = "Sign Up"
                st.rerun()


if st.session_state.page == "Home":
    show_home()

elif st.session_state.page == "Login":
    show_login()

elif st.session_state.page == "Sign Up":
    show_signup()

elif st.session_state.page == "Profile":
    show_profile()

elif st.session_state.page in ["Financial Dashboard", "Dashboard"]:
    show_dashboard()

elif st.session_state.page == "Risk Assessment":
    show_risk_assessment()

elif st.session_state.page == "Wealth Planner":
    wealth_dashboard()

elif st.session_state.page == "Stock Analysis":

    st.title("📈 Market Research Dashboard")

    col_s1, col_s2, col_s3 = st.columns([2, 1, 1])

    with col_s1:
        symbol = st.text_input(
            "Enter Stock Symbol (NSE / Global)",
            value="TCS.NS",
            key="stock_symbol_field"
        )

    with col_s2:
        period = st.selectbox(
            "Select Period",
            ["1mo", "3mo", "6mo", "1y", "5y"],
            index=3,
            key="stock_period_field"
        )

    with col_s3:
        st.write("")
        st.write("")
        st.button("🔍 Refresh Data", key="refresh_stock_btn", use_container_width=True)

    if symbol:
        with st.spinner(f"Fetching market telemetry for {symbol}..."):
            info = get_stock_info(symbol)

        if "error" in info:
            st.error(f"Error fetching stock data: {info['error']}")
        else:
            st.header(f"Stock Overview: {info.get('company_name', symbol)}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Current Price", info.get("current_price", "N/A"))

            with col2:
                st.metric("Market Cap", info.get("market_cap", "N/A"))

            with col3:
                st.metric("P/E Ratio", info.get("pe_ratio", "N/A"))

            st.write("**Company:**", info.get("company_name", "N/A"))
            st.write("**Sector:**", info.get("sector", "N/A"))
            st.write("**Industry:**", info.get("industry", "N/A"))
            st.write("**52 Week High:**", info.get("52_week_high", "N/A"))
            st.write("**52 Week Low:**", info.get("52_week_low", "N/A"))

            # Historical Data
            history = get_price_history(symbol, period)

            if history is not None and not history.empty:
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
                    history[["Close", "Daily Return (%)"]].tail(20),
                    use_container_width=True
                )

            # Dividends
            dividends = get_dividends(symbol)

            st.header("Dividend History")

            if dividends is not None and len(dividends) > 0:
                st.dataframe(dividends.tail(10), use_container_width=True)
            else:
                st.write("No dividend data available.")