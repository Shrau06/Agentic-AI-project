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

        with st.expander("🔍 View Agent Tool Execution"):
            for message in result.get("messages", []):
                msg_type = getattr(message, "type", "unknown")
                st.write(f"**Message Type:** {msg_type}")

                msg_content = getattr(message, "content", "")
                if msg_content:
                    cleaned_msg = extract_clean_text(msg_content)

                    if cleaned_msg.strip():
                        st.text(cleaned_msg)
                    else:
                        st.caption("(Tool call execution message)")

                st.divider()


if __name__ == "__main__":
    st.set_page_config(
        page_title="WealthLens AI - Autonomous Risk Assessment",
        layout="centered",
    )
    show_risk_assessment()