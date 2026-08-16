from langchain_core.tools import tool


@tool
def risk_tool(user_data: dict) -> dict:
    """Calculate the user's investment risk score and risk profile."""
    score = 0
    factors = {}

    age = user_data["age"]
    income = user_data["income"]
    expense = user_data["monthly_expense"]
    category = user_data["investment_category"]

    if age <= 30:
        age_score = 15
    elif age <= 45:
        age_score = 10
    else:
        age_score = 5

    factors["Age"] = age_score
    score += age_score

    savings = income - expense

    if savings >= 50000:
        savings_score = 20
    elif savings >= 25000:
        savings_score = 15
    elif savings >= 10000:
        savings_score = 10
    else:
        savings_score = 5

    factors["Savings"] = savings_score
    score += savings_score

    if category == "Beginner":
        max_score = 115
        market_scores = {
            "Withdraw all my money": 5,
            "Withdraw some money": 10,
            "Wait for it to recover": 15,
            "Invest more because prices are lower": 20,
        }
        horizon_scores = {
            "Less than 1 year": 5,
            "1-3 years": 10,
            "3-5 years": 15,
            "More than 5 years": 20,
        }
        risk_capacity_scores = {
            "Up to 5%": 5,
            "Around 10%": 10,
            "Around 20%": 15,
            "More than 30%": 20,
        }
        stability_scores = {
            "Unstable": 5,
            "Somewhat stable": 10,
            "Stable": 15,
            "Very stable": 20,
        }

        values = {
            "Market Behaviour": market_scores.get(user_data.get("market_reaction"), 10),
            "Investment Horizon": horizon_scores.get(user_data.get("investment_period"), 10),
            "Risk Capacity": risk_capacity_scores.get(user_data.get("risk_capacity"), 10),
            "Income Stability": stability_scores.get(user_data.get("income_stability"), 10),
        }
    else:
        max_score = 135
        products_score = min(len(user_data.get("products_used", [])) * 4, 20)
        market_scores = {
            "Sell everything": 5,
            "Sell some investments": 10,
            "Hold my investments": 15,
            "Invest more": 20,
        }
        return_scores = {
            "Stable but lower returns": 5,
            "Balanced growth": 15,
            "Higher returns with higher risk": 20,
        }
        review_scores = {
            "Rarely": 5,
            "Every few months": 10,
            "Monthly": 15,
            "Weekly": 20,
        }
        horizon_scores = {
            "1-3 years": 5,
            "3-5 years": 10,
            "5-10 years": 15,
            "More than 10 years": 20,
        }

        values = {
            "Investment Experience": products_score,
            "Market Behaviour": market_scores.get(user_data.get("market_reaction"), 10),
            "Return Preference": return_scores.get(user_data.get("return_preference"), 10),
            "Review Frequency": review_scores.get(user_data.get("review_frequency"), 10),
            "Investment Horizon": horizon_scores.get(user_data.get("investment_period"), 10),
        }

    factors.update(values)
    score += sum(values.values())

    risk_percentage = round((score / max_score) * 100, 2)

    if risk_percentage < 40:
        profile = "Conservative"
    elif risk_percentage < 70:
        profile = "Moderate"
    else:
        profile = "Aggressive"

    return {
        "risk_score": score,
        "maximum_score": max_score,
        "risk_percentage": risk_percentage,
        "risk_profile": profile,
        "factor_scores": factors,
        "monthly_savings": savings,
        "risk_level": profile,
    }