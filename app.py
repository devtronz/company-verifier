import os
import re
import streamlit as st
import google.generativeai as genai
from datetime import datetime

# ========= PAGE CONFIG =========
st.set_page_config(
    page_title="AI JobVerify",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========= GEMINI =========
API_KEY = st.secrets.get("GEMINI_API_KEY", "")

if API_KEY:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None

# ========= CSS =========
st.markdown("""
<style>

.main {
    background-color:#0E1117;
}

.block-container{
    padding-top:1rem;
}

.big-title{
    font-size:42px;
    font-weight:800;
    color:#00E5FF;
}

.subtitle{
    color:#CCCCCC;
    font-size:18px;
}

.metric-box{
    background:#1B1F2A;
    padding:15px;
    border-radius:12px;
    border:1px solid #2F3545;
}

.section{
    background:#161B22;
    padding:18px;
    border-radius:12px;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# ========= SIDEBAR =========
with st.sidebar:

    st.title("🛡️ AI JobVerify")

    st.caption("One Search. Verify Everything.")

    st.divider()

    st.markdown("### Navigation")

    st.markdown("""
- Dashboard
- Company
- Leadership
- Domain
- Social
- Jobs
- News
- Reputation
- Trust Score
- Evidence
- PDF Report
""")

    st.divider()

    st.success("Gemini 2.5 Flash")

# ========= HEADER =========

st.markdown(
    "<div class='big-title'>🛡️ AI JobVerify</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>One Search. Complete Company & Job Verification</div>",
    unsafe_allow_html=True
)

st.write("")

# ========= SEARCH =========

query = st.text_input(
    "",
    placeholder="Search company, website, recruiter email, job URL or job description..."
)

search = st.button("🔍 Analyze", use_container_width=True)

# ========= DETECT INPUT =========

def detect_input(text):

    if not text:
        return "unknown"

    if text.startswith("http"):
        return "url"

    if "@" in text:
        return "email"

    if "job" in text.lower():
        return "job"

    return "company"

# ========= DASHBOARD =========

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric("Trust Score","--")

with col2:
    st.metric("Risk","--")

with col3:
    st.metric("Confidence","--")

with col4:
    st.metric("Status","Waiting")

st.divider()

tabs = st.tabs([
    "🏢 Company",
    "👤 Leadership",
    "🌐 Domain",
    "📱 Social",
    "💼 Jobs",
    "📰 News",
    "⚖️ Reputation",
    "📊 Trust",
    "📂 Evidence",
    "🤖 AI"
])

# ========= ANALYZE =========

if search:

    if not query.strip():

        st.warning("Please enter a company, website, job URL or email.")

        st.stop()

    input_type = detect_input(query)

    progress = st.progress(0)

    status = st.empty()

    steps = [
        "Detecting input...",
        "Collecting public information...",
        "Checking domain...",
        "Finding leadership...",
        "Searching news...",
        "Analyzing with Gemini...",
        "Building report..."
    ]

    for i, step in enumerate(steps):

        status.info(step)

        progress.progress((i + 1) * 100 // len(steps))

    if model:

        prompt = f"""
You are an AI company verification assistant.

Analyze:

{query}

Return:

1 Company Summary

2 Trust Score (0-100)

3 Risk Level

4 Recommendation

Be concise.
"""

        try:

            response = model.generate_content(prompt)

            ai_summary = response.text

        except Exception as e:

            ai_summary = f"Gemini Error: {e}"

    else:

        ai_summary = "Gemini API key not configured."

    status.success("Analysis Complete")

    with tabs[0]:

        st.subheader("Company Profile")

        st.info("Company profile module will populate here.")

    with tabs[1]:

        st.subheader("Leadership")

        st.info("Founder, CEO and ownership information.")

    with tabs[2]:

        st.subheader("Domain Intelligence")

        st.info("WHOIS, SSL, DNS and domain analysis.")

    with tabs[3]:

        st.subheader("Official Social Media")

        st.info("LinkedIn, X, GitHub and more.")

    with tabs[4]:

        st.subheader("Job Verification")

        st.info("Official careers page and recruiter verification.")

    with tabs[5]:

        st.subheader("Latest News")

        st.info("Latest public news.")

    with tabs[6]:

        st.subheader("Reputation")

        st.info("Legal matters and controversies.")

    with tabs[7]:

        st.subheader("Trust Score")

        st.metric("Overall","Pending")

    with tabs[8]:

        st.subheader("Evidence")

        st.info("Sources will appear here.")

    with tabs[9]:

        st.subheader("Gemini Analysis")

        st.write(ai_summary)