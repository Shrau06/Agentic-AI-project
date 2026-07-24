
from dotenv import load_dotenv

import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI

from risk_agent import run_risk_assessment


# ------------------------------------
# Load Environment Variables
# ------------------------------------

load_dotenv()


# ------------------------------------
# Initialize Gemini
# ------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
)


# ------------------------------------
# Run Application
# ------------------------------------

result = run_risk_assessment(llm)

if result:

    st.success("Risk Assessment Completed Successfully!")

    st.subheader("Risk Assessment")

    # st.json(result["risk_assessment"])

    st.subheader("Suggested Portfolio")

    # st.json(result["portfolio"])

    st.subheader("AI Recommendation")

    st.markdown(result["ai_recommendation"])