import streamlit as st

def show_home():

    st.title("💰 WealthLens AI")

    st.subheader("Your AI Financial Research Assistant")

    st.write("""
    Analyze stocks, mutual funds, ETFs, SIPs and
    receive personalized investment insights
    powered by AI Agents.
    """)

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📈 Portfolio Analysis")

    with col2:
        st.info("⚖ Risk Assessment")

    with col3:
        st.info("🤖 AI Recommendations")