from langchain_core.tools import tool


@tool
def portfolio_tool(user_data: dict, risk_result: dict) -> dict:
    """
    Generates a recommended investment portfolio
    based on the user's risk profile.
    """

    profile = risk_result["risk_profile"]
    goal = user_data["goal"]
    horizon = user_data["investment_period"]

  

    if profile == "Conservative":

        allocation = {
            "Debt Funds": 45,
            "Fixed Deposits": 25,
            "Gold": 15,
            "Equity": 10,
            "Cash": 5
        }

        expected_return = "6% - 8% annually"

    elif profile == "Moderate":

        allocation = {
            "Equity": 50,
            "Debt Funds": 25,
            "Gold": 10,
            "ETFs": 10,
            "Cash": 5
        }

        expected_return = "8% - 12% annually"

    else:

        allocation = {
            "Equity": 70,
            "ETFs": 15,
            "Gold": 10,
            "Cash": 5
        }

        expected_return = "12% - 15% annually"

   

    if goal == "Saving money safely":

        allocation = {
            "Fixed Deposits": 40,
            "Debt Funds": 35,
            "Gold": 15,
            "Cash": 10
        }

        expected_return = "5% - 7% annually"

    elif goal == "Protecting money from inflation":

        allocation["Gold"] = max(allocation.get("Gold", 0), 20)

  

    if horizon == "Less than 1 year":

        allocation = {
            "Liquid Funds": 40,
            "Fixed Deposits": 35,
            "Cash": 25
        }

        expected_return = "4% - 6% annually"

    return {

        "portfolio_type": profile,

        "allocation": allocation,

        "expected_return": expected_return,

        "investment_horizon": horizon
    }