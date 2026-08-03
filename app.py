import base64
import json
import streamlit as st
from google import genai
from domain import analyze_domain

# ===================================
# PAGE CONFIG
# ===================================

st.set_page_config(
    page_title="🛡 AI JobVerify",
    page_icon="🛡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===================================
# LOAD CSS
# ===================================

def load_css():
    with open("assets/style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

def add_bg_video():
    with open("assets/background.mp4", "rb") as video:
        video_bytes = video.read()

    video_base64 = base64.b64encode(video_bytes).decode()

    st.markdown(
        f"""
        <style>
        #bg-video {{
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%;
            min-height: 100%;
            object-fit: cover;
            z-index: -100;
            opacity: 0.18;
        }}

        .stApp {{
            background: transparent;
        }}

        .main .block-container {{
            background: rgba(8, 14, 30, 0.72);
            backdrop-filter: blur(12px);
            border-radius: 20px;
            padding: 2rem;
            margin-top: 1rem;
        }}
        </style>

        <video autoplay muted loop playsinline id="bg-video">
            <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
        </video>
        """,
        unsafe_allow_html=True,
    )

load_css()
add_bg_video()
# ===================================
# GEMINI
# ===================================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)

MODEL = "gemini-3.5-flash"

# ===================================
# SIDEBAR
# ===================================

with st.sidebar:

    st.title("🛡 AI JobVerify")

    st.caption("One Search. Verify Everything.")

    st.divider()

    st.markdown("### Features")

    st.markdown("""
✅ Company Verification

✅ Domain Intelligence

✅ AI Analysis

✅ Trust Score

✅ Risk Detection

✅ Recruiter Verification
""")

# ===================================
# HEADER
# ===================================

st.markdown("""
<div class="main-title">
🛡 AI JobVerify
</div>

<div class="sub-title">
Verify Companies • Domains • Recruiters with AI
</div>
""", unsafe_allow_html=True)

# ===================================
# SEARCH
# ===================================

query = st.text_input(
    "",
    placeholder="Search company, website, recruiter email or job..."
)

analyze = st.button(
    "🚀 Analyze",
    use_container_width=True
)

data = {}

# ===================================
# ANALYSIS
# ===================================

if analyze:

    if not query.strip():
        st.warning("Please enter a search query.")
        st.stop()

    with st.spinner("🔎 Verifying..."):

        prompt = f"""
You are an AI Company Verification Assistant.

Analyze this query:

{query}

Return ONLY valid JSON.

{{
    "summary":"Short company summary",
    "trust_score":85,
    "risk":"Low",
    "recommendation":"Safe",
    "analysis":"Detailed explanation."
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
            st.error(f"Analysis failed: {e}")
            st.stop()

    # ===================================
    # RESULT HEADER
    # ===================================

    st.markdown("## 🛡 AI Verification Result")

    trust = int(data.get("trust_score", 0))

    st.progress(trust / 100)

    if trust >= 80:
        st.success(f"Trust Score: **{trust}/100** • Highly Trusted")
    elif trust >= 60:
        st.warning(f"Trust Score: **{trust}/100** • Needs Review")
    else:
        st.error(f"Trust Score: **{trust}/100** • High Risk")

    st.write("")

    # ===================================
    # METRICS
    # ===================================

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "🛡 Trust Score",
            f"{trust}/100"
        )

    with c2:
        st.metric(
            "⚠ Risk",
            data.get("risk", "Unknown")
        )

    with c3:
        st.metric(
            "🤖 Recommendation",
            data.get("recommendation", "Unknown")
        )

    st.divider()

    # ===================================
    # SUMMARY & ANALYSIS
    # ===================================

    left, right = st.columns(2)

    with left:

        st.subheader("📋 Summary")

        st.info(
            data.get(
                "summary",
                "No summary available."
            )
        )

    with right:

        st.subheader("🤖 AI Analysis")

        st.success(
            data.get(
                "analysis",
                "No analysis available."
            )
        )

    st.divider()

# ===================================
# COMPANY & DOMAIN TABS
# ===================================

tab_company, tab_domain = st.tabs([
    "🏢 Company",
    "🌐 Domain Intelligence"
])

# ===================================
# COMPANY TAB
# ===================================
st.subheader("🏢 Company Overview")

c1, c2 = st.columns(2)

with c1:
    st.info(data.get("summary", "No summary available."))

with c2:
    st.success(
        f"""
**Recommendation:** {data.get("recommendation","Unknown")}

**Risk:** {data.get("risk","Unknown")}
"""
    )


# ===================================
# DOMAIN TAB
# ===================================

with tab_domain:

    if "." in query:

        info = analyze_domain(query)

        st.subheader("🌐 Domain Intelligence")

        c1, c2 = st.columns(2)

        with c1:

            st.metric(
                "🌍 Domain",
                info.get("domain","Unknown")
            )

            st.metric(
                "🏢 Registrar",
                info.get("registrar","Unknown")
            )

            st.metric(
                "🌐 IP Address",
                info.get("ip","Unknown")
            )

        with c2:

            st.metric(
                "🔒 HTTPS",
                info.get("https","Unknown")
            )

            st.metric(
                "📡 Status",
                str(info.get("status","Unknown"))
            )

        st.divider()

        left, right = st.columns(2)

        with left:

            st.markdown("### 📅 Dates")

            st.write("**Created**")
            st.write(info.get("creation_date","Unknown"))

            st.write("")

            st.write("**Expires**")
            st.write(info.get("expiration_date","Unknown"))

        with right:

            st.markdown("### 🌐 DNS")

            st.write("**Name Servers**")

            if info.get("ns"):
                for server in info["ns"]:
                    st.write("•", server)
            else:
                st.write("No records found")

            st.write("")

            st.write("**Mail Servers**")

            if info.get("mx"):
                for server in info["mx"]:
                    st.write("•", server)
            else:
                st.write("No records found")

    else:

        st.info(
            "Enter a domain name (example: google.com) to view Domain Intelligence."
        )
