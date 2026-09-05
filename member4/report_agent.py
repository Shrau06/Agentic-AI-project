def report_agent(
    goal,
    monthly_investment,
    years,
    total_investment,
    future_wealth,
    profit,
    goal_status
):

    if future_wealth >= goal:

        advice = """
✅ Congratulations!

Your current investment strategy has the
potential to achieve your financial goal.

Continue investing regularly and review
your plan periodically.
"""


    else:

        difference = goal - future_wealth

        advice = f"""
⚠️ Your current plan may not fully achieve
your target.

Additional wealth required:

₹{difference:,.0f}


Suggestions:

• Increase monthly investment

• Extend investment duration

• Review your financial goal
"""


    return {
        "goal": f"₹{goal:,.0f}",
        "investment": f"₹{monthly_investment:,.0f}",
        "years": f"{years} Years",
        "total": f"₹{total_investment:,.0f}",
        "future": f"₹{future_wealth:,.0f}",
        "profit": f"₹{profit:,.0f}",
        "status": goal_status,
        "advice": advice
    }