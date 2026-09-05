from agents.research_agent import generate_research_report

stock_info = """
Company: Microsoft
Price: 500
PE Ratio: 35
"""

news = """
Microsoft launches new AI products.
Microsoft reports strong earnings.
"""

report = generate_research_report(
    stock_info,
    news
)

print(report)