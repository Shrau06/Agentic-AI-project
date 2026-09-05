import streamlit as st
import plotly.graph_objects as go

from tools.mf_tool import (
    search_fund,
    get_fund_details,
    get_nav_history
)

from agents.research_agent import generate_research_report


def mutualfund_page():

    st.title("💼 Mutual Fund Research Dashboard")

    # ---------------- Search Section ----------------

    fund_name = st.text_input(
        "Mutual Fund Name",
        placeholder="Example: Parag Parikh Flexi Cap Fund"
    )

    if not fund_name:
        return

    with st.spinner("Searching mutual funds..."):
        funds = search_fund(fund_name)

    if len(funds) == 0:
        st.warning("No matching mutual funds found.")
        return

    selected = st.selectbox(
        "Select Mutual Fund",
        funds,
        format_func=lambda x: x["schemeName"]
    )

    scheme_code = selected["schemeCode"]

    # ---------------- Fetch Details ----------------

    with st.spinner("Fetching fund details..."):
        details = get_fund_details(scheme_code)

    st.markdown("---")

    st.subheader(
        f"💼 {details.get('scheme_name')}"
    )

    # ---------------- Metrics ----------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Fund House",
            details.get("fund_house", "N/A")
        )

    with col2:
        st.metric(
            "Category",
            details.get("scheme_category", "N/A")
        )

    with col3:
        st.metric(
            "Type",
            details.get("scheme_type", "N/A")
        )

    with col4:
        st.metric(
            "Scheme Code",
            scheme_code
        )

    st.markdown("---")

    # ---------------- Fund Details ----------------

    left, right = st.columns([2, 1])

    with left:

        st.subheader("📋 Fund Information")

        st.write(
            "**Scheme Name:**",
            details.get("scheme_name")
        )

        st.write(
            "**Fund House:**",
            details.get("fund_house")
        )

        st.write(
            "**Category:**",
            details.get("scheme_category")
        )

        st.write(
            "**Type:**",
            details.get("scheme_type")
        )

    with right:

        st.subheader("📌 Quick Info")

        st.info(
            f"""
Fund House:
{details.get('fund_house')}

Category:
{details.get('scheme_category')}

Type:
{details.get('scheme_type')}
"""
        )

    st.markdown("---")

    # ---------------- NAV History ----------------

    history = get_nav_history(
        scheme_code
    )

    if history is not None and not history.empty:

        history["date"] = (
            history["date"]
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=history["date"],
                y=history["nav"],
                mode="lines",
                name="NAV"
            )
        )

        fig.update_layout(
            title="NAV History",
            height=500,
            xaxis_title="Date",
            yaxis_title="NAV"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.warning(
            "NAV history unavailable."
        )

    st.markdown("---")

    # ---------------- NAV Returns ----------------

    if history is not None and not history.empty:

        history["Daily Return (%)"] = (
            history["nav"].pct_change() * 100
        )

        st.subheader(
            "📅 Recent NAV Returns"
        )

        st.dataframe(
            history[
                [
                    "date",
                    "nav",
                    "Daily Return (%)"
                ]
            ].tail(20),
            use_container_width=True
        )

    st.markdown("---")

    # ---------------- NAV Statistics ----------------

    if history is not None and not history.empty:

        latest_nav = round(
            history["nav"].iloc[-1],
            2
        )

        highest_nav = round(
            history["nav"].max(),
            2
        )

        lowest_nav = round(
            history["nav"].min(),
            2
        )

        avg_nav = round(
            history["nav"].mean(),
            2
        )

        st.subheader(
            "📊 NAV Statistics"
        )

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Latest NAV",
            latest_nav
        )

        c2.metric(
            "Highest NAV",
            highest_nav
        )

        c3.metric(
            "Lowest NAV",
            lowest_nav
        )

        c4.metric(
            "Average NAV",
            avg_nav
        )

    st.markdown("---")

    # ---------------- Recent NAV Data ----------------

    if history is not None and not history.empty:

        st.subheader(
            "📈 Recent NAV Data"
        )

        st.dataframe(
            history.tail(20),
            use_container_width=True
        )

    st.markdown("---")

    # ---------------- AI Report ----------------

    mf_text = f"""
Scheme Name: {details.get('scheme_name')}
Fund House: {details.get('fund_house')}
Scheme Type: {details.get('scheme_type')}
Category: {details.get('scheme_category')}
Latest NAV: {latest_nav if history is not None and not history.empty else 'N/A'}
Highest NAV: {highest_nav if history is not None and not history.empty else 'N/A'}
Lowest NAV: {lowest_nav if history is not None and not history.empty else 'N/A'}
"""

    st.subheader(
        "🤖 AI Mutual Fund Analysis"
    )

    with st.spinner(
        "Generating AI report..."
    ):

        report = generate_research_report(
            investment_type="Mutual Fund",
            investment_info=mf_text,
            news_text=""
        )

    st.markdown(report)