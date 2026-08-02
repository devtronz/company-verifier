
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
# HEADER
# -------------------------
st.markdown("""
<div class="main-title">
🛡 AI JobVerify
</div>

<div class="sub-title">
Verify Companies • Domains • Recruiters with AI
</div>
""", unsafe_allow_html=True)

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

    # -----------------------
# PREMIUM RESULT
# -----------------------

st.markdown("## 🛡 AI Verification Result")

st.progress(data["trust_score"] / 100)

st.success(
    f"Trust Score: **{data['trust_score']}/100** • {data['recommendation']}"
)

st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🛡 Trust Score", f"{data['trust_score']}/100")

with col2:
    st.metric("⚠ Risk", data["risk"])

with col3:
    st.metric(
        "🌐 Domain",
        "Verified" if "." in query else "N/A"
    )

st.divider()