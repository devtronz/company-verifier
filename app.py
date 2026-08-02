import json
import streamlit as st
from google import genai

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="AI JobVerify",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI JobVerify")
st.caption("One Search. Verify Everything.")

# -----------------------
# API KEY
# -----------------------
API_KEY = st.secrets["GEMINI_API_KEY"]

client = genai.Client(api_key=API_KEY)

# -----------------------
# SEARCH BOX
# -----------------------
query = st.text_input(
    "Search",
    placeholder="Company name, website, recruiter email or job..."
)

analyze = st.button("🔍 Analyze", use_container_width=True)

# -----------------------
# ANALYSIS
# -----------------------
if analyze:

    if not query.strip():
        st.warning("Please enter a search query.")
        st.stop()

    with st.spinner("Analyzing..."):

        prompt = f"""
You are an AI Company Verification Assistant.

Analyze:

{query}

Return ONLY valid JSON.

{{
  "summary":"...",
  "trust_score":80,
  "risk":"Low",
  "recommendation":"Safe",
  "analysis":"..."
}}
"""

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            text = response.text.strip()

            text = text.replace("```json", "")
            text = text.replace("```", "")

            data = json.loads(text)

        except Exception as e:

            st.error(e)
            st.stop()

    # -----------------------
    # METRICS
    # -----------------------

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Trust Score",
        f"{data['trust_score']}/100"
    )

    c2.metric(
        "Risk",
        data["risk"]
    )

    c3.metric(
        "Recommendation",
        data["recommendation"]
    )

    st.divider()

    st.subheader("Summary")
    st.write(data["summary"])

    st.subheader("Analysis")
    st.write(data["analysis"])

    st.success("Analysis Complete")