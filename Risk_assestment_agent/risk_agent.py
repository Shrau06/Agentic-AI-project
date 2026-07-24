from ui import risk_assessment_ui
from risk_tool import risk_tool
from portfolio_tool import portfolio_tool
from prompts import RISK_ASSESSMENT_PROMPT


def run_risk_assessment(llm):

    
    user_data = risk_assessment_ui()

    if user_data is None:
        return None

    
    risk_result = risk_tool.invoke({
        "user_data": user_data
    })

 
    portfolio_result = portfolio_tool.invoke({
        "user_data": user_data,
        "risk_result": risk_result
    })

    prompt = RISK_ASSESSMENT_PROMPT.format(

        age=user_data["age"],
        income=user_data["income"],
        monthly_expense=user_data["monthly_expense"],
        investment_category=user_data["investment_category"],
        goal=user_data["goal"],
        investment_period=user_data["investment_period"],
        market_reaction=user_data["market_reaction"],

        risk_score=risk_result["risk_score"],
        risk_level=risk_result["risk_profile"],

        allocation=portfolio_result["allocation"],
        expected_return=portfolio_result["expected_return"]
    )

    
    response = llm.invoke(prompt)

    return {
        "user_profile": user_data,
        "risk_assessment": risk_result,
        "portfolio": portfolio_result,
        "ai_recommendation": response.content
    }