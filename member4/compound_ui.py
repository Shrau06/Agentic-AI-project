import streamlit as st


def compound_interest_ui():

    st.header("📈 Compound Interest Calculator")

    principal = st.number_input(
    "Initial Investment (₹)",
    min_value=1000,
    value=50000,
    step=5000,
    key="compound_principal"
)

    rate = st.number_input(
    "Annual Interest Rate (%)",
    min_value=1.0,
    max_value=30.0,
    value=12.0,
    key="compound_rate"
)

    years = st.number_input(
    "Investment Duration (Years)",
    min_value=1,
    max_value=50,
    value=10,
    key="compound_years"
)

    frequency = st.selectbox(
    "Compounding Frequency",
    [
        "Yearly",
        "Half-Yearly",
        "Quarterly",
        "Monthly"
    ],
    key="compound_frequency"
)


    if st.button("Calculate Compound Interest"):

        if frequency == "Yearly":
            n = 1

        elif frequency == "Half-Yearly":
            n = 2

        elif frequency == "Quarterly":
            n = 4

        else:
            n = 12


        amount = principal * (
            (1 + rate / (100*n)) 
            ** (n * years)
        )


        interest = amount - principal


        col1, col2 = st.columns(2)


        col1.metric(
            "Future Amount",
            f"₹{amount:,.0f}"
        )


        col2.metric(
            "Interest Earned",
            f"₹{interest:,.0f}"
        )


        st.success(
            f"Your investment can grow to ₹{amount:,.0f} after {years} years."
        )