def calculate_financial_metrics(profile):

    income = profile["monthly_income"] + profile["other_income"]
    expense = profile["monthly_expenses"]
    monthly_savings = profile["monthly_savings"]
    current_savings = profile["current_savings"]
    loan_amount = profile["loan_amount"]
    monthly_emi = profile["monthly_emi"]

    savings_rate = 0
    expense_ratio = 0
    debt_ratio = 0
    emergency_fund = 0

    if income > 0:
        savings_rate = (monthly_savings / income) * 100
        expense_ratio = (expense / income) * 100
        debt_ratio = (monthly_emi / income) * 100

    if expense > 0:
        emergency_fund = current_savings / expense

    if savings_rate >= 30:
        savings_status = "Excellent"
    elif savings_rate >= 20:
        savings_status = "Good"
    elif savings_rate >= 10:
        savings_status = "Average"
    else:
        savings_status = "Poor"

    if expense_ratio <= 50:
        expense_status = "Excellent"
    elif expense_ratio <= 70:
        expense_status = "Good"
    elif expense_ratio <= 85:
        expense_status = "Average"
    else:
        expense_status = "Poor"

    if debt_ratio <= 20:
        debt_status = "Excellent"
    elif debt_ratio <= 35:
        debt_status = "Good"
    elif debt_ratio <= 50:
        debt_status = "Average"
    else:
        debt_status = "Poor"

    if emergency_fund >= 6:
        emergency_status = "Excellent"
    elif emergency_fund >= 3:
        emergency_status = "Good"
    elif emergency_fund >= 1:
        emergency_status = "Average"
    else:
        emergency_status = "Poor"

    return {
        "income": income,
        "expense": expense,
        "monthly_savings": monthly_savings,
        "current_savings": current_savings,
        "loan_amount": loan_amount,
        "monthly_emi": monthly_emi,

        "savings_rate": round(savings_rate, 2),
        "expense_ratio": round(expense_ratio, 2),
        "debt_ratio": round(debt_ratio, 2),
        "emergency_fund": round(emergency_fund, 2),

        "savings_status": savings_status,
        "expense_status": expense_status,
        "debt_status": debt_status,
        "emergency_status": emergency_status
    }