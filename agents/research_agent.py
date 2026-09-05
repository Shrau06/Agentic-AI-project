import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def generate_research_report(
    investment_type,
    investment_info,
    news_text=""
):

    prompt = f"""
You are an experienced Financial Market Research Analyst.

Your task is to analyze the investment using ONLY the information provided below.

Investment Type:
{investment_type}

Investment Information:
{investment_info}

Latest News:
{news_text}

Instructions:

• Use ONLY the provided information.
• Do NOT invent company details or financial figures.
• If some information is unavailable, mention that it is not available.
• Generate the report in clean Markdown.
• Use headings and bullet points.
• Keep the report around 400–600 words.
• Make the report professional and easy to understand.


==============================
IF Investment Type = STOCK
==============================

Generate the following sections:

# Company Overview
Briefly describe the company.

# Business & Industry
Explain the company's business and industry.

# Financial Snapshot
Summarize:
- Current Price
- Market Cap
- PE Ratio
- 52 Week High
- 52 Week Low

# Strengths
Mention key strengths.

# Risks
Mention possible risks.

# Recent News Impact
Explain how the latest news may affect the company.

# Market Sentiment
State whether the sentiment is Positive, Neutral or Negative and explain why.

# Long-Term Outlook
Explain future growth opportunities.

# Overall View
Choose one:
- Positive
- Neutral
- Cautious

Explain your reasoning.

# Overall Rating
Give a rating out of 10.


==============================
IF Investment Type = ETF
==============================

Generate the following sections:

# ETF Overview

# Investment Objective

# Financial Snapshot

# Advantages

# Risks

# Suitable Investors

# Market Outlook

# Overall View
Choose one:
- Positive
- Neutral
- Cautious

Explain your reasoning.

# Overall Rating
Give a rating out of 10.


==============================
IF Investment Type = Mutual Fund
==============================

Generate the following sections:

# Fund Overview

# Fund House

# Category

# Investment Objective

# Strengths

# Risks

# Suitable Investors

# Long-Term Outlook

# Overall View
Choose one:
- Positive
- Neutral
- Cautious

Explain your reasoning.

# Overall Rating
Give a rating out of 10.


Finally, add the following section:

---
### Disclaimer

This report is AI-generated for educational and research purposes only.
It should not be considered financial or investment advice.
Always conduct your own research or consult a qualified financial advisor before making investment decisions.
"""

    response = model.generate_content(prompt)

    return response.text