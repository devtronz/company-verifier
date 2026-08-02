
import json
import streamlit as st
from google import genai
from domain import analyze_domain

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(
    page_title="🛡️ AI JobVerify",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# CUSTOM CSS
# -------------------------
st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 1rem;
}

.title {
    font-size: 40px;
    font-weight: 700;
    color: #00E5FF;
}

.subtitle {
    color: #B0B0B0;
    font-size: 18px;
}

div[data-testid="stMetric"] {
    background: #161B22;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #30363D;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# GEMINI
# -------------------------
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL = "gemini-3.5-flash"

# -------------------------
# SIDEBAR
# -------------------------
with st.sidebar:
    st.title("🛡️ AI JobVerify")
    st.caption("One Search. Verify Everything.")

    st.divider()

    st.subheader("Features")

    st.markdown("""
✅ Company Analysis

✅ Job Verification

✅ Domain Intelligence

✅ Official Social Media

✅ Trust Score

✅ Risk Analysis

✅ AI Recommendation
""")

    st.divider()

    st.success("Gemini Connected")

# -------------------------
# HEADER
# -------------------------
st.markdown(
    "<div class='title'>🛡️ AI JobVerify</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>AI-powered Company & Job Verification Platform</div>",
    unsafe_allow_html=True
)

st.write("")

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