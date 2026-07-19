# import streamlit as st
# import matplotlib.pyplot as plt

# from member4.wealth_tool import calculate_sip, calculate_growth

# # -----------------------------
# # Page Configuration
# # -----------------------------
# st.set_page_config(
#     page_title="WealthLensAI",
#     page_icon="💰",
#     layout="wide"
# )

# # -----------------------------
# # Title
# # -----------------------------
# st.title("💰 WealthLensAI")
# st.write("### Smart Wealth Planning Calculator")

# st.divider()

# # -----------------------------
# # User Inputs
# # -----------------------------
# investment = st.number_input(
#     "Monthly Investment (₹)",
#     min_value=0,
#     value=5000,
#     step=500
# )

# rate = st.number_input(
#     "Expected Annual Return (%)",
#     min_value=1.0,
#     max_value=30.0,
#     value=12.0,
#     step=0.5
# )

# years = st.number_input(
#     "Investment Period (Years)",
#     min_value=1,
#     max_value=40,
#     value=10,
#     step=1
# )

# goal = st.number_input(
#     "Financial Goal (₹)",
#     min_value=100000,
#     value=2000000,
#     step=100000
# )

# # -----------------------------
# # Button
# # -----------------------------
# if st.button("🚀 Calculate Wealth"):

#     total, future, profit = calculate_sip(
#         investment,
#         rate,
#         years
#     )

#     st.divider()

#     st.subheader("📊 Investment Summary")

#     col1, col2, col3 = st.columns(3)

#     col1.metric(
#         "Total Investment",
#         f"₹{total:,.0f}"
#     )

#     col2.metric(
#         "Future Wealth",
#         f"₹{future:,.0f}"
#     )

#     col3.metric(
#         "Estimated Profit",
#         f"₹{profit:,.0f}"
#     )

#     st.divider()

#     # -----------------------------
#     # Goal Checker
#     # -----------------------------
#     st.subheader("🎯 Goal Status")

#     if future >= goal:

#         st.success("🎉 Congratulations! Your financial goal can be achieved.")

#     else:

#         difference = goal - future

#         st.error("❌ Goal Not Achieved")

#         st.write(
#             f"You need approximately ₹{difference:,.0f} more to achieve your goal."
#         )

#     st.divider()

#     # -----------------------------
#     # Wealth Growth Graph
#     # -----------------------------
#     st.subheader("📈 Wealth Growth")

#     growth = calculate_growth(
#         investment,
#         rate,
#         years
#     )

#     year_list = list(range(1, years + 1))

#     fig, ax = plt.subplots(figsize=(8,5))

#     ax.plot(
#         year_list,
#         growth,
#         marker="o",
#         linewidth=2
#     )

#     ax.set_title("Investment Growth Over Time")

#     ax.set_xlabel("Years")

#     ax.set_ylabel("Future Wealth (₹)")

#     ax.grid(True)

#     st.pyplot(fig)

#     st.divider()

#     st.info(
#         "📌 This calculation assumes a fixed annual return. "
#         "Actual market returns may vary."
#     )


from member4.wealth_ui import wealth_dashboard

wealth_dashboard()