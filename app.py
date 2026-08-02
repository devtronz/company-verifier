
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

/* Background */
.stApp{
    background: linear-gradient(135deg,#0b1220,#111827,#0f172a);
}

/* Main container */
.block-container{
    padding-top:2rem;
    max-width:1200px;
}

/* Title */
.main-title{
    font-size:3rem;
    font-weight:800;
    color:white;
    margin-bottom:0;
}

.sub-title{
    color:#9CA3AF;
    font-size:1.1rem;
    margin-bottom:2rem;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#0B1120;
    border-right:1px solid #1F2937;
}

/* Search box */
.stTextInput input{
    border-radius:14px;
    border:1px solid #334155;
    background:#111827;
    color:white;
    height:55px;
    font-size:18px;
}

/* Button */
.stButton>button{
    width:100%;
    height:55px;
    border:none;
    border-radius:14px;
    background:linear-gradient(90deg,#3B82F6,#06B6D4);
    color:white;
    font-size:18px;
    font-weight:700;
}

.stButton>button:hover{
    transform:translateY(-2px);
    transition:.25s;
}

/* Cards */
div[data-testid="stMetric"]{
    background:#111827;
    border:1px solid #1E293B;
    border-radius:16px;
    padding:18px;
    box-shadow:0 8px 20px rgba(0,0,0,.35);
}

/* Tabs */
button[data-baseweb="tab"]{
    font-size:16px;
    font-weight:600;
}

/* Info boxes */
.stAlert{
    border-radius:14px;
}

hr{
    border:1px solid #1F2937;
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
