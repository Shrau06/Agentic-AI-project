def calculate_sip(monthly_investment, annual_return, years):

    monthly_rate = annual_return / 12 / 100
    months = years * 12

    future_value = monthly_investment * (
        ((1 + monthly_rate) ** months - 1)
        / monthly_rate
    ) * (1 + monthly_rate)

    total_investment = monthly_investment * months
    profit = future_value - total_investment

    return total_investment, future_value, profit


def calculate_growth(monthly_investment, annual_return, years):

    growth = []

    for year in range(1, years + 1):

        _, future, _ = calculate_sip(
            monthly_investment,
            annual_return,
            year
        )

        growth.append(future)

    return growth


def yearly_report(monthly_investment, annual_return, years):

    report = []

    for year in range(1, years + 1):

        total, future, profit = calculate_sip(
            monthly_investment,
            annual_return,
            year
        )

        report.append({
            "Year": year,
            "Investment": round(total),
            "Future Value": round(future),
            "Profit": round(profit)
        })

    return report


def calculate_compound_interest(principal, annual_rate, years):

    future_value = principal * ((1 + annual_rate / 100) ** years)

    interest = future_value - principal

    return principal, future_value, interest


def wealth_projection(monthly_investment, annual_return):

    projections = []

    for year in [5, 10, 15]:

        total, future, profit = calculate_sip(
            monthly_investment,
            annual_return,
            year
        )

        projections.append({
            "Years": year,
            "Total Investment": round(total),
            "Future Wealth": round(future),
            "Profit": round(profit)
        })

    return projections