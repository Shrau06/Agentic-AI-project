import streamlit as st


def show_home():

    # Hero Title Banner
    st.markdown(
        """
        <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 32px; border-radius: 12px; border-left: 6px solid #3b82f6; margin-bottom: 25px;">
            <h1 style="color: #60a5fa; margin: 0; font-size: 32px; font-weight: 700;">💰 WealthLens AI</h1>
            <h3 style="color: #e2e8f0; font-weight: 400; margin-top: 8px; font-size: 18px;">Intelligent Financial Research & Wealth Advisory Platform</h3>
            <p style="color: #94a3b8; margin-top: 10px; font-size: 15px; line-height: 1.6;">
                Analyze your financial health, calculate your personalized risk profile, simulate wealth growth with smart SIP and compounding tools, and explore real-time stock market telemetry.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("Explore Features")

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### 📊 Financial Dashboard")
            st.write("Detailed breakdown of your income, expenses, debts, savings rate, and customized AI financial health summary.")
            if st.button("Open Financial Dashboard", key="home_btn_fin", use_container_width=True):
                st.session_state.page = "Financial Dashboard"
                st.rerun()

        with st.container(border=True):
            st.markdown("### 💰 Wealth Planner")
            st.write("SIP projections, compound interest modeling, goal progress tracking, and downloadable PDF wealth reports.")
            if st.button("Open Wealth Planner", key="home_btn_wealth", use_container_width=True):
                st.session_state.page = "Wealth Planner"
                st.rerun()

    with col2:
        with st.container(border=True):
            st.markdown("### ⚖️ Risk Assessment")
            st.write("Behavioral risk analysis, tailored asset allocation strategies, and portfolio recommendations.")
            if st.button("Open Risk Assessment", key="home_btn_risk", use_container_width=True):
                st.session_state.page = "Risk Assessment"
                st.rerun()

        with st.container(border=True):
            st.markdown("### 📈 Stock Analysis")
            st.write("Real-time market search, historical price trends, volume charts, dividend history, and daily return analytics.")
            if st.button("Open Stock Analysis", key="home_btn_stocks", use_container_width=True):
                st.session_state.page = "Stock Analysis"
                st.rerun()