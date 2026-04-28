import streamlit as st

st.set_page_config(
    page_title="AI Placement Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ──────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Root theme */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Gradient background */
.stApp {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    min-height: 100vh;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.1);
}

/* Cards */
.glass-card {
    background: rgba(255,255,255,0.07);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 28px;
    margin: 12px 0;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, rgba(102,126,234,0.3), rgba(118,75,162,0.3));
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    color: white;
}

/* Hero section */
.hero-section {
    background: linear-gradient(135deg, rgba(102,126,234,0.2) 0%, rgba(118,75,162,0.2) 100%);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 24px;
    padding: 60px 40px;
    text-align: center;
    margin-bottom: 30px;
}

.hero-title {
    font-size: 3.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a78bfa, #60a5fa, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 16px;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 1.2rem;
    color: rgba(255,255,255,0.7);
    margin-bottom: 8px;
}

/* Result cards */
.result-placed {
    background: linear-gradient(135deg, rgba(52,211,153,0.25), rgba(16,185,129,0.15));
    border: 2px solid rgba(52,211,153,0.5);
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    animation: pulse-green 2s infinite;
}

.result-not-placed {
    background: linear-gradient(135deg, rgba(248,113,113,0.25), rgba(239,68,68,0.15));
    border: 2px solid rgba(248,113,113,0.5);
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    animation: pulse-red 2s infinite;
}

@keyframes pulse-green {
    0%, 100% { box-shadow: 0 0 20px rgba(52,211,153,0.3); }
    50% { box-shadow: 0 0 40px rgba(52,211,153,0.6); }
}

@keyframes pulse-red {
    0%, 100% { box-shadow: 0 0 20px rgba(248,113,113,0.3); }
    50% { box-shadow: 0 0 40px rgba(248,113,113,0.6); }
}

/* Nav pills in sidebar */
div[data-testid="stRadio"] > label {
    color: white !important;
    font-weight: 600;
    font-size: 1.05rem;
}

div[data-testid="stRadio"] div[role="radio"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 8px 12px;
    margin: 4px 0;
    border: 1px solid rgba(255,255,255,0.08);
    transition: all 0.2s;
}

div[data-testid="stRadio"] div[role="radio"]:hover {
    background: rgba(167,139,250,0.2);
    border-color: rgba(167,139,250,0.4);
}

/* Streamlit override: text colors */
h1, h2, h3, h4, h5, p, li {
    color: white !important;
}

.stMarkdown p { color: rgba(255,255,255,0.85) !important; }

/* Slider, inputs */
.stSlider > div > div > div > div { background: #a78bfa !important; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 28px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    transition: all 0.3s !important;
    box-shadow: 0 4px 15px rgba(102,126,234,0.4) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102,126,234,0.6) !important;
}

/* Tab styling */
.stTabs [data-baseweb="tab"] {
    color: rgba(255,255,255,0.6) !important;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    color: #a78bfa !important;
    border-bottom-color: #a78bfa !important;
}

/* DataFrames */
.dataframe { color: white !important; }

/* Progress bar */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, #667eea, #a78bfa) !important;
}

/* Badge styles */
.badge-ready {
    display: inline-block;
    background: linear-gradient(135deg, #34d399, #059669);
    color: white;
    padding: 6px 18px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.9rem;
}
.badge-improve {
    display: inline-block;
    background: linear-gradient(135deg, #f59e0b, #d97706);
    color: white;
    padding: 6px 18px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.9rem;
}
.badge-risk {
    display: inline-block;
    background: linear-gradient(135deg, #f87171, #dc2626);
    color: white;
    padding: 6px 18px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 0.9rem;
}

/* Divider */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(167,139,250,0.5), transparent);
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar Navigation ───────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 20px 0 10px 0;'>
        <div style='font-size:2.5rem;'>🎓</div>
        <div style='font-size:1.2rem; font-weight:700; color:white;'>PlacementAI</div>
        <div style='font-size:0.75rem; color:rgba(255,255,255,0.5); margin-top:4px;'>Powered by Random Forest</div>
    </div>
    <div class='custom-divider'></div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🏠 Home", "🎯 Predict Placement", "📊 Analytics", "📈 Model Performance", "ℹ️ About"],
        label_visibility="collapsed"
    )

    st.markdown("<div class='custom-divider'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:rgba(255,255,255,0.4); font-size:0.75rem; text-align:center; padding:10px;'>
        Dataset: 150,000 students<br>
        Model: Random Forest Classifier<br>
        Accuracy: ~85%
    </div>
    """, unsafe_allow_html=True)

# ── Route to pages ───────────────────────────────────────────────────────────
if page == "🏠 Home":
    from pages.Home import show
    show()
elif page == "🎯 Predict Placement":
    from pages.Prediction import show
    show()
elif page == "📊 Analytics":
    from pages.Analytics import show
    show()
elif page == "📈 Model Performance":
    from pages.Performance import show
    show()
elif page == "ℹ️ About":
    from pages.About import show
    show()
