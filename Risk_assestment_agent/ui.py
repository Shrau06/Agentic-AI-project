

import streamlit as st


def risk_assessment_ui():
    """
    Displays the WealthLens AI Risk Assessment UI
    and returns user data when the user clicks
    'Analyze My Risk Profile'.
    """

    # ============================================================
    # DARK THEME / UI STYLING
    # ============================================================

    st.markdown(
        """
        <style>
        /* Brand Header */
        .brand-header {
            background: linear-gradient(
                135deg,
                #1f2937 0%,
                #111827 100%
            );
            border: 1px solid #374151;
            border-left: 6px solid #2563eb;
            padding: 24px;
            border-radius: 8px;
            margin-bottom: 24px;
        }

        .brand-header h1 {
            color: #38bdf8 !important;
            font-size: 30px !important;
            font-weight: 700 !important;
            margin: 0 0 6px 0 !important;
            padding: 0 !important;
            letter-spacing: -0.5px;
        }

        .brand-header p {
            color: #9ca3af !important;
            font-size: 15px !important;
            margin: 0 !important;
        }

        /* Section Headers */
        .section-header {
            color: #3b82f6 !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.05em !important;
            padding-bottom: 8px !important;
            border-bottom: 2px solid #e2e8f0 !important;
            margin-top: 16px !important;
            margin-bottom: 20px !important;
        }

        /* Input fields */
        div[data-baseweb="input"],
        div[data-baseweb="select"] {
            background-color: #1f2937 !important;
            border-color: #374151 !important;
            color: #ffffff !important;
        }

        /* Input text */
        input {
            color: #ffffff !important;
        }

        /* Radio group */
        div[role="radiogroup"] {
            gap: 10px;
        }

        div[role="radiogroup"] label {
            background-color: #161b22;
            border: 1px solid #30363d;

            padding: 10px 14px;
            border-radius: 6px;

            width: 100%;

            transition: all 0.2s ease;
        }

        div[role="radiogroup"] label:hover {
            border-color: #2563eb;
            background-color: #1f2937;
        }

        /* Buttons */
        .stButton > button {
            width: 100% !important;

            background-color: #2563eb !important;
            color: #ffffff !important;

            font-weight: 600 !important;
            font-size: 16px !important;

            padding: 12px 20px !important;

            border-radius: 6px !important;
            border: none !important;

            margin-top: 10px !important;
        }

        .stButton > button:hover {
            background-color: #1d4ed8 !important;
            color: #ffffff !important;
        }

        /* Form submit button */
        button[kind="primaryFormSubmit"] {
            width: 100% !important;

            background-color: #2563eb !important;
            color: #ffffff !important;

            font-weight: 600 !important;
            font-size: 16px !important;

            padding: 12px 20px !important;

            border-radius: 6px !important;
            border: none !important;
        }

        button[kind="primaryFormSubmit"]:hover {
            background-color: #1d4ed8 !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # ============================================================
    # BRAND HEADER
    # ============================================================

    st.markdown(
        """
        <div class="brand-header">
            <h1>WealthLensAI</h1>
            <p>Risk & Investment Assessment</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write(
        "Answer a few questions so we can understand your "
        "investment behaviour and suggest a suitable "
        "investment approach."
    )

    # ============================================================
    # FORM
    # ============================================================

    with st.form("risk_assessment_form"):

        # ========================================================
        # BASIC INFORMATION (AUTO-SYNCED)
        # ========================================================

        profile = st.session_state.get("profile", {})
        default_age = int(profile.get("age", 25)) if profile.get("age", 0) >= 18 else 25
        default_income = int(profile.get("monthly_income", 30000) + profile.get("other_income", 0)) if profile.get("monthly_income", 0) > 0 else 30000
        default_expense = int(profile.get("monthly_expenses", 15000)) if profile.get("monthly_expenses", 0) > 0 else 15000

        st.info(f"🔗 **Synced with Profile:** Age: **{default_age}** | Monthly Income: **₹{default_income:,.0f}** | Expenses: **₹{default_expense:,.0f}** | Savings: **₹{default_income - default_expense:,.0f}**")

        with st.expander("✏️ Adjust Personal Financial Numbers (Optional)", expanded=False):
            col1, col2, col3 = st.columns(3)
            with col1:
                age = st.number_input(
                    "Your Age",
                    min_value=18,
                    max_value=100,
                    value=default_age,
                )
            with col2:
                income = st.number_input(
                    "Monthly Income (₹)",
                    min_value=0,
                    value=default_income,
                )
            with col3:
                monthly_expense = st.number_input(
                    "Monthly Expenses (₹)",
                    min_value=0,
                    value=default_expense,
                )

        # ========================================================
        # INVESTMENT EXPERIENCE
        # ========================================================

        st.markdown(
            '<div class="section-header">Investment Experience</div>',
            unsafe_allow_html=True,
        )

        investment_category = st.radio(
            "Investment Experience",
            ["Beginner", "Intermediate"],
            horizontal=True,
        )

        st.write("")

        # ========================================================
        # BEGINNER
        # ========================================================

        if investment_category == "Beginner":

            col_a, col_b = st.columns(2)

            with col_a:

                market_reaction = st.radio(
                    "If ₹10,000 becomes ₹8,000 after one month, "
                    "what will you do?",
                    [
                        "Withdraw all my money",
                        "Withdraw some money",
                        "Wait for it to recover",
                        "Invest more because prices are lower",
                    ],
                )

                goal = st.radio(
                    "What is your investment goal?",
                    [
                        "Saving money safely",
                        "Building long-term wealth",
                        "Generating higher returns",
                        "Protecting money from inflation",
                    ],
                )

                investment_period = st.radio(
                    "How long can you stay invested?",
                    [
                        "Less than 1 year",
                        "1-3 years",
                        "3-5 years",
                        "More than 5 years",
                    ],
                )

            with col_b:

                risk_capacity = st.radio(
                    "Maximum temporary loss you can tolerate",
                    [
                        "Up to 5%",
                        "Around 10%",
                        "Around 20%",
                        "More than 30%",
                    ],
                )

                income_stability = st.radio(
                    "Income Stability",
                    [
                        "Unstable",
                        "Somewhat stable",
                        "Stable",
                        "Very stable",
                    ],
                )

        # ========================================================
        # INTERMEDIATE
        # ========================================================

        else:

            col_a, col_b = st.columns(2)

            with col_a:

                products_used = st.multiselect(
                    "Products you've invested in",
                    [
                        "Fixed Deposits",
                        "Gold",
                        "Mutual Funds",
                        "Stocks",
                        "ETFs",
                        "Government Bonds",
                    ],
                )

                market_reaction = st.radio(
                    "If your portfolio falls by 20%, "
                    "what would you do?",
                    [
                        "Sell everything",
                        "Sell some investments",
                        "Hold my investments",
                        "Invest more",
                    ],
                )

                return_preference = st.radio(
                    "Preferred Returns",
                    [
                        "Stable but lower returns",
                        "Balanced growth",
                        "Higher returns with higher risk",
                    ],
                )

            with col_b:

                review_frequency = st.radio(
                    "Portfolio Review Frequency",
                    [
                        "Rarely",
                        "Every few months",
                        "Monthly",
                        "Weekly",
                    ],
                )

                investment_period = st.radio(
                    "Investment Horizon",
                    [
                        "1-3 years",
                        "3-5 years",
                        "5-10 years",
                        "More than 10 years",
                    ],
                )

                goal = "Building long-term wealth"

        # ========================================================
        # SUBMIT
        # ========================================================

        st.write("")

        submitted = st.form_submit_button(
            "Analyze My Risk Profile"
        )

        # ========================================================
        # RETURN USER DATA
        # ========================================================

        if submitted:

            user_data = {
                "age": age,
                "income": income,
                "monthly_expense": monthly_expense,
                "investment_category": investment_category,
                "goal": goal,
                "investment_period": investment_period,
                "market_reaction": market_reaction,
            }

            if investment_category == "Beginner":

                user_data.update(
                    {
                        "risk_capacity": risk_capacity,
                        "income_stability": income_stability,
                    }
                )

            else:

                user_data.update(
                    {
                        "products_used": products_used,
                        "return_preference": return_preference,
                        "review_frequency": review_frequency,
                    }
                )

            return user_data

    return None