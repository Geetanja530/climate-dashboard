import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import streamlit.components.v1 as components
# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Climate Risk, ESG & Carbon Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)
# — Google Analytics —        ← ADD THIS BLOCK after set_page_config
def inject_ga():
    components.html("""
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-EJ5BDN2SG8"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', 'G-EJ5BDN2SG8');
        </script>
    """, height=0)

inject_ga()
# ── Theme ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
.stApp { background: linear-gradient(135deg, #0a1f0a 0%, #0d2b1a 50%, #0a1f2e 100%); color: #e0f0e0; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #0d2b1a 0%, #0a1f0a 100%); border-right: 1px solid #1a4a2a; }
[data-testid="stMetric"] { background: linear-gradient(135deg, #0d3a1a, #0a2a2a); border: 1px solid #2a6a3a; border-radius: 12px; padding: 16px; box-shadow: 0 4px 20px rgba(0,200,80,0.1); }
[data-testid="stMetricValue"] { color: #4dff91 !important; font-size: 2rem !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #90c0a0 !important; }
h1, h2, h3 { color: #4dff91 !important; }
h1 { font-size: 2.2rem !important; font-weight: 700 !important; }
.stTabs [data-baseweb="tab-list"] { background: #0d2b1a; border-radius: 10px; padding: 4px; }
.stTabs [data-baseweb="tab"] { color: #90c0a0; border-radius: 8px; }
.stTabs [aria-selected="true"] { background: #1a5a2a !important; color: #4dff91 !important; }
.stButton > button { background: linear-gradient(135deg, #1a5a2a, #0d3a4a); color: #4dff91; border: 1px solid #2a8a4a; border-radius: 8px; font-weight: 600; transition: all 0.2s; }
.stButton > button:hover { background: linear-gradient(135deg, #2a7a3a, #1a5a6a); border-color: #4dff91; transform: translateY(-1px); }
.stInfo { background: #0d3a2a; border-left: 4px solid #4dff91; color: #e0f0e0; }
hr { border-color: #1a4a2a; }
.stSelectbox > div > div { background: #0d2b1a; border-color: #2a6a3a; color: #e0f0e0; }
.stProgress > div > div { background: linear-gradient(90deg, #1a5a2a, #4dff91); }
.stTextInput > div > div { background: #0d2b1a; border-color: #2a6a3a; color: #e0f0e0; }
.stSuccess { background: #0d3a1a; border-left: 4px solid #4dff91; }

.source-badge {
    display: inline-block; background: #0d3a1a; border: 1px solid #2a6a3a;
    border-radius: 6px; padding: 3px 10px; font-size: 0.75rem; color: #4dff91; margin: 2px 4px;
}
</style>
""", unsafe_allow_html=True)

PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(10,31,10,0)",
    plot_bgcolor="rgba(13,43,26,0.6)",
    font=dict(color="#c0e0c0", family="Space Grotesk"),
    title_font=dict(color="#4dff91", size=16),
    xaxis=dict(gridcolor="#1a4a2a", linecolor="#2a6a3a"),
    yaxis=dict(gridcolor="#1a4a2a", linecolor="#2a6a3a"),
    colorway=["#4dff91", "#00c8ff", "#ffcc00", "#ff6b6b", "#b266ff"],
)
GREEN_SEQ = ["#0d3a1a", "#1a6a2a", "#2a9a4a", "#4dff91"]

# ══════════════════════════════════════════════════════════════════════════════
# GOOGLE ANALYTICS 4 — FREE VISITOR TRACKING
# ─────────────────────────────────────────────────────────────────────────────
# HOW TO SET UP (5 minutes, completely free):
#   1. Go to https://analytics.google.com — sign in with Google
#   2. Click "Start measuring" → name your account → create a Property
#   3. Choose "Web" → enter your Streamlit app URL → click Create Stream
#   4. Copy the Measurement ID (looks like  G-EJ5BDN2SG8)
#   5. Replace "G-EJ5BDN2SG8" below with your actual ID & push to GitHub
#   6. Data appears in GA within 24 hours — see visitors, countries, devices!
# ══════════════════════════════════════════════════════════════════════════════

GA_MEASUREMENT_ID = "G-EJ5BDN2SG8"  # ← PASTE YOUR REAL GA4 ID HERE

st.markdown(f"""
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{GA_MEASUREMENT_ID}', {{
    page_title: 'Climate Risk ESG Dashboard',
    page_location: window.location.href,
  }});
  document.addEventListener('click', function(e) {{
    var tab = e.target.closest('[data-baseweb="tab"]');
    if (tab) {{
