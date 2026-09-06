import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

try:
    from .risk_agent import run_risk_assessment, get_risk_llm
    from .ui import risk_assessment_ui
except ImportError:
    from Risk_assestment_agent.risk_agent import run_risk_assessment, get_risk_llm
    from Risk_assestment_agent.ui import risk_assessment_ui

load_dotenv()


def extract_clean_text(content):
    """Extract clean text string from model content blocks or message payloads."""
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


def show_risk_assessment():
    llm = get_risk_llm()

    user_data = risk_assessment_ui()

    if user_data:
        with st.spinner("🤖 WealthLens AI Agent is analyzing your profile..."):
            try:
                result = run_risk_assessment(llm, user_data)
                st.session_state["risk_assessment_result"] = result

                if result and isinstance(result, dict):
                    risk_result = result.get("risk_result")
                    if risk_result:
                        st.session_state["risk_level"] = risk_result.get("risk_level")
                        st.session_state["risk_score"] = risk_result.get("risk_score")
                        st.session_state["risk_percentage"] = risk_result.get("risk_percentage")
            except Exception as e:
                st.error(f"Error running risk assessment: {e}")
                st.session_state["risk_assessment_result"] = None

    result = st.session_state.get("risk_assessment_result")
    if result and isinstance(result, dict):
        st.success("Risk Assessment Completed Successfully!")
        st.subheader("🤖 WealthLens AI Agent Recommendation")

        clean_report = extract_clean_text(result.get("agent_response", ""))
        st.markdown(clean_report)

        with st.expander("🔍 View Agent Tool Execution", expanded=False):
            st.markdown("### 🛠️ Agent Autonomous Tool Execution Trace")
            
            # 1. Risk Tool Execution
            risk_res = result.get("risk_result")
            if risk_res:
                st.markdown("#### 1️⃣ `risk_tool` Execution Output")
                st.write(f"**Calculated Risk Level:** `{risk_res.get('risk_level', 'Moderate')}` | **Risk Score:** `{risk_res.get('risk_score', 'N/A')}/{risk_res.get('maximum_score', 115)}` ({risk_res.get('risk_percentage', 0)}%)")
                if "factor_scores" in risk_res:
                    st.write("**Factor Breakdown:**")
                    st.json(risk_res["factor_scores"])
                else:
                    st.json(risk_res)
                st.divider()

            # 2. Portfolio Tool Execution
            port_res = result.get("portfolio_result")
            if port_res:
                st.markdown("#### 2️⃣ `portfolio_tool` Execution Output")
                st.write(f"**Strategy:** `{port_res.get('portfolio_type', 'N/A')}` | **Expected Return:** `{port_res.get('expected_return', 'N/A')}` | **Horizon:** `{port_res.get('investment_horizon', 'N/A')}`")
                st.write("**Asset Allocation Breakdown (%):**")
                st.json(port_res.get("allocation", port_res))
                st.divider()

            # 3. LLM Message Sequence Trace
            messages = result.get("messages", [])
            if messages:
                st.markdown("#### 3️⃣ LLM Message Exchange Trace")
                for i, message in enumerate(messages):
                    msg_type = getattr(message, "type", None)
                    if not msg_type and isinstance(message, dict):
                        msg_type = message.get("role", f"Step {i+1}")
                    
                    st.write(f"**Step {i+1} — {str(msg_type).upper()}:**")
                    msg_content = getattr(message, "content", "") if hasattr(message, "content") else message.get("content", "")
                    if msg_content:
                        cleaned = extract_clean_text(msg_content)
                        if cleaned.strip():
                            st.code(cleaned, language="markdown")
                        else:
                            st.caption("(Tool call executed)")
                    st.divider()


if __name__ == "__main__":
    st.set_page_config(
        page_title="WealthLens AI - Autonomous Risk Assessment",
        layout="centered",
    )
    show_risk_assessment()