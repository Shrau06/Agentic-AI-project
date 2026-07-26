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
            "💰 WealthLensAI<br/>Wealth Planning Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1,20)
    )


    # Investment Summary

    content.append(
        Paragraph(
            "🎯 Financial Goal",
            styles["Heading2"]
        )
    )


    goal_table = Table(
        [
            ["Goal Amount", data["goal"]]
        ]
    )


    goal_table.setStyle(
        TableStyle(
            [
                ("GRID",(0,0),(-1,-1),0.5,None),
            ]
        )
    )


    content.append(goal_table)

    content.append(
        Spacer(1,20)
    )


    # Investment Details

    content.append(
        Paragraph(
            "💵 Investment Details",
            styles["Heading2"]
        )
    )


    investment_table = Table(
        [
            ["Monthly Investment", data["investment"]],
            ["Duration", data["years"]],
        ]
    )


    investment_table.setStyle(
        TableStyle(
            [
                ("GRID",(0,0),(-1,-1),0.5,None),
            ]
        )
    )


    content.append(investment_table)

    content.append(
        Spacer(1,20)
    )


    # Wealth Calculation

    content.append(
        Paragraph(
            "📊 Wealth Calculation",
            styles["Heading2"]
        )
    )


    wealth_table = Table(
        [
            ["Total Investment", data["total"]],
            ["Future Wealth", data["future"]],
            ["Estimated Profit", data["profit"]],
        ]
    )


    wealth_table.setStyle(
        TableStyle(
            [
                ("GRID",(0,0),(-1,-1),0.5,None),
            ]
        )
    )


    content.append(wealth_table)

    content.append(
        Spacer(1,20)
    )


    # Goal Status

    content.append(
        Paragraph(
            "🎯 Goal Achievement Status",
            styles["Heading2"]
        )
    )


    content.append(
        Paragraph(
            data["status"],
            styles["Normal"]
        )
    )


    content.append(
        Spacer(1,20)
    )


    # AI Advice

    content.append(
        Paragraph(
            "🤖 AI Wealth Advice",
            styles["Heading2"]
        )
    )


    content.append(
        Paragraph(
            data["advice"],
            styles["Normal"]
        )
    )


    pdf.build(content)


    return filename