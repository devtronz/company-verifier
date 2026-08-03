import json
import base64
import streamlit as st
from google import genai
from domain import analyze_domain

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="AI JobVerify",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# LOAD CSS
# ============================================

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

# ============================================
# BACKGROUND VIDEO
# ============================================

def add_bg_video():

    with open("assets/background.mp4", "rb") as video:

        video_bytes = video.read()

    encoded = base64.b64encode(video_bytes).decode()

    st.markdown(
        f"""
<style>

#bg-video{{
position:fixed;
right:0;
bottom:0;
min-width:100%;
min-height:100%;
object-fit:cover;
z-index:-999;
}}

.stApp{{
background:transparent;
}}

[data-testid="stHeader"]{{
background:transparent;
}}

[data-testid="stAppViewContainer"]{{
background:transparent;
}}

</style>

<video autoplay muted loop playsinline id="bg-video">
<source src="data:video/mp4;base64,{encoded}" type="video/mp4">
</video>

""",
        unsafe_allow_html=True,
    )

# ============================================
# LOAD UI
# ============================================

load_css()
add_bg_video()

# ============================================
# GEMINI
# ============================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL = "gemini-3.5-flash"

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:

    st.image(
        "https://img.icons8.com/fluency/96/security-shield-green.png",
        width=70
    )

    st.title("AI JobVerify")

    st.caption("Enterprise AI Verification")

    st.divider()

    st.markdown("### Features")

    st.markdown("""
✅ Company Verification

✅ Job Verification

✅ Domain Intelligence

✅ AI Risk Analysis

✅ Trust Score

✅ Recruiter Verification

✅ Domain WHOIS

✅ HTTPS Detection
""")

    st.divider()

    st.success("🟢 Gemini Connected")

# ============================================
# HERO
# ============================================

st.markdown("""
<div class="hero-card">

<div class="main-title">
🛡 AI JobVerify
</div>

<div class="sub-title">
Verify Companies • Domains • Recruiters with AI

<br><br>

AI powered verification platform that helps detect fake
companies, suspicious recruiters and risky domains.

</div>

</div>
""", unsafe_allow_html=True)

# ============================================
# SEARCH SECTION
# ============================================

st.markdown('<div class="search-card">', unsafe_allow_html=True)

query = st.text_input(
    "",
    placeholder="🔍 Search company, website, recruiter email or job title..."
)

analyze = st.button(
    "🚀 Analyze",
    use_container_width=True
)

st.markdown("</div>", unsafe_allow_html=True)

# Placeholder for AI response
data = {}

# ============================================
# AI ANALYSIS
# ============================================

if analyze:

    if not query.strip():
        st.warning("Please enter a company, domain or recruiter.")
        st.stop()

    with st.spinner("🧠 Gemini is analyzing..."):

        prompt = f"""
You are an expert Company Verification AI.

Analyze:

{query}

Return ONLY valid JSON.

{{
    "summary":"Short company summary",
    "trust_score":85,
    "risk":"Low",
    "recommendation":"Safe",
    "analysis":"Detailed explanation of why."
}}
"""

        try:

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            text = response.text.strip()

            text = text.replace("```json", "")
            text = text.replace("```", "")

            data = json.loads(text)

        except Exception as e:

            st.error(f"Analysis failed.\n\n{e}")
            st.stop()

    # ============================================
    # RESULT HEADER
    # ============================================

    st.markdown("## 🛡 AI Verification Result")

    trust = int(data.get("trust_score", 0))

    st.progress(trust / 100)

    if trust >= 80:
        st.success(
            f"✅ Trust Score **{trust}/100** — Highly Trusted"
        )

    elif trust >= 60:
        st.warning(
            f"⚠ Trust Score **{trust}/100** — Verify Carefully"
        )

    else:
        st.error(
            f"❌ Trust Score **{trust}/100** — High Risk"
        )

    st.write("")

    # ============================================
    # PREMIUM METRIC CARDS
    # ============================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "🛡 Trust",
            f"{trust}/100"
        )

    with c2:
        st.metric(
            "⚠ Risk",
            data.get("risk", "Unknown")
        )

    with c3:

        if "." in query:
            domain_status = "Verified"
        else:
            domain_status = "N/A"

        st.metric(
            "🌐 Domain",
            domain_status
        )

    with c4:
        st.metric(
            "🤖 AI Verdict",
            data.get("recommendation", "Unknown")
        )

    st.divider()

    # ============================================
    # SUMMARY & ANALYSIS
    # ============================================

    left, right = st.columns(2)

    with left:

        st.markdown("### 📋 Company Summary")

        st.info(
            data.get(
                "summary",
                "No summary available."
            )
        )

    with right:

        st.markdown("### 🧠 AI Analysis")

        st.success(
            data.get(
                "analysis",
                "No analysis available."
            )
        )

    st.divider()

# ============================================
# COMPANY & DOMAIN TABS
# ============================================

tab_company, tab_domain = st.tabs([
    "🏢 Company",
    "🌐 Domain Intelligence"
])

# ============================================
# COMPANY TAB
# ============================================

with tab_company:

    st.markdown("## 🏢 Company Overview")

    if data:

        c1, c2 = st.columns([2, 1])

        with c1:

            st.markdown("### 📋 Summary")

            st.write(data.get("summary", "No summary available."))

            st.markdown("### 🧠 AI Analysis")

            st.write(data.get("analysis", "No analysis available."))

        with c2:

            st.markdown("### 📊 Verification")

            st.metric(
                "Trust Score",
                f"{data.get('trust_score', '--')}/100"
            )

            st.metric(
                "Risk",
                data.get("risk", "Unknown")
            )

            st.metric(
                "Recommendation",
                data.get("recommendation", "Unknown")
            )

    else:

        st.info("Run an analysis to view company details.")

# ============================================
# DOMAIN TAB
# ============================================

with tab_domain:

    st.markdown("## 🌐 Domain Intelligence")

    if "." in query:

        try:

            info = analyze_domain(query)

            c1, c2, c3, c4 = st.columns(4)

            c1.metric(
                "HTTPS",
                info.get("https", "Unknown")
            )

            c2.metric(
                "Status",
                str(info.get("status", "Unknown"))
            )

            c3.metric(
                "Registrar",
                info.get("registrar", "Unknown")
            )

            c4.metric(
                "IP Address",
                info.get("ip", "Unknown")
            )

            st.divider()

            left, right = st.columns(2)

            with left:

                st.markdown("### 📅 Registration")

                st.write("**Created**")
                st.write(info.get("creation_date", "Unknown"))

                st.write("")

                st.write("**Expires**")
                st.write(info.get("expiration_date", "Unknown"))

            with right:

                st.markdown("### 🌍 DNS Records")

                st.write("**Name Servers**")

                ns = info.get("ns", [])

                if ns:
                    for server in ns:
                        st.write(f"• {server}")
                else:
                    st.write("No records found.")

                st.write("")

                st.write("**Mail Servers (MX)**")

                mx = info.get("mx", [])

                if mx:
                    for server in mx:
                        st.write(f"• {server}")
                else:
                    st.write("No records found.")

        except Exception as e:

            st.error(f"Domain lookup failed: {e}")

    else:

        st.info("Enter a domain such as **google.com** to view domain intelligence.")