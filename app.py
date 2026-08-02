
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

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

# -------------------------
# GEMINI
# -------------------------
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL = "gemini-3.5-flash"

# -----------------------
# SEARCH BOX
# -----------------------
query = st.text_input(
    "Search",
    placeholder="Company name, website, recruiter email or job..."
)

data = {}

analyze = st.button("🔍 Analyze", use_container_width=True)

# -----------------------
# PREMIUM DASHBOARD
# -----------------------

st.markdown("## 📊 Verification Dashboard")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="🛡 Trust Score",
        value=f"{data.get('trust_score', '--')}/100",
        delta="AI Score"
    )

with col2:
    st.metric(
        label="⚠ Risk Level",
        value=data.get("risk", "--"),
        delta="Assessment"
    )

with col3:
    domain_status = "Verified" if "." in query else "N/A"

    st.metric(
        label="🌐 Domain",
        value=domain_status,
        delta="Security"
    )

with col4:
    st.metric(
        label="🤖 Recommendation",
        value=data.get("recommendation", "--"),
        delta="AI Verdict"
    )

st.divider()

# -------------------------
# HEADER
# -------------------------
st.markdown("""
<div class="main-title">
🛡️ AI JobVerify
</div>

<div class="sub-title">
AI-powered Company • Domain • Job Verification Platform
</div>
""", unsafe_allow_html=True)

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

st.divider()

tab_company, tab_domain = st.tabs([
    "🏢 Company",
    "🌐 Domain"
])

with tab_company:
    if "data" in locals():
        st.subheader("Company Summary")
        st.write(data.get("summary", "No summary available."))
    else:
        st.info("Click 'Analyze' to view company information.")

with tab_domain:

    if "." in query:

        info = analyze_domain(query)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Domain", info["domain"])
            st.metric("Registrar", info["registrar"])
            st.metric("IP Address", info["ip"])

        with col2:
            st.metric("HTTPS", info["https"])
            st.metric("Status", info["status"])

        st.write("### Created")
        st.write(info["creation_date"])

        st.write("### Expires")
        st.write(info["expiration_date"])

        st.write("### Name Servers")
        st.write(info["ns"])

        st.write("### Mail Servers")
        st.write(info["mx"])

    else:
        st.info("Enter a domain like google.com")
