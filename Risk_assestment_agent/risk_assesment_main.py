
from dotenv import load_dotenv

import streamlit as st

from langchain_google_genai import ChatGoogleGenerativeAI

from risk_agent import run_risk_assessment



load_dotenv()




llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
)



result = run_risk_assessment(llm)

if result:

    st.success("Risk Assessment Completed Successfully!")
    st.subheader("Risk Assessment")
    st.subheader("Suggested Portfolio")
    st.subheader("AI Recommendation")
    st.markdown(result["ai_recommendation"])