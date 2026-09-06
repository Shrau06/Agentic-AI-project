from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(data, filename="WealthLensAI_Report.pdf"):
    pdf = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    content = []

    # Title
    content.append(
        Paragraph(
            "WealthLens AI - Comprehensive Financial & Wealth Planning Report",
            styles["Title"]
        )
    )
    content.append(Spacer(1, 20))

    # Financial & Risk Diagnostics
    diag_rows = []
    if data.get("health_score") and data.get("health_score") != "N/A":
        diag_rows.append(["Financial Health Score", str(data["health_score"])])
    if data.get("risk_level") and data.get("risk_level") != "Not Assessed":
        diag_rows.append(["Risk Assessment Profile", str(data["risk_level"])])

    if diag_rows:
        content.append(
            Paragraph(
                "Executive Health & Risk Summary",
                styles["Heading2"]
            )
        )
        diag_table = Table(diag_rows)
        diag_table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, None)]))
        content.append(diag_table)
        content.append(Spacer(1, 20))

    # Financial Goal
    content.append(
        Paragraph(
            "Financial Goal",
            styles["Heading2"]
        )
    )
    goal_table = Table(
        [
            ["Goal Amount", str(data.get("goal", "")).replace("₹", "Rs. ")]
        ]
    )
    goal_table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, None)]))
    content.append(goal_table)
    content.append(Spacer(1, 20))

    # Investment Details
    content.append(
        Paragraph(
            "Investment Details",
            styles["Heading2"]
        )
    )
    investment_table = Table(
        [
            ["Monthly Investment", str(data.get("investment", "")).replace("₹", "Rs. ")],
            ["Duration", str(data.get("years", ""))],
        ]
    )
    investment_table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, None)]))
    content.append(investment_table)
    content.append(Spacer(1, 20))

    # Wealth Calculation
    content.append(
        Paragraph(
            "Wealth Calculation & Projections",
            styles["Heading2"]
        )
    )
    wealth_table = Table(
        [
            ["Total Investment", str(data.get("total", "")).replace("₹", "Rs. ")],
            ["Future Wealth", str(data.get("future", "")).replace("₹", "Rs. ")],
            ["Estimated Profit", str(data.get("profit", "")).replace("₹", "Rs. ")],
        ]
    )
    wealth_table.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.5, None)]))
    content.append(wealth_table)
    content.append(Spacer(1, 20))

    # Goal Status
    content.append(
        Paragraph(
            "Goal Achievement Status",
            styles["Heading2"]
        )
    )
    status_text = str(data.get("status", "")).replace("✅", "[ACHIEVABLE]").replace("⚠️", "[ATTENTION]").replace("₹", "Rs. ")
    content.append(
        Paragraph(
            status_text,
            styles["Normal"]
        )
    )
    content.append(Spacer(1, 20))

    # AI Advice
    content.append(
        Paragraph(
            "AI Wealth Advisor Insights",
            styles["Heading2"]
        )
    )

    advice_text = data.get("advice", "")
    for line in str(advice_text).split("\n"):
        clean_line = line.strip().replace("₹", "Rs. ").replace("•", "-")
        if clean_line:
            content.append(Paragraph(clean_line, styles["Normal"]))
            content.append(Spacer(1, 4))

    pdf.build(content)
    return filename