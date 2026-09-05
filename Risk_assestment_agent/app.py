
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from risk_agent import run_risk_assessment
from ui import risk_assessment_ui

load_dotenv()

st.set_page_config(
    page_title="WealthLens AI - Autonomous Risk Assessment",
    page_icon="💼",
    layout="centered",
)


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


llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)

user_data = risk_assessment_ui()

if user_data:
    with st.spinner("🤖 WealthLens AI Agent is analyzing your profile..."):
        result = run_risk_assessment(llm, user_data)

        # Extract risk assessment result and store it in session state
        risk_result = result.get("risk_result")

        if risk_result:
            st.session_state["risk_level"] = risk_result.get("risk_level")
            st.session_state["risk_score"] = risk_result.get("risk_score")
            st.session_state["risk_percentage"] = risk_result.get("risk_percentage")

    st.success("Risk Assessment Completed Successfully!")

    st.subheader("🤖 WealthLens AI Agent Recommendation")

    # Clean the agent response text before rendering
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