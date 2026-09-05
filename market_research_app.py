import streamlit as st

from modules.stock_page import stock_page
from modules.etf_page import etf_page
from modules.mutualfund_page import mutualfund_page

st.set_page_config(
    page_title="AI Market Research Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .block-container {
        padding-top: 2.5rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }

    section[data-testid="stSidebar"] {
        width: 280px !important;
    }

    .hero-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 0.2rem;
        line-height: 1.1;
    }

    .hero-subtitle {
        text-align: center;
        color: #7a7a7a;
        font-size: 17px;
        margin-bottom: 1.4rem;
    }

    .top-card {
        padding: 14px 16px;
        border-radius: 14px;
        background: rgba(120, 120, 120, 0.08);
        border: 1px solid rgba(120, 120, 120, 0.18);
        text-align: center;
        font-size: 15px;
        font-weight: 500;
    }

    .sidebar-note {
        font-size: 14px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-title">📈 AI Market Research Dashboard</div>
<div class="hero-subtitle">Stocks • ETFs • Mutual Funds • AI Research Reports</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("📊 Navigation")
    st.markdown("---")

    page = st.radio(
        "Choose Module",
        ["📈 Stocks", "📊 ETFs", "💼 Mutual Funds"],
        index=0
    )

    st.markdown("---")
    st.markdown("### 🚀 Features")
    st.markdown(
        """
        <div class="sidebar-note">
        ✅ Stock Research<br>
        ✅ ETF Analysis<br>
        ✅ Mutual Fund Analysis<br>
        ✅ Historical Charts<br>
        ✅ AI Research Reports
        </div>
        """,
        unsafe_allow_html=True
    )

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        "<div class='top-card'>📈 Analyze Stocks using real-time market data</div>",
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        "<div class='top-card'>📊 Research ETFs with historical trends</div>",
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        "<div class='top-card'>💼 Explore Mutual Funds and NAV history</div>",
        unsafe_allow_html=True
    )

st.divider()

if page == "📈 Stocks":
    stock_page()

elif page == "📊 ETFs":
    etf_page()

elif page == "💼 Mutual Funds":
    mutualfund_page()
    