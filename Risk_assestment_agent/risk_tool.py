from langchain_core.tools import tool


@tool
def risk_tool(user_data: dict) -> dict:
    """
    Calculates the user's investment risk score
    and returns the corresponding risk profile.
    """

    score = 0
    factors = {}

    age = user_data["age"]
    income = user_data["income"]
    expense = user_data["monthly_expense"]
    category = user_data["investment_category"]

    # -------------------------------------------------
    # Age Score
    # -------------------------------------------------

    if age <= 30:
        factors["Age"] = 15

    elif age <= 45:
        factors["Age"] = 10

    else:
        factors["Age"] = 5

    score += factors["Age"]

    # -------------------------------------------------
    # Savings Score
    # -------------------------------------------------

    savings = income - expense

    if savings >= 50000:
        factors["Savings"] = 20

    elif savings >= 25000:
        factors["Savings"] = 15

    elif savings >= 10000:
        factors["Savings"] = 10

    else:
        factors["Savings"] = 5

    score += factors["Savings"]

    # ============================================================
    # BEGINNER
    # ============================================================

    if category == "Beginner":

        score += {
            "Withdraw all my money": 5,
            "Withdraw some money": 10,
            "Wait for it to recover": 15,
            "Invest more because prices are lower": 20
        }[user_data["market_reaction"]]

        score += {
            "Less than 1 year": 5,
            "1-3 years": 10,
            "3-5 years": 15,
            "More than 5 years": 20
        }[user_data["investment_period"]]

        score += {
            "Up to 5%": 5,
            "Around 10%": 10,
            "Around 20%": 15,
            "More than 30%": 20
        }[user_data["risk_capacity"]]

        score += {
            "Unstable": 5,
            "Somewhat stable": 10,
            "Stable": 15,
            "Very stable": 20
        }[user_data["income_stability"]]

    # ============================================================
    # INTERMEDIATE
    # ============================================================

    else:

        score += min(len(user_data["products_used"]) * 4, 20)

        score += {
            "Sell everything": 5,
            "Sell some investments": 10,
            "Hold my investments": 15,
            "Invest more": 20
        }[user_data["market_reaction"]]

        score += {
            "Stable but lower returns": 5,
            "Balanced growth": 15,
            "Higher returns with higher risk": 20
        }[user_data["return_preference"]]

        score += {
            "Rarely": 5,
            "Every few months": 10,
            "Monthly": 15,
            "Weekly": 20
        }[user_data["review_frequency"]]

        score += {
            "1-3 years": 5,
            "3-5 years": 10,
            "5-10 years": 15,
            "More than 10 years": 20
        }[user_data["investment_period"]]

    # -------------------------------------------------
    # Final Risk Profile
    # -------------------------------------------------

    risk_percentage = round((score / 115) * 100, 2)

    if risk_percentage < 40:
        profile = "Conservative"

    elif risk_percentage < 70:
        profile = "Moderate"

    else:
        profile = "Aggressive"

    return {
        "risk_score": score,
        "risk_percentage": risk_percentage,
        "risk_profile": profile,
        "factor_scores": factors
    }