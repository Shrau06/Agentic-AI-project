import os
from dotenv import load_dotenv
from tools.financial_tool import calculate_financial_metrics

load_dotenv()


def get_llms():
    """Return a priority-ordered list of candidate LLMs across providers."""
    llms = []
    groq_key = os.getenv("GROQ_API_KEY") or os.getenv("Groq_API")
    if groq_key:
         # pyrefly: ignore [missing-import]
        from langchain_groq import ChatGroq
        for model_name in [
            "llama-3.3-70b-versatile",
            "llama3-70b-8192",
            "mixtral-8x7b-32768",
            "openai/gpt-oss-120b"
        ]:
            try:
                llms.append(ChatGroq(model=model_name, api_key=groq_key, temperature=0.3, timeout=10))
            except Exception:
                pass

    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        # pyrefly: ignore [missing-import]
        from langchain_google_genai import ChatGoogleGenerativeAI
        for model_name in ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro"]:
            try:
                llms.append(ChatGoogleGenerativeAI(model=model_name, google_api_key=gemini_key, temperature=0.3, timeout=10))
            except Exception:
                pass

    return llms


def extract_clean_text(content):
    """Extract clean markdown text string from model content blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and "text" in item:
                parts.append(item["text"])
        if parts:
            return "\n".join(parts)
    if isinstance(content, dict) and "text" in content:
        return content["text"]
    return str(content)


def generate_financial_report(metrics_or_profile, goal=None):
    """
    Generate an in-depth AI Financial Health Analysis report.
    Accepts either a calculated metrics dict or a raw user profile dict.
    """
    # If a full profile is provided, calculate metrics automatically
    if "monthly_income" in metrics_or_profile:
        profile = metrics_or_profile
        metrics = calculate_financial_metrics(profile)
        if goal is None:
            goal = profile.get("goal", "Retirement")
    else:
        metrics = metrics_or_profile
        if goal is None:
            goal = "Retirement"

    # Safe defaults for all metrics
    income = metrics.get("income", 85000)
    expense = metrics.get("expense", 35000)
    monthly_savings = metrics.get("monthly_savings", 40000)
    current_savings = metrics.get("current_savings", 250000)
    loan_amount = metrics.get("loan_amount", 300000)
    monthly_emi = metrics.get("monthly_emi", 12000)
    savings_rate = metrics.get("savings_rate", 42.1)
    expense_ratio = metrics.get("expense_ratio", 36.8)
    debt_ratio = metrics.get("debt_ratio", 12.6)
    emergency_fund = metrics.get("emergency_fund", 7.1)
    savings_status = metrics.get("savings_status", "Good")
    expense_status = metrics.get("expense_status", "Good")
    debt_status = metrics.get("debt_status", "Good")
    emergency_status = metrics.get("emergency_status", "Good")

    system_prompt = f"""You are WealthLens AI, an expert certified financial advisor.

Analyze the user's financial profile and generate a comprehensive diagnostic report.

### User Financial Profile:
- Monthly Income: ₹{income:,.0f}
- Monthly Expenses: ₹{expense:,.0f}
- Monthly Savings: ₹{monthly_savings:,.0f}
- Current Liquid Savings: ₹{current_savings:,.0f}
- Outstanding Loan Amount: ₹{loan_amount:,.0f}
- Monthly EMI: ₹{monthly_emi:,.0f}
- Savings Rate: {savings_rate}% (Status: {savings_status})
- Expense Ratio: {expense_ratio}% (Status: {expense_status})
- Debt-to-Income Ratio: {debt_ratio}% (Status: {debt_status})
- Emergency Fund Buffer: {emergency_fund} months of expenses (Status: {emergency_status})
- Primary Financial Goal: {goal}

### Generate your report strictly with the following clear markdown structure:
# 📊 Financial Health Diagnostic Report
## 1. Overall Financial Health Assessment
- Financial Health Score: (0-100)
- Current Health Tier: (Excellent / Good / Needs Improvement)
- Executive Summary (2-3 concise paragraphs)

## 2. Key Financial Strengths
- Exactly 3 specific bullet points highlighting what the user is doing well.

## 3. Financial Vulnerabilities & Risks
- Exactly 3 bullet points identifying potential risks or areas needing improvement.

## 4. Immediate Action Priorities
- 3 prioritized, numbered steps the user should execute in the next 30-90 days.

## 5. Personalized Advisory & Growth Strategy
- Practical wealth-building recommendations tailored to their goal ({goal}).
- Guidance on emergency fund allocation, debt optimization, and savings deployment.

## 6. Professional Disclaimer
- Educational financial analysis disclaimer.
"""

    prompt_message = "Generate my complete financial health analysis and strategic advisory report."

    # Try all configured LLM candidates
    for llm in get_llms():
        try:
            response = llm.invoke(f"{system_prompt}\n\nHuman: {prompt_message}")
            clean_text = extract_clean_text(response.content)
            if len(clean_text.strip()) > 100:
                return clean_text
        except Exception:
            continue

    # Fallback to analytical template if all LLM endpoints are unreachable
    health_score = 100
    if savings_rate < 20:
        health_score -= 20
    if expense_ratio > 70:
        health_score -= 20
    if debt_ratio > 40:
        health_score -= 20
    if current_savings < expense * 6:
        health_score -= 20
    health_score = max(20, health_score)

    tier = "Excellent" if health_score >= 80 else ("Good" if health_score >= 60 else "Needs Improvement")

    return f"""# 📊 Financial Health Diagnostic Report
## 1. Overall Financial Health Assessment
- **Financial Health Score:** {health_score}/100
- **Current Health Tier:** {tier}
- **Executive Summary:** With a total monthly income of ₹{income:,.0f} and monthly expenses of ₹{expense:,.0f}, you maintain an effective savings rate of {savings_rate}%. Your debt obligations (monthly EMI ₹{monthly_emi:,.0f}) represent {debt_ratio}% of your income, which is categorized as **{debt_status}**. Your liquid reserve covers approximately {emergency_fund} months of ongoing expenses.

## 2. Key Financial Strengths
- **Consistent Savings Inflow:** Generating ₹{monthly_savings:,.0f} monthly towards your net worth.
- **Controlled Expense Ratio:** Living costs consume {expense_ratio}% of cash inflow, rated **{expense_status}**.
- **Reserve Buffer:** Maintaining ₹{current_savings:,.0f} in liquid assets for emergency security.

## 3. Financial Vulnerabilities & Risks
- **Goal Capitalization:** Reaching **{goal}** requires systematic allocation rather than uninvested cash.
- **Debt Service:** Outstanding debt of ₹{loan_amount:,.0f} incurs ongoing interest cost.
- **Inflation Protection:** Idle cash reserves must be protected against inflation through growth investments.

## 4. Immediate Action Priorities
1. Deploy monthly surplus (₹{monthly_savings:,.0f}) into disciplined monthly SIPs and equity index funds.
2. Maintain at least 6 months of emergency reserves in high-yield liquid instruments.
3. Accelerate repayment on high-interest loan tranches to lower your {debt_ratio}% debt-to-income ratio.

## 5. Personalized Advisory & Growth Strategy
- **Target Goal:** Tailored execution roadmap to achieve your **{goal}** milestone.
- **Asset Allocation:** Balance asset growth across 60% equities, 25% debt/fixed income, and 15% liquid buffer.

## 6. Professional Disclaimer
*This diagnostic analysis is generated for educational and planning purposes. Consult a licensed SEBI registered financial advisor for personalized wealth management.*
"""
