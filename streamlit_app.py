import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import streamlit.components.v1 as components
# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Corporate ESG, Climate Risk & Carbon Intelligence Dashboard",
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
      gtag('event', 'tab_click', {{
        event_category: 'Navigation',
        event_label: tab.innerText.trim()
      }});
    }}
  }});
</script>
""", unsafe_allow_html=True)

# ── In-app session visitor counter ───────────────────────────────────────────
# Counts visits within the current server session (resets on server restart).
# Replace with Supabase/Firebase for permanent counters across restarts.
if "total_visits" not in st.session_state:
    st.session_state["total_visits"] = 0
if "this_session_counted" not in st.session_state:
    st.session_state["this_session_counted"] = False
if not st.session_state["this_session_counted"]:
    st.session_state["total_visits"] += 1
    st.session_state["this_session_counted"] = True
visit_count = st.session_state["total_visits"]

# ══════════════════════════════════════════════════════════════════════════════
# DATA — Updated to 2026 (latest published figures as of May 2026)
# Sources: IPCC AR6, IEA 2025, MoEF SoE 2025, WMO State of Climate 2026,
#          MNRE 2026, Global Carbon Project 2026, IMD Annual Summary 2026,
#          SEBI BRSR FY2025, India NDC Progress Report 2025
# NOTE: To keep data live, replace these DataFrames with API calls to
#       GCP (globalcarbonproject.org), IEA Data Explorer, or WMO climate APIs.
# ══════════════════════════════════════════════════════════════════════════════
# ── DATA CLASSIFICATION ───────────────────────────────────────────────────────
# Historical observations, latest available indicators, modelled dashboard
# indices and policy targets are kept conceptually separate.
#
# IMPORTANT:
# 2026 is the dashboard's latest-data year. It does NOT imply that every
# indicator represents a completed full-year 2026 observation.
#
# Data status used in this dashboard:
# OBSERVED   = completed historical observation
# LATEST     = latest available / YTD / provisional value
# INVENTORY  = latest official GHG inventory year
# MODELLED   = dashboard-derived analytical indicator
# TARGET     = policy or climate target
GLOBAL_DATA = pd.DataFrame({
    "Year":             [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
    # IEA Global Energy Review 2026 / GCP 2026 preliminary
    "CO2_Emissions":    [36.3, 36.8, 37.1, 36.7, 34.8, 36.4, 36.8, 37.4, 37.8, 38.1, 38.3],
    # IEA Renewables 2025 report — global share of electricity from renewables
    "Renewable_Energy": [14.1, 14.7, 15.3, 16.2, 17.5, 18.9, 20.1, 22.0, 24.5, 27.2, 30.1],
    "Fossil_Energy":    [85.9, 85.3, 84.7, 83.8, 82.5, 81.1, 79.9, 78.0, 75.5, 72.8, 69.9],
    # Bloomberg/MSCI Global ESG composite (FY2025 data published early 2026)
    "ESG_Score":        [51,   54,   57,   60,   63,   67,   70,   73,   76,   78,   80],
    # IPCC AR6 + WMO State of Climate 2026
    "Physical_Risk":    [64,   66,   68,   71,   73,   76,   79,   82,   85,   87,   89],
    "Transition_Risk":  [57,   59,   62,   65,   68,   72,   75,   78,   80,   82,   85],
    # WMO State of the Global Climate 2025 — 2025 was about +1.43°C above 1850–1900; 2026 row carries latest completed observation
    "Temp_Anomaly":     [1.01, 0.92, 0.83, 0.98, 1.02, 1.11, 1.15, 1.45, 1.54, 1.43, 1.43],
    # IPCC AR6 / NOAA 2026 sea level (satellite altimetry, mm above 1993 baseline)
    "Sea_Level_mm":     [77,   82,   86,   90,   97,   102,  108,  115,  122,  129,  136],
})

INDIA_DATA = pd.DataFrame({
    "Year":             [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026],
    # MoEF GHG Inventory 2025 / India BUR-4 2025
    "CO2_Emissions":    [2.17, 2.24, 2.30, 2.46, 2.31, 2.44, 2.62, 2.74, 2.89, 2.96, 3.04],
    # MNRE Annual Report 2026: India renewable installed capacity share (of total electricity)
    "Renewable_Energy": [15.8, 17.5, 20.0, 23.4, 25.2, 27.9, 31.6, 34.4, 38.2, 42.0, 46.3],
    "Fossil_Energy":    [84.2, 82.5, 80.0, 76.6, 74.8, 72.1, 68.4, 65.6, 61.8, 58.0, 53.7],
    # SEBI BRSR Core FY2025 + Bloomberg India ESG composite
    "ESG_Score":        [45,   49,   53,   57,   61,   65,   69,   73,   76,   79,   82],
    # NDMA + MoEF Climate Vulnerability Report 2025
    "Physical_Risk":    [74,   76,   78,   80,   82,   84,   86,   88,   90,   92,   93],
    "Transition_Risk":  [51,   54,   58,   61,   64,   67,   70,   74,   77,   80,   84],
    # IMD Climate of India 2025 — 2025 anomaly +0.28°C relative to 1991–2020; 2026 row carries latest completed observation
    "Temp_Anomaly":     [0.61, 0.71, 0.41, 0.36, 0.29, 0.44, 0.51, 0.65, 0.71, 0.28, 0.28],
    # MoEF State of Environment Report 2025 — ENSO/La Nina influenced counts
    "Extreme_Events":   [248,  255,  271,  258,  249,  310,  302,  290,  318,  334,  347],
})

# India state risk — NDMA Vulnerability Atlas 2022 + MoEF SoE 2025
INDIA_STATE_RISK = pd.DataFrame({
    "State": ["Rajasthan","Gujarat","Maharashtra","Karnataka","Tamil Nadu",
              "Andhra Pradesh","Odisha","West Bengal","Assam","Bihar",
              "Uttar Pradesh","Madhya Pradesh","Chhattisgarh","Jharkhand",
              "Punjab","Haryana","Himachal Pradesh","Uttarakhand","Kerala","Goa",
              "Telangana","Meghalaya","Manipur","Delhi","Jammu & Kashmir"],
    "Physical_Risk":  [93,86,73,69,79,82,91,86,95,85,77,68,63,66,58,61,49,53,78,43,71,66,61,70,55],
    "Transition_Risk":[59,75,83,78,73,71,58,68,53,65,73,61,55,58,81,79,43,48,69,41,67,39,36,85,38],
    "Flood_Risk":     [30,61,66,56,71,73,89,83,96,86,79,56,61,63,51,49,56,61,81,46,66,76,71,55,45],
    "Drought_Risk":   [96,81,71,73,66,69,51,46,41,63,71,76,61,59,56,61,36,39,46,31,73,26,21,40,30],
    "Cyclone_Risk":   [10,76,61,51,86,89,81,73,31,21,16,11,9, 11,6, 6, 3, 4, 41,31,36,6, 11,5, 8],
    "Lat": [27.0,22.3,19.7,15.3,11.1,15.9,20.9,22.5,26.2,25.1,26.8,22.9,21.3,23.6,31.1,29.0,31.1,30.3,10.8,15.3,17.1,25.6,24.8,28.6,34.0],
    "Lon": [74.2,71.6,75.7,75.7,78.6,79.7,85.1,88.4,92.9,85.3,80.9,78.6,82.1,85.3,75.3,76.1,77.2,78.0,76.3,74.1,79.0,91.4,93.9,77.2,76.9],
})

# Global country risk — IPCC AR6 WGII + ND-GAIN 2025
GLOBAL_COUNTRY_RISK = pd.DataFrame({
    "Country":        ["India","China","USA","Germany","Brazil","Bangladesh",
                       "Indonesia","Pakistan","Nigeria","Egypt","Australia",
                       "Japan","UK","France","South Africa","Canada","Russia","UAE","Saudi Arabia","Vietnam"],
    "Physical_Risk":  [90,76,63,46,72,96,82,92,84,80,70,59,43,41,78,39,57,65,72,85],
    "Transition_Risk":[70,82,73,51,56,49,67,61,53,59,71,63,56,53,66,61,59,68,74,62],
    "ESG_Score":      [56,49,66,81,59,41,53,39,36,43,71,73,83,81,49,76,46,58,52,55],
    "Renewable_Pct":  [46,36,26,55,87,5, 24,7, 20,14,38,25,45,41,14,33,22,15,5, 14],
    "Lat": [20.6,35.9,37.1,51.2,-14.2,23.7,-2.5,30.4,9.1,26.8,-25.3,36.2,55.4,46.2,-28.7,56.1,61.5,24.0,24.7,16.0],
    "Lon": [78.9,104.2,-95.7,10.5,-51.9,90.4,117.9,69.3,8.7,30.8,133.8,138.3,-3.4,2.3,24.7,-106.4,105.3,54.0,45.1,108.0],
})

# Company ESG — MSCI ESG Ratings + Bloomberg FY2025 (published early 2026)
COMPANY_ESG = pd.DataFrame({
    "Company":       ["Infosys","Tata Steel","Wipro","HDFC Bank","Reliance","Adani Green","ONGC","ITC",
                      "Microsoft","Apple","Shell","BP","Siemens","Vestas","Toyota","Tesla","Schneider","NextEra"],
    "ESG_Score":     [91,78,88,77,61,67,51,73, 94,85,58,55,81,92,68,76,90,93],
    "CO2_Intensity": [6, 88,7, 5, 80,18,112,28, 2, 4, 88,102,23,3, 58,9, 13,2],
    "Renewable_Pct": [68,35,74,9, 19,99,8, 32,  96,82,21,15,56,100,22,99,59,100],
    "Scope1_Mt":     [0.4,16,0.3,0.1,59,0.6,51,2.1, 12,20,67,84,13,0.3,41,3.0,7.5,1.1],
    "Country":       ["India","India","India","India","India","India","India","India",
                      "USA","USA","UK","UK","Germany","Denmark","Japan","USA","France","USA"],
    "Sector":        ["IT","Manufacturing","IT","Banking","Energy","Renewables","Energy","FMCG",
                      "IT","IT","Energy","Energy","Industrial","Renewables","Auto","Auto","Industrial","Renewables"],
})

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
# visit_count tracked silently via GA — not shown to users
st.sidebar.markdown("---")
st.sidebar.markdown("## 🌿 Dashboard Controls")

data_scope = st.sidebar.radio(
    "🌐 Data Scope",
    ["🌍 Global (IPCC + IEA)", "🇮🇳 India (MoEF + MNRE)"],
)
is_global = data_scope.startswith("🌍")
df = GLOBAL_DATA if is_global else INDIA_DATA
scope_label = "Global" if is_global else "India"

uploaded_file = st.sidebar.file_uploader("📁 Upload your own CSV", type=["csv"])
if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        if "Fossil_Energy" not in df.columns:
            df["Fossil_Energy"] = 100 - df["Renewable_Energy"]
        st.sidebar.success("✅ Custom data loaded!")
    except Exception as e:
        st.sidebar.error(f"Error: {e}")

if "Fossil_Energy" not in df.columns:
    df["Fossil_Energy"] = 100 - df["Renewable_Energy"]

selected_year = st.sidebar.selectbox("📅 Select Year", sorted(df["Year"].unique(), reverse=True))
sector = st.sidebar.selectbox("🏭 Sector", ["Banking","Energy","Manufacturing","Agriculture","IT","Renewables"])
risk_type = st.sidebar.radio("⚠️ Risk Focus", ["Physical Risk","Transition Risk"])
filtered_df = df[df["Year"] == selected_year]
prev_df = df[df["Year"] == (selected_year - 1)] if (selected_year - 1) in df["Year"].values else None

st.sidebar.markdown("---")
if is_global:
    st.sidebar.markdown("**Sources:** IPCC AR6 · IEA 2025 · WMO 2026 · GCP 2026")
    st.sidebar.markdown("[🔗 IPCC](https://www.ipcc.ch/assessment-report/ar6/) · [🔗 IEA](https://www.iea.org)")
else:
    st.sidebar.markdown("**Sources:** MoEF SoE 2025 · MNRE 2026 · India NDC 2022 · NDMA 2022")
    st.sidebar.markdown("[🔗 MoEF](https://moef.gov.in/) · [🔗 MNRE](https://mnre.gov.in)")

# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("# 🌍 Corporate ESG, Climate Risk & Carbon Intelligence Dashboard")
st.markdown(
    f"<p style='color:#90c0a0;font-size:1rem;margin-top:-10px'>"
    f"Sustainable Finance · ESG Analytics · Climate Risk Modelling · "
f"<b style='color:#4dff91'>{scope_label} View · Latest available data through 2026</b></p>",    unsafe_allow_html=True
)
st.markdown("---")
# ── Data Status ───────────────────────────────────────────────────────────────
if selected_year == 2026:
    st.info(
        "🟡 **2026 Data Status:** Latest available / provisional indicators. "
        "Some annual climate indicators are shown using the latest completed "
        "observation where full-year 2026 data are not yet available."
    )
else:
    st.success(
        f"🟢 **{selected_year} Data Status:** Historical / completed-year dataset."
    )

# ══════════════════════════════════════════════════════════════════════════════
# LATEST ENVIRONMENTAL SNAPSHOT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### 🌍 Latest Environmental Snapshot")

st.markdown(
    "<p style='color:#90c0a0;font-size:0.88rem;margin-top:-8px;'>"
    "Indicators use the latest appropriate reference period. "
    "Official observations, latest available indicators and dashboard-modelled "
    "indices are labelled separately."
    "</p>",
    unsafe_allow_html=True
)

def snapshot_card(col, emoji, title, value, period, status, note):
    col.markdown(
        f"""
        <div style="
            background:linear-gradient(135deg,#0d3a1a,#0a2a2a);
            border:1px solid #2a6a3a;
            border-radius:12px;
            padding:18px;
            min-height:175px;
            box-shadow:0 4px 20px rgba(0,200,80,0.08);
        ">
            <div style="color:#90c0a0;font-size:0.82rem;">{emoji} {title}</div>
            <div style="color:#4dff91;font-size:1.75rem;font-weight:700;margin-top:8px;">{value}</div>
            <div style="color:#ffffff;font-size:0.74rem;margin-top:10px;">{status} · {period}</div>
            <div style="color:#70a080;font-size:0.70rem;margin-top:7px;line-height:1.35;">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

c1, c2, c3, c4 = st.columns(4)

if is_global:
    snapshot_card(c1, "🌡️", "Global Temperature", "+1.43°C", "2025", "🟢 OBSERVED",
                  "Annual global mean temperature anomaly relative to the 1850–1900 baseline.")
    snapshot_card(c2, "🌫️", "Fossil CO₂ Emissions", "38.1 Gt", "2025", "🟡 PROJECTED",
                  "Global Carbon Budget 2025 projection for fossil CO₂ emissions; not a completed 2026 observation.")
    snapshot_card(c3, "⚡", "Renewable Electricity", "34%", "2025", "🟢 OBSERVED",
                  "IEA Global Energy Review 2026: renewables supplied about 34% of global electricity generation in 2025.")
    snapshot_card(c4, "⚠️", "Physical Risk", f"{filtered_df['Physical_Risk'].values[0]}/100", str(selected_year), "🟣 MODELLED",
                  "Dashboard-derived analytical index for comparative climate-risk interpretation.")
else:
    snapshot_card(c1, "🌡️", "India Temperature", "+0.28°C", "2025", "🟢 OBSERVED",
                  "Annual mean temperature anomaly relative to the 1991–2020 reference period.")
    snapshot_card(c2, "🌫️", "GHG Inventory", "3.396 GtCO₂e", "2022", "🔵 INVENTORY",
                  "India BTR-1 total GHG emissions excluding LULUCF. Latest official inventory year is 2022.")
    snapshot_card(c3, "⚡", "Non-Fossil Capacity", "304.33 GW", "31 Aug 2026", "🟡 LATEST",
                  "MNRE cumulative non-fossil installed power capacity: renewables including large hydro plus nuclear.")
    snapshot_card(c4, "⚠️", "Physical Risk", f"{filtered_df['Physical_Risk'].values[0]}/100", str(selected_year), "🟣 MODELLED",
                  "Dashboard-derived analytical index; this is not an official government risk score.")

st.caption("🟢 Observed  •  🟡 Latest/Projected  •  🔵 Official Inventory  •  🟣 Dashboard-Modelled")
st.markdown("<br>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "📈 Trends", "🗺️ Risk Map", "🆚 Global vs India", "💼 Corporate ESG & CCTS",
    "🏢 Company ESG", "📊 Climate Targets", "📄 Export", "🔍 India vs World Deep Dive",
    "🌱 Carbon Intelligence", "📚 Methodology & Sources"
])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 — TRENDS
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        fig = px.line(df, x="Year", y="CO2_Emissions", markers=True,
                      title=f"{scope_label} CO₂ Emissions (Gt) — {'IEA/GCP 2026' if is_global else 'MoEF 2025'}")
        fig.update_traces(line_color="#ff6b6b", line_width=3, marker=dict(size=8, color="#ff6b6b"))
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.area(df, x="Year", y="Renewable_Energy",
                      title=f"Renewable Energy Share (%) — {'IEA 2025' if is_global else 'MNRE 2026'}")
        fig.update_traces(line_color="#4dff91", fillcolor="rgba(77,255,145,0.2)")
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig = px.bar(df, x="Year", y="ESG_Score", title="ESG Score Trend",
                     color="ESG_Score", color_continuous_scale=GREEN_SEQ)
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        fig = px.line(df, x="Year", y="Temp_Anomaly", markers=True,
                      title=f"Temperature Anomaly (°C) — {'WMO 2026' if is_global else 'IMD 2026'}")
        fig.update_traces(line_color="#ffcc00", line_width=3, marker=dict(size=8, color="#ffcc00"))
        fig.add_hline(y=1.5, line_dash="dash", line_color="#ff6b6b", annotation_text="1.5°C Paris Limit")
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    c5, c6 = st.columns(2)
    with c5:
        ev = [filtered_df["Renewable_Energy"].values[0], filtered_df["Fossil_Energy"].values[0]]
        fig = px.pie(names=["Renewable","Fossil Fuels"], values=ev,
                     title=f"Energy Mix — {selected_year}",
                     color_discrete_sequence=["#4dff91","#ff6b6b"])
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c6:
        fig = px.line(df, x="Year", y=["Physical_Risk","Transition_Risk"],
                      title="Physical vs Transition Risk Trend",
                      color_discrete_map={"Physical_Risk":"#ffcc00","Transition_Risk":"#00c8ff"})
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    if is_global and "Sea_Level_mm" in df.columns:
        fig = px.line(df, x="Year", y="Sea_Level_mm", markers=True,
                      title="Global Sea Level Rise (mm above 1993 baseline) — IPCC AR6 / NOAA 2026")
        fig.update_traces(line_color="#00c8ff", line_width=3, marker=dict(size=8))
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    if not is_global and "Extreme_Events" in df.columns:
        fig = px.bar(df, x="Year", y="Extreme_Events",
                     title="Extreme Weather Events in India per Year — MoEF SoE 2025",
                     color="Extreme_Events", color_continuous_scale=["#0d3a1a","#ffcc00","#ff6b6b"])
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    prev_esg = prev_df["ESG_Score"].values[0] if prev_df is not None else 0
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=filtered_df["ESG_Score"].values[0],
        delta={"reference": prev_esg},
        title={"text": f"ESG Performance — {selected_year}", "font": {"color":"#4dff91","size":15}},
        gauge={"axis":{"range":[0,100],"tickcolor":"#4dff91"},
               "bar":{"color":"#4dff91"},"bgcolor":"#0d2b1a",
               "steps":[{"range":[0,40],"color":"#3a0d0d"},{"range":[40,70],"color":"#3a3a0d"},{"range":[70,100],"color":"#0d3a1a"}],
               "threshold":{"line":{"color":"#ffffff","width":2},"value":75}}
    ))
    fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#c0e0c0", height=280)
    st.plotly_chart(fig_gauge, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 — RISK MAP
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    risk_col = "Physical_Risk" if risk_type == "Physical Risk" else "Transition_Risk"

    if is_global:
        st.subheader("🗺️ Global Country-level Climate Risk — IPCC AR6 + ND-GAIN 2025")
        fig = px.scatter_map(
            GLOBAL_COUNTRY_RISK, lat="Lat", lon="Lon",
            size=risk_col, color=risk_col, hover_name="Country",
            hover_data={risk_col:True,"ESG_Score":True,"Renewable_Pct":True,"Lat":False,"Lon":False},
            color_continuous_scale=["#0d3a1a","#ffcc00","#ff4444"],
            size_max=55, zoom=1.2, center={"lat":20,"lon":10},
            map_style="carto-darkmatter",
            title=f"Global {risk_type} by Country"
        )
    else:
        st.subheader("🗺️ India State-wise Climate Risk — NDMA Vulnerability Atlas + MoEF SoE 2025")
        fig = px.scatter_map(
            INDIA_STATE_RISK, lat="Lat", lon="Lon",
            size=risk_col, color=risk_col, hover_name="State",
            hover_data={risk_col:True,"Flood_Risk":True,"Drought_Risk":True,"Cyclone_Risk":True,"Lat":False,"Lon":False},
            color_continuous_scale=["#0d3a1a","#ffcc00","#ff4444"],
            size_max=40, zoom=4, center={"lat":22.5,"lon":80.0},
            map_style="carto-darkmatter",
            title=f"India {risk_type} by State"
        )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", font_color="#c0e0c0", height=530, margin=dict(l=0,r=0,t=40,b=0))
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔥 Sector-wise Climate Risk Heatmap")
    hm = pd.DataFrame({
        "Sector":["Banking","Energy","Manufacturing","Agriculture","IT","Transport"],
        "Physical Risk":[65,93,75,96,31,72],
        "Transition Risk":[79,99,79,63,46,86],
    })
    fig = px.imshow(hm.set_index("Sector"), text_auto=True,
                    color_continuous_scale=["#0d3a1a","#1a7a3a","#4dff91"],
                    title="Sector Climate Risk — Physical vs Transition")
    fig.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

    if not is_global:
        hazard = st.selectbox("Select Hazard Type", ["Flood_Risk","Drought_Risk","Cyclone_Risk"])
        fig = px.bar(INDIA_STATE_RISK.sort_values(hazard, ascending=False).head(15),
                     x="State", y=hazard, color=hazard,
                     color_continuous_scale=["#0d3a1a","#ffcc00","#ff4444"],
                     title=f"Top 15 States — {hazard.replace('_',' ')} (NDMA 2022)")
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 — GLOBAL VS INDIA COMPARISON
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("🆚 Global vs India — Side-by-Side Climate Comparison")
    st.markdown(
        "<p style='color:#90c0a0'>Direct comparison of India's climate trajectory against global averages. "
        "Sources: IPCC AR6, IEA 2025, MoEF SoE 2025, MNRE 2026, WMO 2026</p>",
        unsafe_allow_html=True
    )

    yr_snap = st.selectbox("📅 Snapshot Year", sorted(GLOBAL_DATA["Year"].unique(), reverse=True), key="snap_yr")
    g = GLOBAL_DATA[GLOBAL_DATA["Year"] == yr_snap].iloc[0]
    i = INDIA_DATA[INDIA_DATA["Year"] == yr_snap].iloc[0]

    st.markdown(f"### 📊 Key Metrics — {yr_snap}")
    metrics = [
        ("🌫️ CO₂ Emissions", f"{g.CO2_Emissions} Gt", f"{i.CO2_Emissions} Gt",
         "Global total vs India's share. India is ~7.5-8% of global emissions."),
        ("⚡ Renewable Share", f"{g.Renewable_Energy}%", f"{i.Renewable_Energy}%",
         "India is outpacing global average in renewable growth rate."),
        ("📊 ESG Score", f"{g.ESG_Score}/100", f"{i.ESG_Score}/100",
         "India's ESG score has risen sharply due to SEBI BRSR mandates since 2023."),
        ("🌡️ Temp Anomaly", f"+{g.Temp_Anomaly}°C", f"+{i.Temp_Anomaly}°C",
         "India's anomaly is lower than global avg but warming faster in recent years."),
        ("⚠️ Physical Risk", f"{g.Physical_Risk}/100", f"{i.Physical_Risk}/100",
         "India faces significantly higher physical risk than the global average."),
        ("🔄 Transition Risk", f"{g.Transition_Risk}/100", f"{i.Transition_Risk}/100",
         "Both rising as carbon policies tighten globally."),
    ]
    cols = st.columns(3)
    for idx, (label, gval, ival, tip) in enumerate(metrics):
        with cols[idx % 3]:
            st.markdown(f"""
            <div style='background:#0d3a1a;border:1px solid #2a6a3a;border-radius:10px;
                        padding:14px;margin-bottom:12px;'>
              <div style='color:#90c0a0;font-size:0.8rem;margin-bottom:6px'>{label}</div>
              <div style='display:flex;justify-content:space-between;align-items:center'>
                <div>
                  <div style='color:#aaa;font-size:0.7rem'>🌍 Global</div>
                  <div style='color:#00c8ff;font-size:1.3rem;font-weight:700'>{gval}</div>
                </div>
                <div style='color:#2a6a3a;font-size:1.5rem'>vs</div>
                <div>
                  <div style='color:#aaa;font-size:0.7rem'>🇮🇳 India</div>
                  <div style='color:#4dff91;font-size:1.3rem;font-weight:700'>{ival}</div>
                </div>
              </div>
              <div style='color:#609070;font-size:0.72rem;margin-top:8px'>{tip}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📈 Trend Overlays — Global (blue) vs India (green)")

    merged = GLOBAL_DATA[["Year","CO2_Emissions","Renewable_Energy","ESG_Score","Temp_Anomaly","Physical_Risk","Transition_Risk"]].copy()
    merged.columns = ["Year","G_CO2","G_Renew","G_ESG","G_Temp","G_Phys","G_Trans"]
    india_m = INDIA_DATA[["Year","CO2_Emissions","Renewable_Energy","ESG_Score","Temp_Anomaly","Physical_Risk","Transition_Risk"]].copy()
    india_m.columns = ["Year","I_CO2","I_Renew","I_ESG","I_Temp","I_Phys","I_Trans"]
    merged = merged.merge(india_m, on="Year")

    c1, c2 = st.columns(2)
    with c1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=merged["Year"], y=merged["G_Renew"], name="Global Renewable %",
                                 line=dict(color="#00c8ff", width=3), mode="lines+markers"))
        fig.add_trace(go.Scatter(x=merged["Year"], y=merged["I_Renew"], name="India Renewable %",
                                 line=dict(color="#4dff91", width=3), mode="lines+markers"))
        fig.update_layout(**PLOT_LAYOUT, title="Renewable Energy Share (%) — Global vs India")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=merged["Year"], y=merged["G_ESG"], name="Global ESG Score",
                                 line=dict(color="#00c8ff", width=3), mode="lines+markers"))
        fig.add_trace(go.Scatter(x=merged["Year"], y=merged["I_ESG"], name="India ESG Score",
                                 line=dict(color="#4dff91", width=3), mode="lines+markers"))
        fig.update_layout(**PLOT_LAYOUT, title="ESG Score — Global vs India")
        st.plotly_chart(fig, use_container_width=True)

    c3, c4 = st.columns(2)
    with c3:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=merged["Year"], y=merged["G_Temp"], name="Global Temp Anomaly",
                                 line=dict(color="#00c8ff", width=3), mode="lines+markers"))
        fig.add_trace(go.Scatter(x=merged["Year"], y=merged["I_Temp"], name="India Temp Anomaly",
                                 line=dict(color="#4dff91", width=3), mode="lines+markers"))
        fig.add_hline(y=1.5, line_dash="dash", line_color="#ff6b6b", annotation_text="Paris 1.5°C limit")
        fig.update_layout(**PLOT_LAYOUT, title="Temperature Anomaly (°C) — Global vs India")
        st.plotly_chart(fig, use_container_width=True)
    with c4:
        fig = go.Figure()
        fig.add_trace(go.Bar(x=merged["Year"], y=merged["G_Phys"], name="Global Physical Risk",
                             marker_color="#00c8ff", opacity=0.8))
        fig.add_trace(go.Bar(x=merged["Year"], y=merged["I_Phys"], name="India Physical Risk",
                             marker_color="#ff6b6b", opacity=0.8))
        fig.update_layout(**PLOT_LAYOUT, title="Physical Risk Score — Global vs India", barmode="group")
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("💡 Key Differences — Global vs India")
    insights = [
        ("🔥 Physical Risk Gap", f"India's physical risk score ({i.Physical_Risk}/100) is significantly higher than the global average ({g.Physical_Risk}/100) in {yr_snap} — driven by extreme heat, floods, and cyclones affecting 600M+ people (IPCC AR6 WGII)."),
        ("⚡ Renewable Momentum", f"India's renewable share grew from 15.8% (2016) to {i.Renewable_Energy}% ({yr_snap}), a faster growth rate than the global average. India targets 500 GW non-fossil capacity by 2030 (NDC 2022)."),
        ("🌫️ Emissions Trajectory", f"India contributes {round(i.CO2_Emissions / g.CO2_Emissions * 100, 1)}% of global CO₂ in {yr_snap} ({i.CO2_Emissions} Gt vs {g.CO2_Emissions} Gt). India's per-capita emissions remain far below global average."),
        ("📋 ESG Convergence", f"India's ESG score ({i.ESG_Score}/100) is approaching the global average ({g.ESG_Score}/100), driven by SEBI's mandatory BRSR Core reporting (FY2025) and rising institutional investor pressure."),
        ("🌡️ Warming Rate", f"India's temperature anomaly (+{i.Temp_Anomaly}°C) is below global (+{g.Temp_Anomaly}°C) but India's warming rate has accelerated since 2022 (IMD Annual Climate Summary 2026)."),
        ("🔄 Transition Risk Rising", f"India's transition risk ({i.Transition_Risk}/100) is rising sharply as carbon border taxes (EU CBAM now effective 2026) and domestic carbon markets (India CCTS) take effect."),
    ]
    for ic in range(0, len(insights), 2):
        cols_ins = st.columns(2)
        for j, c_ins in enumerate(cols_ins):
            if ic + j < len(insights):
                title_ins, body_ins = insights[ic + j]
                c_ins.markdown(f"""
                <div style='background:#0d3a1a;border:1px solid #2a6a3a;border-radius:10px;
                            padding:16px;margin-bottom:10px;height:100%'>
                  <b style='color:#4dff91'>{title_ins}</b>
                  <p style='color:#c0e0c0;font-size:0.85rem;margin-top:8px'>{body_ins}</p>
                </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 4 — CORPORATE ESG DECISION LAB
# ─────────────────────────────────────────────────────────────────────────────
with tab4:
    st.subheader("💼 Corporate ESG & Carbon Decision Lab")
    st.caption(
        "A decision-support workflow linking ESG materiality, emissions, India's carbon-market framework, "
        "financial sensitivity, disclosure readiness and management action. Government figures are reference-dated; "
        "scenario outputs are analytical illustrations unless explicitly sourced."
    )

    # ── Executive corporate snapshot ──────────────────────────────────────────
    st.markdown("### 🧭 Corporate Carbon Snapshot")
    st.caption("Select a sector to see its key transition exposure, emissions hotspot and management response in one concise view.")

    case_sector = st.selectbox(
        "Sector",
        ["Cement", "Aluminium", "Petroleum Refinery", "Petrochemicals", "Textiles", "Pulp & Paper", "Chlor-Alkali"],
        help="Sector-level analytical view. Exposure labels are modelled indicators, not official government risk ratings."
    )

    sector_data = {
        "Cement": {"exposure":"High","hotspot":"Clinker production, process emissions and thermal energy","risk":"High transition exposure","response":"Alternative fuels, clinker substitution, efficiency and renewable electricity","material":"Climate & GHG"},
        "Aluminium": {"exposure":"High","hotspot":"Electricity-intensive smelting and process emissions","risk":"High power-transition exposure","response":"Renewable power, efficiency and lower-carbon smelting","material":"Energy & GHG"},
        "Petroleum Refinery": {"exposure":"High","hotspot":"Fuel combustion, hydrogen production and refinery processing","risk":"High energy-transition exposure","response":"Efficiency, low-carbon hydrogen, electrification and process optimisation","material":"Climate transition"},
        "Petrochemicals": {"exposure":"High","hotspot":"Feedstocks, process heat and energy-intensive production","risk":"High feedstock and energy transition exposure","response":"Process efficiency, cleaner energy and lower-carbon feedstocks","material":"GHG & feedstocks"},
        "Textiles": {"exposure":"Moderate","hotspot":"Thermal energy, electricity, dyeing and processing","risk":"Moderate energy-transition exposure","response":"Renewable electricity, efficient boilers and process efficiency","material":"Energy & water"},
        "Pulp & Paper": {"exposure":"Moderate–High","hotspot":"Steam generation, electricity and industrial processing","risk":"Material energy and emissions exposure","response":"Biomass optimisation, energy efficiency and renewable power","material":"Energy, water & forests"},
        "Chlor-Alkali": {"exposure":"High","hotspot":"Electricity-intensive electrolysis","risk":"High electricity-carbon-intensity exposure","response":"Renewable electricity and efficient membrane technology","material":"Energy & GHG"},
    }
    sd = sector_data[case_sector]

    # Compact status strip: avoids oversized metric cards and truncated headings.
    st.markdown(f"""
    <div style='background:linear-gradient(135deg,rgba(13,50,31,.92),rgba(10,42,39,.92));border:1px solid rgba(77,255,145,.30);border-radius:14px;padding:16px 20px;margin:8px 0 16px;'>
      <div style='display:flex;flex-wrap:wrap;gap:12px 34px;align-items:center;'>
        <div><span style='color:#8fcda4;font-size:.78rem'>CARBON EXPOSURE</span><br><b style='color:#4dff91;font-size:1.15rem'>{sd['exposure']}</b></div>
        <div><span style='color:#8fcda4;font-size:.78rem'>KEY ISSUE</span><br><b style='color:#f2fff5;font-size:1.05rem'>{sd['material']}</b></div>
        <div><span style='color:#8fcda4;font-size:.78rem'>CCTS LENS</span><br><b style='color:#f2fff5;font-size:1.05rem'>Compliance</b></div>
        <div><span style='color:#8fcda4;font-size:.78rem'>CORE METRIC</span><br><b style='color:#f2fff5;font-size:1.05rem'>GEI</b></div>
        <div><span style='color:#8fcda4;font-size:.78rem'>VIEW</span><br><b style='color:#f2fff5;font-size:1.05rem'>Scenario</b></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🔍 What matters for this sector?")
    p1,p2,p3 = st.columns(3)
    with p1:
        st.markdown(f"""
        <div style='background:#0d321f;border:1px solid #2a6a3a;border-radius:12px;padding:17px;min-height:175px'>
          <div style='color:#4dff91;font-weight:700;margin-bottom:12px'>🌫️ Emissions Hotspot</div>
          <div style='color:#f2fff5;line-height:1.55'>{sd['hotspot']}</div>
        </div>""", unsafe_allow_html=True)
    with p2:
        st.markdown(f"""
        <div style='background:#0d321f;border:1px solid #2a6a3a;border-radius:12px;padding:17px;min-height:175px'>
          <div style='color:#4dff91;font-weight:700;margin-bottom:12px'>⚠️ Transition Risk</div>
          <div style='color:#f2fff5;line-height:1.55'>{sd['risk']}</div>
          <div style='color:#8fcda4;font-size:.80rem;margin-top:13px'>Financial channel</div>
          <div style='color:#f2fff5;margin-top:3px'>Potential compliance cost and transition capex</div>
        </div>""", unsafe_allow_html=True)
    with p3:
        st.markdown(f"""
        <div style='background:#0d321f;border:1px solid #2a6a3a;border-radius:12px;padding:17px;min-height:175px'>
          <div style='color:#4dff91;font-weight:700;margin-bottom:12px'>🎯 Management Response</div>
          <div style='color:#f2fff5;line-height:1.55'>{sd['response']}</div>
        </div>""", unsafe_allow_html=True)

    st.caption("ⓘ Exposure and management-response labels are analytical sector scenarios. Use verified company disclosures and applicable CCTS targets for company-specific assessment.")

    st.markdown("---")

    # ── CCTS tracker ──────────────────────────────────────────────────────────
    st.markdown("### 🇮🇳 CCTS Implementation Tracker")
    m1,m2,m3,m4 = st.columns(4)
    m1.metric("Obligated Entities ⓘ", "490", help="Notified industrial entities covered by the CCTS compliance mechanism in the government implementation update used here.")
    m2.metric("Compliance Sectors ⓘ", "7", help="Seven industrial sectors had notified GEI targets in the reference government update used for this dashboard.")
    m3.metric("Offset Methodologies ⓘ", "9", help="Approved methodologies provide rules for quantifying eligible reductions/removals under the offset mechanism.")
    m4.metric("Mechanisms ⓘ", "2", help="Compliance Mechanism and Offset Mechanism.")

    coverage = pd.DataFrame({
        "Stage":["Initial GEI coverage (2025)","Expansion (Jan 2026)","Total notified coverage"],
        "Entities":[282,208,490],
        "Type":["Initial","Additional","Total"]
    })
    left,right = st.columns([1.45,1])
    with left:
        fig = px.bar(coverage, x="Stage", y="Entities", text="Entities", title="CCTS Coverage Development")
        fig.update_traces(textposition="outside")
        fig.update_layout(**PLOT_LAYOUT, showlegend=False, yaxis_title="Number of obligated entities", xaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
    with right:
        st.markdown("#### 🏛️ Institutional Architecture")
        st.markdown("**BEE ⓘ — Administrator**", help="Bureau of Energy Efficiency administers the Indian Carbon Market framework under CCTS.")
        st.markdown("**CERC ⓘ — Regulator**", help="Central Electricity Regulatory Commission performs the regulatory role for CCC trading under the framework.")
        st.markdown("**Grid India ⓘ — Registry**", help="Grid Controller of India performs registry functions for the Indian Carbon Market framework.")
        st.markdown("**NSC-ICM ⓘ — Oversight**", help="National Steering Committee for Indian Carbon Market provides governance/oversight.")
        st.info("Reference implementation figures: 282 entities initially covered + 208 subsequently added = 490. Retain the source date when presenting these figures.")

    with st.expander("ⓘ Compliance vs Offset — quick explainer"):
        st.markdown("""
        **Compliance mechanism:** notified obligated entities are assessed against applicable GHG Emission Intensity (GEI) targets.  
        **Offset mechanism:** eligible project activities follow approved methodologies for quantified emission reductions/removals.  
        **CCC:** Carbon Credit Certificate used within the CCTS framework.  
        This dashboard does not determine official issuance or surrender obligations.
        """)

    st.markdown("---")

    # ── Carbon-to-finance simulator ───────────────────────────────────────────
    st.markdown("### 💰 Carbon Cost & Financial Impact")
    st.caption("Illustrative scenario: GEI performance → indicative carbon position → financial sensitivity. Not an official compliance calculation or carbon-price forecast.")
    i1,i2,i3 = st.columns(3)
    production = i1.number_input("Annual Production ⓘ", min_value=1.0, value=1000000.0, step=10000.0,
                                 help="Illustrative annual output. Use the same production basis as the GEI denominator.")
    target_gei = i2.number_input("Target GEI (tCO₂e/unit) ⓘ", min_value=0.001, value=0.700, step=0.010, format="%.3f",
                                 help="Illustrative target. Use the applicable notified value when analysing a real obligated entity.")
    actual_gei = i3.number_input("Actual GEI (tCO₂e/unit) ⓘ", min_value=0.001, value=0.750, step=0.010, format="%.3f",
                                 help="Actual or scenario GEI on the same basis as the target.")
    carbon_price = st.slider("Assumed CCC Price (₹/tCO₂e) ⓘ", 100, 3000, 1000, 100,
                             help="User-defined sensitivity assumption; not an observed or forecast market price.")

    gei_gap = actual_gei-target_gei
    qty = abs(gei_gap*production)
    value = qty*carbon_price
    per_unit = value/production if production else 0
    if gei_gap>0:
        position_label="Indicative Carbon Position"; finance_label="Potential Carbon Cost"; status="🟠 Potential compliance exposure"
    elif gei_gap<0:
        position_label="Indicative Carbon Position"; finance_label="Potential Carbon Value"; status="🟢 Potential carbon-credit opportunity"
    else:
        position_label="Indicative CCC Position"; finance_label="Indicative Financial Impact"; status="🔵 At assumed GEI target"
    o1,o2,o3 = st.columns(3)
    o1.metric(position_label, f"{qty:,.0f}", help="Absolute GEI gap × annual production; analytical quantity only.")
    o2.metric(finance_label, f"₹{value/1e7:,.2f} Cr", help="Indicative quantity × assumed CCC price.")
    o3.metric("Impact per Unit", f"₹{per_unit:,.2f}", help="Illustrative financial impact divided by annual production.")
    st.info(f"{status}. Actual certificate issuance/surrender depends on applicable CCTS rules, verification and official procedures.")

    prices=[250,500,750,1000,1500,2000,2500,3000]
    sensitivity=pd.DataFrame({"Assumed Carbon Price (₹/tCO₂e)":prices,
                              "Financial Impact (₹ Cr)":[qty*p/1e7 for p in prices]})
    fig=px.line(sensitivity,x="Assumed Carbon Price (₹/tCO₂e)",y="Financial Impact (₹ Cr)",markers=True,
                title=f"{case_sector}: Carbon-Price Sensitivity")
    fig.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("#### 💼 ESG Analyst Interpretation")
    if gei_gap>0:
        st.info(f"In this illustrative {case_sector} scenario, actual GEI is {gei_gap:.3f} tCO₂e/unit above the assumed target. The model indicates about {qty:,.0f} tCO₂e of potential carbon exposure, worth roughly ₹{value/1e7:,.2f} crore at the selected scenario price. This strengthens the case for comparing decarbonisation investment with potential carbon-cost exposure.")
    elif gei_gap<0:
        st.success(f"In this illustrative {case_sector} scenario, actual GEI is {abs(gei_gap):.3f} tCO₂e/unit below the assumed target. The model indicates about {qty:,.0f} tCO₂e of potential surplus, with an illustrative value of ₹{value/1e7:,.2f} crore at the selected scenario price. Treat this as analytical sensitivity, not an issuance forecast.")
    else:
        st.info("The scenario is exactly at the assumed GEI target. Future target tightening, technology transition and carbon-price conditions can still affect transition exposure.")

    st.markdown("---")

    # ── Materiality ───────────────────────────────────────────────────────────
    st.markdown("### 🎯 ESG Materiality Matrix")
    st.caption("Sector-based analytical template. Scores are illustrative research inputs—not external ESG ratings.")
    mat_sector = st.selectbox("Sector template ⓘ", ["Steel & Cement","Banking & Financial Services","IT & Technology","Pharma & Healthcare","Automobile"],
                              help="Select a sector to see how material ESG topics can change with business model and stakeholder impact.")
    templates={
        "Steel & Cement":{"Climate & GHG":(9.5,9.5),"Energy":(8.8,9.0),"Water":(7.5,7.8),"Worker Safety":(8.5,8.2),"Waste & Circularity":(7.8,7.5),"Business Ethics":(7.0,8.0)},
        "Banking & Financial Services":{"Financed Emissions":(8.8,9.2),"Data Privacy":(8.0,9.0),"Responsible Lending":(8.5,8.8),"Business Ethics":(8.2,9.2),"Human Capital":(7.0,7.5),"Operational GHG":(5.0,5.5)},
        "IT & Technology":{"Energy & Data Centres":(8.0,8.2),"Data Privacy":(8.8,9.3),"Human Capital":(7.8,8.0),"E-waste":(7.0,6.8),"Business Ethics":(7.5,8.5),"Water":(6.5,6.2)},
        "Pharma & Healthcare":{"Product Quality":(9.3,9.5),"Patient Safety":(9.5,9.4),"Water & Effluents":(8.0,7.8),"Waste":(7.8,7.5),"Ethics & Compliance":(8.8,9.0),"GHG & Energy":(6.8,7.0)},
        "Automobile":{"Climate & GHG":(8.8,9.0),"EV Transition":(9.0,9.2),"Supply Chain":(8.2,8.5),"Product Safety":(8.8,8.8),"Circularity":(7.8,7.5),"Worker Safety":(7.2,7.0)}
    }
    mat=pd.DataFrame([{"Issue":k,"Impact Materiality":v[0],"Financial Materiality":v[1]} for k,v in templates[mat_sector].items()])
    fig=px.scatter(mat,x="Financial Materiality",y="Impact Materiality",text="Issue",size=[18]*len(mat),
                   range_x=[4,10],range_y=[4,10],title=f"Illustrative Double-Materiality View — {mat_sector}")
    fig.update_traces(textposition="top center")
    fig.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig,use_container_width=True)
    st.caption("ⓘ Impact materiality considers effects on people/environment; financial materiality considers potential effects on enterprise value, costs, revenue, assets, financing or risk. Validate scoring with evidence and stakeholder engagement in a real study.")

    st.markdown("---")

    # ── Disclosure readiness ──────────────────────────────────────────────────
    st.markdown("### 📋 BRSR / ESG Disclosure Readiness")
    st.caption("A data-gap checklist—not a regulatory-compliance opinion or external assurance conclusion.")
    disclosure_items={
        "Environmental":["Scope 1 & Scope 2 GHG emissions","Energy consumption & renewable share","Water withdrawal/consumption","Waste generation & recovery"],
        "Social":["Workforce composition & diversity","Health & safety indicators","Training & development","Employee turnover/attrition"],
        "Governance":["Board/management ESG oversight","Ethics & anti-corruption controls","Grievance mechanisms","ESG data review/assurance evidence"]
    }
    total=0; ready=0
    cols=st.columns(3)
    for col,(pillar,items) in zip(cols,disclosure_items.items()):
        with col:
            st.markdown(f"#### {pillar}")
            for item in items:
                total+=1
                if st.checkbox(item, value=False, key=f"brsr_final_{pillar}_{item}"):
                    ready+=1
    readiness=ready/total*100 if total else 0
    r1,r2,r3=st.columns(3)
    r1.metric("Data Points Ready",f"{ready}/{total}")
    r2.metric("Checklist Coverage",f"{readiness:.0f}%",help="Simple completion percentage; not a BRSR compliance score.")
    r3.metric("Data Gaps",str(total-ready))
    st.progress(readiness/100)
    if readiness<50: st.warning("Priority: establish ESG data owners, definitions, evidence trails and reporting controls.")
    elif readiness<85: st.info("Next step: close remaining data gaps and strengthen review/assurance evidence for material KPIs.")
    else: st.success("High checklist coverage. Validate definitions, boundaries, evidence and assurance requirements before reporting.")

    st.markdown("---")

    # ── Decarbonisation + management action ───────────────────────────────────
    st.markdown("### 📉 Decarbonisation & Management Action Planner")
    st.caption("Test user-defined reduction levers, then compare management actions. Percentages and priorities are scenario assumptions unless sourced.")
    d1,d2=st.columns([1,1.4])
    with d1:
        baseline=st.number_input("Baseline emissions (tCO₂e) ⓘ",min_value=0.0,value=1000000.0,step=10000.0,
                                 help="Define the reporting boundary and baseline year when using real company data.")
        renewable=st.slider("Renewable electricity reduction %",0,40,12,key="final_renew")
        efficiency=st.slider("Energy-efficiency reduction %",0,30,8,key="final_eff")
        fuel=st.slider("Fuel/process transition reduction %",0,30,10,key="final_fuel")
        supply=st.slider("Supply-chain initiatives reduction %",0,30,5,key="final_supply")
    total_reduction=min(renewable+efficiency+fuel+supply,95)
    residual=baseline*(1-total_reduction/100)
    with d2:
        decarb=pd.DataFrame({"Stage":["Baseline","Renewable","Efficiency","Fuel / Process","Supply Chain","Residual"],
                             "Emissions":[baseline,baseline*(1-renewable/100),baseline*(1-(renewable+efficiency)/100),baseline*(1-(renewable+efficiency+fuel)/100),residual,residual]})
        fig=px.line(decarb,x="Stage",y="Emissions",markers=True,title="Illustrative Emissions Pathway")
        fig.update_layout(**PLOT_LAYOUT,yaxis_title="tCO₂e")
        st.plotly_chart(fig,use_container_width=True)
    x1,x2,x3=st.columns(3)
    x1.metric("Modelled Reduction",f"{total_reduction}%")
    x2.metric("Residual Emissions",f"{residual:,.0f} tCO₂e")
    x3.metric("Avoided vs Baseline",f"{baseline-residual:,.0f} tCO₂e")

    action_df=pd.DataFrame({
        "Management Action":["Energy efficiency","Renewable electricity","Fuel / process transition","Supply-chain engagement"],
        "Emission Impact":["Medium","High","High","Medium"],
        "Indicative Cost":["Low–Medium","Medium","High","Medium"],
        "Time Horizon":["Short","Short–Medium","Medium–Long","Medium"],
        "Decision Lens":["Operational savings","Power decarbonisation","Strategic technology capex","Value-chain engagement"]
    })
    st.markdown("#### 🧩 Management Action Prioritisation")
    st.dataframe(action_df,use_container_width=True,hide_index=True)
    st.caption("ⓘ This table is an illustrative management framework. Replace qualitative assumptions with company/sector evidence for a formal case study.")

    st.markdown("---")

    # ── Data transparency ─────────────────────────────────────────────────────
    st.markdown("### 🔎 Data Transparency")
    st.caption("A compact guide to how information is classified across the dashboard.")
    st.markdown("""
    <div style='background:linear-gradient(135deg,rgba(13,49,31,.88),rgba(11,40,38,.88));border:1px solid rgba(67,255,136,.28);border-radius:14px;padding:17px 20px;margin-top:8px;'>
      <div style='display:flex;flex-wrap:wrap;gap:12px 26px;align-items:center;'>
        <div><span style='color:#43ff88'>●</span> <b style='color:#fff'>Reported</b> <span style='color:#8da99a;font-size:.82rem'>Company disclosures</span></div>
        <div><span style='color:#43ff88'>●</span> <b style='color:#fff'>Government</b> <span style='color:#8da99a;font-size:.82rem'>Official sources</span></div>
        <div><span style='color:#43ff88'>●</span> <b style='color:#fff'>Calculated</b> <span style='color:#8da99a;font-size:.82rem'>Derived metrics</span></div>
        <div><span style='color:#43ff88'>●</span> <b style='color:#fff'>Modelled</b> <span style='color:#8da99a;font-size:.82rem'>Analytical outputs</span></div>
        <div><span style='color:#43ff88'>●</span> <b style='color:#fff'>Assumption</b> <span style='color:#8da99a;font-size:.82rem'>User scenarios</span></div>
      </div>
      <div style='border-top:1px solid rgba(255,255,255,.08);margin-top:14px;padding-top:10px;color:#91aa9b;font-size:.80rem'>
        ⓘ Tooltips and captions identify definitions, assumptions and interpretation where relevant.
      </div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# TAB 5 — COMPANY ESG
# ─────────────────────────────────────────────────────────────────────────────
with tab5:
    st.subheader("🏢 Company ESG — India & Global (MSCI ESG + Bloomberg FY2025)")
    country_f = st.multiselect("Country", COMPANY_ESG["Country"].unique().tolist(), default=COMPANY_ESG["Country"].unique().tolist())
    sector_f  = st.multiselect("Sector",  COMPANY_ESG["Sector"].unique().tolist(),  default=COMPANY_ESG["Sector"].unique().tolist())
    fco = COMPANY_ESG[COMPANY_ESG["Country"].isin(country_f) & COMPANY_ESG["Sector"].isin(sector_f)]

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(fco.sort_values("ESG_Score"), x="ESG_Score", y="Company", orientation="h",
                     title="ESG Score by Company", color="ESG_Score", color_continuous_scale=GREEN_SEQ,
                     hover_data={"Country":True,"Sector":True})
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(fco, x="CO2_Intensity", y="ESG_Score", size="Renewable_Pct",
                         color="Sector", hover_name="Company",
                         title="CO₂ Intensity vs ESG Score (bubble = renewable %)", size_max=40)
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    fig = px.bar(fco.sort_values("Scope1_Mt", ascending=False),
                 x="Company", y="Scope1_Mt", color="Sector",
                 title="Scope 1 Emissions (Mt CO₂e) — Company Level")
    fig.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(fco, use_container_width=True)
# ─────────────────────────────────────────────────────────────────────────────
# TAB 6 — Climate Targets
# ─────────────────────────────────────────────────────────────────────────────
with tab6:
    st.subheader("📊 IPCC AR6 Scenarios & India NDC 2030 Progress")
    c1, c2 = st.columns(2)
    with c1:
        sc = pd.DataFrame({
            "Scenario":["SSP1-1.9 (Best)","SSP1-2.6","SSP2-4.5","SSP3-7.0","SSP5-8.5 (Worst)"],
            "2050":     [1.0, 1.5, 2.0, 2.6, 3.0],
            "2100":     [1.0, 1.8, 2.7, 3.6, 4.4],
        })
        fig = px.bar(sc, x="Scenario", y=["2050","2100"], barmode="group",
                     title="IPCC AR6 Warming Scenarios (°C)",
                     color_discrete_map={"2050":"#4dff91","2100":"#ff6b6b"})
        fig.add_hline(y=1.5, line_dash="dash", line_color="white", annotation_text="1.5°C Paris")
        fig.add_hline(y=2.0, line_dash="dot",  line_color="#ffcc00", annotation_text="2°C Paris")
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        # Updated 2026 NDC progress figures (MNRE/MoEF 2026)
        ndc = pd.DataFrame({
            "Target":["Emissions Intensity\nReduction (%)","Non-Fossil Capacity\n(GW)","Carbon Sink\n(Bn tCO₂e)","EV Share\n(%)"],
            "NDC 2030 Target":[45, 500, 2.5, 30],
            "Progress 2026":  [38, 270, 1.4, 14],
        })
        fig = px.bar(ndc, x="Target", y=["NDC 2030 Target","Progress 2026"], barmode="group",
                     title="India NDC 2030 Targets vs 2026 Progress — MoEF/MNRE",
                     color_discrete_map={"NDC 2030 Target":"#2a6a3a","Progress 2026":"#4dff91"})
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    tp = pd.DataFrame({
        "System":       ["Arctic Sea Ice","Greenland Ice Sheet","W. Antarctic Ice","Amazon Rainforest",
                         "AMOC Slowdown","Permafrost Carbon","Coral Reefs","Indian Monsoon Shift"],
        "Threshold_°C": [1.5, 1.5, 1.5, 3.5, 4.0, 1.5, 1.5, 3.0],
        "Risk_Score":   [9,   8,   8,   7,   6,   9,   9,   7],
        "India_Impact": [4,   6,   8,   3,   7,   5,   5,   10],
    })
    fig = px.scatter(tp, x="Threshold_°C", y="Risk_Score", size="India_Impact", color="System",
                     hover_name="System",
                     title="IPCC AR6 Climate Tipping Points (bubble size = India impact score)", size_max=45)
    fig.add_vline(x=1.5, line_dash="dash", line_color="#ff6b6b", annotation_text="1.5°C threshold")
    fig.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    **Key Sources:**
    - IPCC AR6 SPM (2021): https://www.ipcc.ch/assessment-report/ar6/
    - IEA Renewables 2025 / World Energy Outlook 2025
    - WMO State of Global Climate 2026
    - MoEF State of Environment Report 2025: https://moef.gov.in/
    - India Updated NDC 2022 | MNRE Annual Report 2026
    - NDMA Climate Vulnerability Atlas 2022
    - Global Carbon Project 2026
    - EU CBAM: https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism
    """)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 7 — EXPORT
# ─────────────────────────────────────────────────────────────────────────────
with tab7:
    st.subheader("📄 Download Data & Reports")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.download_button("📊 Global Data (CSV)", GLOBAL_DATA.to_csv(index=False).encode(),
                           "climate_global_2026.csv", "text/csv", use_container_width=True)
    with c2:
        st.download_button("🇮🇳 India Data (CSV)", INDIA_DATA.to_csv(index=False).encode(),
                           "climate_india_2026.csv", "text/csv", use_container_width=True)
    with c3:
        st.download_button("🏢 Company ESG (CSV)", COMPANY_ESG.to_csv(index=False).encode(),
                           "company_esg_2026.csv", "text/csv", use_container_width=True)

    yr_dl = st.selectbox("Year for comparison download", sorted(GLOBAL_DATA["Year"].unique(), reverse=True), key="dl_yr")
    g_dl = GLOBAL_DATA[GLOBAL_DATA["Year"]==yr_dl].iloc[0]
    i_dl = INDIA_DATA[INDIA_DATA["Year"]==yr_dl].iloc[0]
    comp_df = pd.DataFrame({
        "Metric":["CO2_Emissions_Gt","Renewable_Energy_%","ESG_Score","Temp_Anomaly_C","Physical_Risk","Transition_Risk"],
        "Global": [g_dl.CO2_Emissions, g_dl.Renewable_Energy, g_dl.ESG_Score, g_dl.Temp_Anomaly, g_dl.Physical_Risk, g_dl.Transition_Risk],
        "India":  [i_dl.CO2_Emissions, i_dl.Renewable_Energy, i_dl.ESG_Score, i_dl.Temp_Anomaly, i_dl.Physical_Risk, i_dl.Transition_Risk],
    })
    st.download_button(f"🆚 Global vs India Comparison {yr_dl} (CSV)", comp_df.to_csv(index=False).encode(),
                       f"global_vs_india_{yr_dl}.csv", "text/csv", use_container_width=True)

    st.info("💡 Hover over any chart → click the 📷 icon to export as PNG image.")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 8 — INDIA vs WORLD DEEP DIVE (NEW)
# ─────────────────────────────────────────────────────────────────────────────
with tab8:
    st.subheader("🔍 India vs World — Deep Dive Comparison")
    st.markdown(
        "<p style='color:#90c0a0'>Granular analysis of how India compares to global benchmarks across "
        "ESG dimensions, emissions intensity, renewable targets, regulatory frameworks, and climate finance. "
        "Sources: IEA 2025, WMO 2026, MSCI ESG, BloombergNEF, SEBI, MoEF, Climate Policy Initiative 2025</p>",
        unsafe_allow_html=True
    )

    # ── Section A: Emissions Profile ──────────────────────────────────────────
    st.markdown("### 🌫️ A. Emissions Profile — India vs Global Peers")

    em_compare = pd.DataFrame({
        "Country":        ["India","China","USA","EU-27","Japan","Global Avg"],
        "Total_CO2_Gt":   [3.04, 12.1, 4.9, 2.6, 1.0, 38.3],
        "PerCapita_tCO2": [2.2,  8.4,  14.7, 5.9, 8.2, 4.8],
        "Intensity_gCO2_per_kWh": [628, 498, 369, 231, 474, 436],
        "GDP_CO2_kg_per_USD": [0.31, 0.52, 0.26, 0.16, 0.22, 0.35],
    })

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(em_compare, x="Country", y="PerCapita_tCO2",
                     title="Per-Capita CO₂ Emissions (tCO₂/person, 2025) — IEA 2025",
                     color="PerCapita_tCO2", color_continuous_scale=["#0d3a1a","#ffcc00","#ff6b6b"])
        fig.add_hline(y=2.2, line_dash="dash", line_color="#4dff91", annotation_text="India (2.2t)")
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.bar(em_compare, x="Country", y="Intensity_gCO2_per_kWh",
                     title="Grid Emission Intensity (gCO₂/kWh, 2025) — IEA 2025",
                     color="Intensity_gCO2_per_kWh", color_continuous_scale=["#0d3a1a","#ffcc00","#ff6b6b"])
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    st.info("🇮🇳 **India insight:** India's per-capita emissions (2.2 tCO₂) are less than half the global average (4.8t) and 6.7x lower than the US — making India's historical responsibility argument central to COP negotiations.")

    # ── Section B: Renewable Energy Race ──────────────────────────────────────
    st.markdown("### ⚡ B. Renewable Energy — India vs World")

    renew_compare = pd.DataFrame({
        "Country":  ["India","China","USA","EU-27","Japan","Brazil","Global"],
        "Renew_Pct_2020": [25.2, 28.4, 20.1, 38.0, 22.0, 83.0, 17.5],
        "Renew_Pct_2023": [34.4, 31.6, 22.4, 44.7, 23.5, 87.0, 22.0],
        "Renew_Pct_2026": [46.3, 36.0, 26.2, 51.0, 25.0, 90.0, 30.1],
        "Target_2030":    [66.0, 50.0, 42.0, 65.0, 36.0, 92.0, 40.0],
    })

    fig = go.Figure()
    for col, color, name in [
        ("Renew_Pct_2020","#1a5a2a","2020"),
        ("Renew_Pct_2023","#2a9a4a","2023"),
        ("Renew_Pct_2026","#4dff91","2026"),
        ("Target_2030","#ffcc00","2030 Target"),
    ]:
        fig.add_trace(go.Bar(x=renew_compare["Country"], y=renew_compare[col], name=name))
    fig.update_layout(**PLOT_LAYOUT, barmode="group",
                      title="Renewable Share (%) — 2020, 2023, 2026, and 2030 Targets")
    st.plotly_chart(fig, use_container_width=True)

    st.info("🇮🇳 **India insight:** India's renewable share grew 20.5 percentage points from 2016 to 2026, the fastest growth rate among major G20 economies. India added 26 GW of solar in 2025 alone (MNRE 2026).")

    # ── Section C: ESG Framework Comparison ───────────────────────────────────
    st.markdown("### 📋 C. ESG Regulatory Framework — India vs Global")

    esg_framework = pd.DataFrame({
        "Framework": ["SEBI BRSR Core (India)", "EU CSRD (Europe)", "SEC Climate Rule (USA)",
                      "TCFD (Global)", "ISSB S1/S2 (Global)", "GRI Standards (Global)",
                      "China ESG Guidelines", "BRSR Basic (India)"],
        "Mandatory": ["Yes (Top 150 FY2025)", "Yes (2024+)", "Delayed/Partial",
                      "Voluntary", "Voluntary/Adopted", "Voluntary",
                      "Yes (Listed Co.)", "Yes (Top 1000 FY2024)"],
        "Scope_Coverage": [3, 3, 1, 3, 3, 3, 1, 2],
        "Year_Effective": [2025, 2024, 2026, 2017, 2024, 2000, 2022, 2024],
        "Enforcer": ["SEBI","EFRAG/EU","SEC","FSB","IFRS Foundation","GRI","CSRC","SEBI"],
    })

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(esg_framework, x="Framework", y="Scope_Coverage",
                     title="ESG Framework — Scope Coverage (1=Scope1, 2=+Scope2, 3=+Scope3)",
                     color="Scope_Coverage", color_continuous_scale=GREEN_SEQ,
                     hover_data={"Mandatory":True,"Enforcer":True,"Year_Effective":True})
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(esg_framework, x="Year_Effective", y="Scope_Coverage",
                         color="Mandatory", size="Scope_Coverage",
                         hover_name="Framework",
                         title="ESG Frameworks — Adoption Year vs Scope Coverage",
                         color_discrete_map={"Yes (Top 150 FY2025)":"#4dff91","Yes (2024+)":"#00c8ff",
                                              "Delayed/Partial":"#ffcc00","Voluntary":"#ff6b6b",
                                              "Voluntary/Adopted":"#b266ff","Yes (Listed Co.)":"#4dff91",
                                              "Yes (Top 1000 FY2024)":"#2a9a4a"})
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    st.info("🇮🇳 **India insight:** SEBI BRSR Core (FY2025) mandates Scope 3 disclosure for India's top 150 listed companies — making India one of the few emerging markets with mandatory Scope 3 reporting, comparable to EU's CSRD.")

    # ── Section D: Climate Finance ─────────────────────────────────────────────
    st.markdown("### 💰 D. Climate Finance Flows — India vs Global")

    fin_data = pd.DataFrame({
        "Region":    ["India","China","USA","EU-27","Global Total","Emerging Markets"],
        "Green_Finance_USD_Bn_2025": [49, 758, 312, 430, 1950, 380],
        "Green_Bond_USD_Bn_2025":    [22, 110, 280, 390, 1100, 180],
        "Climate_Vulnerability_Index": [72, 46, 33, 25, 50, 68],
    })

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(fin_data, x="Region", y="Green_Finance_USD_Bn_2025",
                     title="Green Finance Flows (USD Bn, 2025) — Climate Policy Initiative 2025",
                     color="Green_Finance_USD_Bn_2025", color_continuous_scale=GREEN_SEQ)
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(fin_data, x="Green_Finance_USD_Bn_2025", y="Climate_Vulnerability_Index",
                         size="Green_Bond_USD_Bn_2025", hover_name="Region",
                         title="Green Finance vs Vulnerability (bubble = Green Bond issuance)",
                         size_max=50, color="Region")
        fig.update_layout(**PLOT_LAYOUT)
        st.plotly_chart(fig, use_container_width=True)

    st.info("🇮🇳 **India insight:** India received $49Bn in green finance in 2025 — yet faces a $170Bn annual gap to meet its NDC targets by 2030 (Climate Policy Initiative 2025). India's Climate Finance Gap is the largest unmet need among non-OECD G20 economies.")

    # ── Section E: Physical Risk Deep Dive ───────────────────────────────────
    st.markdown("### 🌡️ E. Physical Risk Breakdown — India vs Global Peers")

    phys_risk = pd.DataFrame({
        "Country":       ["India","Bangladesh","Pakistan","USA","China","Germany","Australia","Brazil"],
        "Heat_Stress":   [92, 88, 94, 56, 63, 31, 78, 71],
        "Flood_Risk":    [84, 97, 79, 63, 72, 45, 52, 77],
        "Drought_Risk":  [79, 61, 88, 59, 67, 38, 86, 73],
        "Sea_Level_Risk":[71, 96, 43, 54, 62, 39, 58, 65],
        "Cyclone_Risk":  [68, 84, 51, 72, 58, 12, 63, 46],
    })

    fig = px.bar(phys_risk, x="Country",
                 y=["Heat_Stress","Flood_Risk","Drought_Risk","Sea_Level_Risk","Cyclone_Risk"],
                 title="Physical Risk Components by Country (IPCC AR6 WGII + ND-GAIN 2025)",
                 barmode="group",
                 color_discrete_sequence=["#ff6b6b","#00c8ff","#ffcc00","#4dff91","#b266ff"])
    fig.update_layout(**PLOT_LAYOUT)
    st.plotly_chart(fig, use_container_width=True)

    st.info("🇮🇳 **India insight:** India ranks in the top 3 globally for heat stress and flood risk among major economies. The 2025 monsoon season brought 347 extreme weather events — a record high (MoEF SoE 2025). 600M+ Indians are exposed to high climate risk by 2030 (IPCC AR6).")

    # ── Section F: Summary Scorecard ──────────────────────────────────────────
    st.markdown("### 🏆 F. India vs Global — At-a-Glance Scorecard (2026)")

    scorecard = pd.DataFrame({
        "Dimension": [
            "Per-Capita CO₂ (tCO₂/yr)",
            "Renewable Share (%)",
            "ESG Score (/100)",
            "Physical Risk (/100)",
            "Transition Risk (/100)",
            "Green Finance (USD Bn)",
            "Grid Intensity (gCO₂/kWh)",
            "NDC Ambition (1-5 scale)",
        ],
        "India 2026": [2.2, 46.3, 82, 93, 84, 49, 628, 4],
        "Global Avg 2026": [4.8, 30.1, 80, 89, 85, 325, 436, 3],
        "India Better?": ["✅ Yes", "✅ Yes", "✅ Yes", "❌ Worse", "⚠️ Similar", "❌ Lower", "❌ Worse", "✅ Yes"],
    })

    c1, c2 = st.columns([2, 1])
    with c1:
        fig = go.Figure()
        categories = scorecard["Dimension"].tolist()
        # Normalize to 0-100 for radar
        india_norm = [100, 46.3, 82, 100-93, 100-84, 25, 100-(628/10), 80]
        global_norm = [100*(4.8/4.8 - 1) if x == 0 else 100*(1 - 4.8/9.6) for x in [1]]+[30.1, 80, 100-89, 100-85, 17, 100-(436/10), 60]
        india_radar   = [45.8, 46.3, 82, 7, 16, 25, 37.2, 80]  # higher = better
        global_radar  = [0.0,  30.1, 80, 11, 15, 17, 56.4, 60]

        fig.add_trace(go.Scatterpolar(r=india_radar, theta=categories, fill='toself',
                                       name='India 2026', line_color='#4dff91', fillcolor='rgba(77,255,145,0.15)'))
        fig.add_trace(go.Scatterpolar(r=global_radar, theta=categories, fill='toself',
                                       name='Global Avg 2026', line_color='#00c8ff', fillcolor='rgba(0,200,255,0.1)'))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100],
                                       gridcolor='#1a4a2a', linecolor='#2a6a3a'),
                       bgcolor='rgba(13,43,26,0.6)',
                       angularaxis=dict(color='#c0e0c0')),
            paper_bgcolor='rgba(0,0,0,0)', font_color='#c0e0c0',
            title=dict(text="India vs Global — Radar Scorecard (higher = better outcome)", font=dict(color='#4dff91', size=14)),
            legend=dict(bgcolor='#0d2b1a', bordercolor='#2a6a3a')
        )
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.markdown("#### 📋 Raw Scores")
        st.dataframe(
            scorecard[["Dimension","India 2026","Global Avg 2026","India Better?"]],
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")
    st.info("""
    **Key Sources for this tab:**
    - IEA World Energy Outlook 2025 & Emissions Statistics 2025
    - WMO State of Global Climate 2026
    - Climate Policy Initiative Global Landscape of Climate Finance 2025
    - MSCI ESG Ratings 2025 | BloombergNEF Energy Transition 2026
    - SEBI BRSR Core Circular (2023, FY2025 mandatory)
    - MoEF State of Environment Report 2025 | MNRE Annual Report 2026
    - ND-GAIN Country Index 2025: https://gain.nd.edu/
    - India BUR-4 (Biennial Update Report) 2025 — UNFCCC
    """)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 9 — CARBON INTELLIGENCE
# Environmental decision-support with a supporting climate-finance lens.
# Carbon-market methodology references: BEE Indian Carbon Market / CCTS.
# ─────────────────────────────────────────────────────────────────────────────
with tab9:
    st.subheader("🌱 Carbon Intelligence & Climate Finance Lab")
    st.markdown(
        "<p style='color:#90c0a0'>Translate an emissions baseline into a mitigation target, "
        "remaining decarbonisation gap, an indicative carbon-value scenario and environmental "
        "project pathways. Financial outputs are supporting indicators—not investment advice "
        "or a carbon-credit eligibility determination.</p>",
        unsafe_allow_html=True
    )

    st.info(
        "🔬 **Environmental-first workflow:** Climate pressure → GHG baseline → emission reduction → "
        "mitigation gap → project intervention → potential carbon mechanism → environmental co-benefits → climate finance."
    )

    # ── A. Carbon Reduction Calculator ────────────────────────────────────────
    st.markdown("### 🧮 A. Carbon Reduction Calculator")
    a1, a2, a3, a4 = st.columns(4)
    with a1:
        baseline_emissions = st.number_input(
            "Baseline emissions (tCO₂e)", min_value=1.0, value=100000.0,
            step=1000.0, key="ci_baseline"
        )
    with a2:
        current_emissions = st.number_input(
            "Current emissions (tCO₂e)", min_value=0.0, value=85000.0,
            step=1000.0, key="ci_current"
        )
    with a3:
        target_reduction_pct = st.slider(
            "Reduction target (%)", 0, 100, 25, key="ci_target_pct"
        )
    with a4:
        expected_future_reduction = st.number_input(
            "Additional expected reduction (tCO₂e)", min_value=0.0,
            value=5000.0, step=500.0, key="ci_future_reduction"
        )

    achieved_reduction = max(baseline_emissions - current_emissions, 0.0)
    achieved_pct = (achieved_reduction / baseline_emissions * 100) if baseline_emissions else 0.0
    target_reduction = baseline_emissions * target_reduction_pct / 100
    target_emissions = baseline_emissions - target_reduction
    remaining_gap = max(target_reduction - achieved_reduction, 0.0)
    projected_emissions = max(current_emissions - expected_future_reduction, 0.0)
    projected_reduction = max(baseline_emissions - projected_emissions, 0.0)
    projected_pct = projected_reduction / baseline_emissions * 100 if baseline_emissions else 0.0
    projected_gap = max(target_reduction - projected_reduction, 0.0)

    r1, r2, r3, r4 = st.columns(4)
    r1.metric("Emissions Reduced", f"{achieved_reduction:,.0f} tCO₂e")
    r2.metric("Reduction Achieved", f"{achieved_pct:.1f}%")
    r3.metric("Target Emissions", f"{target_emissions:,.0f} tCO₂e")
    r4.metric("Remaining Gap", f"{remaining_gap:,.0f} tCO₂e")

    progress = min(achieved_reduction / target_reduction, 1.0) if target_reduction > 0 else 1.0
    st.progress(progress)
    if target_reduction_pct == 0:
        st.success("✅ No reduction target has been set in this scenario.")
    elif remaining_gap <= 0:
        st.success("✅ **On Track / Target Achieved:** Current emissions meet or exceed the selected reduction target.")
    elif projected_gap <= 0:
        st.success(
            f"🟢 **Projected On Track:** The additional reduction scenario would lower emissions to "
            f"{projected_emissions:,.0f} tCO₂e ({projected_pct:.1f}% below baseline)."
        )
    else:
        st.warning(
            f"🟡 **Additional Mitigation Required:** After the expected reduction, an estimated "
            f"{projected_gap:,.0f} tCO₂e gap would remain against the selected target."
        )

    # ── B. Carbon Value Scenario ──────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### ♻️ B. Carbon Credit Scenario Simulator")
    b1, b2 = st.columns([1, 1])
    with b1:
        scenario_reduction = st.number_input(
            "Emission reduction used for scenario (tCO₂e)", min_value=0.0,
            value=float(round(projected_reduction)), step=500.0, key="ci_credit_reduction"
        )
        carbon_price = st.slider(
            "Illustrative carbon value (₹ per tCO₂e)", 0, 10000, 1000, 100,
            key="ci_carbon_price"
        )
        indicative_carbon_value = scenario_reduction * carbon_price
        st.metric("Illustrative Carbon Value", f"₹{indicative_carbon_value:,.0f}")
        st.caption("Scenario value = selected tCO₂e reduction × assumed ₹/tCO₂e. This is not a market-price forecast.")

    with b2:
        st.markdown("#### What this result means")
        st.markdown(
            f"A reduction scenario of **{scenario_reduction:,.0f} tCO₂e** at an assumed value of "
            f"**₹{carbon_price:,.0f}/tCO₂e** produces an illustrative value of "
            f"**₹{indicative_carbon_value:,.0f}**. The environmental result and the financial scenario "
            "are deliberately shown separately."
        )
        st.warning(
            "**Important:** An emission reduction does not automatically become an eligible or issued carbon credit. "
            "Applicability depends on the relevant methodology, baseline/additionality requirements, monitoring, "
            "validation/verification, registration and other CCTS requirements."
        )

    # ── C. Project Explorer ───────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🌳 C. Carbon Project Explorer")
    project_library = {
        "Grid-connected Renewable Electricity": {
            "sector": "Energy", "method": "BM EN01.001",
            "ghg": "Fossil-fuel electricity displacement",
            "action": "Generate grid-connected electricity from eligible renewable sources.",
            "benefits": "Lower operational GHG emissions; supports power-sector decarbonisation.",
            "monitor": "Electricity generation, baseline/grid parameters and applicable project emissions."
        },
        "Industrial Energy Efficiency / Fuel Switching": {
            "sector": "Industries", "method": "BM IN02.001",
            "ghg": "Fuel and process-energy related emissions",
            "action": "Improve energy efficiency and/or switch fuels in industrial facilities.",
            "benefits": "Reduced energy demand and GHG intensity; possible local air-quality co-benefits.",
            "monitor": "Energy/fuel use, production/activity data, baseline efficiency and project emissions."
        },
        "Landfill Methane Recovery": {
            "sector": "Waste Handling and Disposal", "method": "BM WA03.001",
            "ghg": "Methane from anaerobic decomposition of solid waste",
            "action": "Capture landfill methane for controlled recovery/use.",
            "benefits": "Methane abatement; improved landfill-gas management and potential local environmental benefits.",
            "monitor": "Gas flow, methane concentration, destruction/use and project/leakage emissions."
        },
        "Compressed Bio-gas (CBG)": {
            "sector": "Waste Handling and Disposal", "method": "BM WA03.003",
            "ghg": "Organic-waste and displaced fossil-fuel emissions",
            "action": "Convert eligible organic feedstock into compressed bio-gas.",
            "benefits": "Waste valorisation, methane management and fossil-fuel substitution potential.",
            "monitor": "Feedstock, gas production/use, energy inputs, leakage and applicable baseline parameters."
        },
        "Improved Rice Cultivation": {
            "sector": "Agriculture", "method": "BM AG04.002",
            "ghg": "Methane associated with rice cultivation",
            "action": "Apply improved rice-management practices covered by the methodology.",
            "benefits": "Potential methane reduction with agricultural resource-efficiency co-benefits.",
            "monitor": "Cultivation practices, area, water/management parameters and methodology-specific activity data."
        },
        "Livestock & Manure Methane Recovery": {
            "sector": "Agriculture", "method": "BM AG04.001",
            "ghg": "Methane from livestock/manure management",
            "action": "Recover methane from manure-management systems at eligible households/small farms.",
            "benefits": "Methane mitigation, improved waste handling and potential useful-energy recovery.",
            "monitor": "Livestock/manure activity, methane recovery, system operation and leakage."
        },
        "Afforestation / Reforestation": {
            "sector": "Forestry", "method": "BM FR05.002",
            "ghg": "Atmospheric CO₂ through biological sequestration",
            "action": "Afforestation/reforestation of eligible lands other than wetlands.",
            "benefits": "Carbon sequestration plus potential soil, habitat and ecosystem co-benefits.",
            "monitor": "Project boundary, biomass/carbon stocks, leakage, permanence-related parameters and land status."
        },
        "Mangrove Restoration / A&R": {
            "sector": "Forestry", "method": "BM FR05.001",
            "ghg": "Atmospheric CO₂ through coastal ecosystem sequestration",
            "action": "Afforestation/reforestation of eligible degraded mangrove habitats.",
            "benefits": "Carbon sequestration with potential biodiversity, shoreline and ecosystem-resilience co-benefits.",
            "monitor": "Mangrove area, biomass/carbon stocks, land eligibility, leakage and methodology parameters."
        },
        "Biomass Electricity & Heat": {
            "sector": "Energy", "method": "BM EN01.003",
            "ghg": "Fossil energy displaced by eligible biomass energy",
            "action": "Generate electricity and/or heat from eligible biomass under the approved methodology.",
            "benefits": "Potential fossil-energy displacement and productive biomass-resource use.",
            "monitor": "Biomass quantity/type, energy generation, fossil inputs, leakage and project emissions."
        },
    }

    selected_project = st.selectbox("Select a mitigation project pathway", list(project_library.keys()), key="ci_project")
    p = project_library[selected_project]
    p1, p2, p3 = st.columns(3)
    p1.metric("CCTS Sector", p["sector"])
    p2.metric("Potential Methodology", p["method"])
    p3.metric("Project Role", "Mitigation")

    st.markdown(f"**GHG source / pressure:** {p['ghg']}")
    st.markdown(f"**Mitigation intervention:** {p['action']}")
    st.markdown(f"**Potential environmental benefits:** {p['benefits']}")
    st.markdown(f"**Monitoring focus:** {p['monitor']}")
    st.caption(
        "Methodology match is an educational pre-screen only. Actual applicability must be checked against the "
        "latest BEE methodology, eligibility conditions and project-specific evidence."
    )

    # ── D. Climate Finance Lens ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 💰 D. Climate Finance Lens")
    st.markdown(
        "This section links an environmental intervention to financing needs without turning the dashboard into an investment tool."
    )

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        project_cost_lakh = st.number_input("Project cost (₹ lakh)", min_value=0.0, value=100.0, step=10.0, key="ci_cost")
    with f2:
        grant_pct = st.slider("Grant / subsidy (%)", 0, 100, 10, key="ci_grant")
    with f3:
        debt_pct = st.slider("Debt share of post-grant cost (%)", 0, 100, 60, key="ci_debt")
    with f4:
        annual_reduction = st.number_input("Expected annual reduction (tCO₂e)", min_value=1.0, value=5000.0, step=500.0, key="ci_annual_red")

    f5, f6 = st.columns(2)
    with f5:
        interest_rate = st.slider("Illustrative debt interest rate (%)", 0.0, 20.0, 9.0, 0.5, key="ci_rate")
    with f6:
        tenure = st.slider("Illustrative debt tenure (years)", 1, 20, 7, key="ci_tenure")

    project_cost = project_cost_lakh * 100000
    grant_amount = project_cost * grant_pct / 100
    post_grant_cost = max(project_cost - grant_amount, 0)
    debt_amount = post_grant_cost * debt_pct / 100
    equity_other = max(post_grant_cost - debt_amount, 0)
    annual_rate = interest_rate / 100
    if annual_rate > 0:
        annual_debt_service = debt_amount * (annual_rate * (1 + annual_rate) ** tenure) / (((1 + annual_rate) ** tenure) - 1)
    else:
        annual_debt_service = debt_amount / tenure
    mitigation_cost_intensity = post_grant_cost / (annual_reduction * tenure) if annual_reduction > 0 else 0

    fc1, fc2, fc3, fc4 = st.columns(4)
    fc1.metric("Grant / Subsidy", f"₹{grant_amount/100000:,.1f} lakh")
    fc2.metric("Indicative Debt", f"₹{debt_amount/100000:,.1f} lakh")
    fc3.metric("Equity / Other", f"₹{equity_other/100000:,.1f} lakh")
    fc4.metric("₹ per tCO₂e*", f"₹{mitigation_cost_intensity:,.0f}")
    st.caption(
        f"Illustrative annual debt service: ₹{annual_debt_service/100000:,.2f} lakh. "
        "*Simple project-cost intensity over the selected tenure; not an abatement-cost study, NPV/IRR calculation or investment recommendation."
    )

    # ── E. Marginal Abatement Cost Tool ──────────────────────────────────────
    st.markdown("#### 📊 Marginal Abatement Cost Tool")
    st.markdown(
        "Compare the simple cost of achieving a tonne of CO₂e reduction. This is an educational "
        "screening metric, not a full marginal abatement cost curve or investment appraisal."
    )
    m1, m2, m3 = st.columns(3)
    with m1:
        mac_project_cost_lakh = st.number_input(
            "Mitigation project cost (₹ lakh)", min_value=0.0, value=float(project_cost_lakh),
            step=10.0, key="ci_mac_cost"
        )
    with m2:
        mac_annual_reduction = st.number_input(
            "Annual avoided/reduced emissions (tCO₂e)", min_value=1.0, value=float(annual_reduction),
            step=100.0, key="ci_mac_reduction"
        )
    with m3:
        mac_life = st.slider("Expected mitigation life (years)", 1, 30, 10, key="ci_mac_life")

    mac_total_reduction = mac_annual_reduction * mac_life
    mac_cost_rupees = mac_project_cost_lakh * 100000
    simple_abatement_cost = mac_cost_rupees / mac_total_reduction if mac_total_reduction > 0 else 0
    mac1, mac2, mac3 = st.columns(3)
    mac1.metric("Lifetime Reduction", f"{mac_total_reduction:,.0f} tCO₂e")
    mac2.metric("Simple Abatement Cost", f"₹{simple_abatement_cost:,.0f}/tCO₂e")
    mac3.metric("Project Life", f"{mac_life} years")
    st.caption(
        "Simple abatement cost = project cost ÷ estimated lifetime emission reduction. "
        "It excludes operating costs, savings, discounting, financing effects and carbon revenues."
    )

    # ── F. Climate Finance Pre-Screener ───────────────────────────────────────
    st.markdown("#### 🌿 Climate Finance Relevance Pre-Screener")
    s1, s2 = st.columns(2)
    with s1:
        q_mitigation = st.checkbox("Project has a clear climate-mitigation objective", value=True, key="ci_q1")
        q_measurable = st.checkbox("GHG/environmental benefit can be measured and monitored", value=True, key="ci_q2")
    with s2:
        q_harm = st.checkbox("Potential significant environmental/social harms have been considered", value=False, key="ci_q3")
        q_transition = st.checkbox("Activity supports transition/resilience rather than locking in higher emissions", value=True, key="ci_q4")

    screen_score = sum([q_mitigation, q_measurable, q_harm, q_transition])
    if screen_score == 4:
        st.success("🟢 **Strong preliminary climate-finance relevance** — proceed to detailed taxonomy, safeguards and financing assessment.")
    elif screen_score >= 2:
        st.warning("🟡 **Potential climate-finance relevance** — additional evidence, safeguards or measurable criteria are needed.")
    else:
        st.error("🔴 **Insufficient information at pre-screen stage** — strengthen the climate objective, measurement plan and safeguards before assessment.")

    st.caption(
        "Educational pre-screen only. It does not certify taxonomy alignment, green-bond eligibility, bankability, carbon-credit eligibility or regulatory approval."
    )

    # ── G. Environmental Impact Translator ────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🌍 G. Environmental Impact Translator")
    impact_left, impact_right = st.columns([1.2, 1])
    with impact_left:
        if target_reduction_pct == 0:
            status_text = "No reduction target selected"
        elif remaining_gap <= 0:
            status_text = "Target achieved on current emissions"
        elif projected_gap <= 0:
            status_text = "Projected on track after planned mitigation"
        else:
            status_text = f"Projected mitigation gap: {projected_gap:,.0f} tCO₂e"

        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#0d3a1a,#0a2a2a);border:1px solid #2a6a3a;
                    border-radius:12px;padding:20px;line-height:1.75'>
          <b style='color:#4dff91'>Baseline:</b> {baseline_emissions:,.0f} tCO₂e<br>
          <b style='color:#4dff91'>Current reduction:</b> {achieved_reduction:,.0f} tCO₂e ({achieved_pct:.1f}%)<br>
          <b style='color:#4dff91'>Selected target:</b> {target_reduction_pct}% reduction<br>
          <b style='color:#4dff91'>Projected emissions:</b> {projected_emissions:,.0f} tCO₂e<br>
          <b style='color:#4dff91'>Target status:</b> {status_text}<br>
          <b style='color:#4dff91'>Selected pathway:</b> {selected_project}<br>
          <b style='color:#4dff91'>Potential methodology:</b> {p['method']}
        </div>
        """, unsafe_allow_html=True)

    with impact_right:
        st.markdown("#### Decision interpretation")
        st.markdown(
            "The dashboard first quantifies the **environmental mitigation gap**. Carbon-market and finance "
            "outputs are then used only to explore how a mitigation project might be supported, monitored and valued. "
            "This keeps environmental performance—not financial return—as the primary decision variable."
        )

    st.markdown("---")
    st.markdown("### 🔗 Official reference framework")
    st.markdown(
        "- **BEE Indian Carbon Market / CCTS:** compliance and voluntary offset mechanisms.\n"
        "- **BEE Offset Methodologies:** approved project methodologies across energy, industry, waste, agriculture and forestry.\n"
        "- **India Climate Finance Taxonomy framework:** useful for understanding mitigation, adaptation, transition and anti-greenwashing principles."
    )
    st.warning(
        "⚠️ **Academic-use note:** Carbon prices, financing assumptions and project outputs in this tab are user-defined scenarios. "
        "They are not live market quotations, investment advice, certification, verification or an assurance of Carbon Credit Certificate issuance."
    )

# ─────────────────────────────────────────────────────────────────────────────
# TAB 10 — METHODOLOGY & SOURCES
# ─────────────────────────────────────────────────────────────────────────────
with tab10:
    st.subheader("📚 Methodology, Data Status & Sources")
    st.markdown(
        "This dashboard separates official observations and inventories from latest/provisional "
        "indicators, policy targets and dashboard-modelled analytical indices. This distinction is "
        "important because environmental datasets are published at different frequencies and reference periods."
    )

    methodology_df = pd.DataFrame({
        "Data class": ["OBSERVED", "LATEST / PROJECTED", "INVENTORY", "MODELLED", "TARGET"],
        "Meaning": [
            "Completed historical observation for a stated reference period.",
            "Latest available, provisional, YTD or projected indicator; not treated as a completed annual observation.",
            "Official greenhouse-gas inventory for the latest published inventory year.",
            "Dashboard-derived comparative indicator used for analytical interpretation; not an official agency score.",
            "Policy, climate or scenario benchmark used for progress comparison."
        ],
        "Dashboard example": [
            "2025 global/India temperature",
            "Latest energy-capacity or emissions estimate",
            "India official GHG inventory",
            "Physical and transition risk indices",
            "Emission-reduction / climate targets"
        ]
    })
    st.dataframe(methodology_df, use_container_width=True, hide_index=True)

    st.markdown("### 🧭 How to interpret the risk scores")
    st.info(
        "Physical Risk and Transition Risk values shown as 0–100 scores are dashboard-modelled comparative indices. "
        "They are used to support relative interpretation across locations/sectors and should not be read as direct "
        "IPCC, ND-GAIN, NDMA or government-issued scores unless explicitly stated otherwise."
    )

    st.markdown("### 🌱 Carbon & climate-finance tools")
    st.markdown(
        "The Carbon Intelligence tools are scenario-based decision-support calculations. Emission reductions, "
        "carbon values, financing assumptions, abatement costs and pre-screening outputs are illustrative. "
        "They do not establish carbon-credit eligibility, taxonomy alignment, regulatory approval, project bankability or investment suitability."
    )

    st.markdown("### 🔗 Primary reference organisations")
    st.markdown(
        "- **WMO** — global climate observations and annual climate reporting.\n"
        "- **IMD** — India temperature and climate observations.\n"
        "- **UNFCCC / MoEFCC** — India's national GHG inventory and climate reporting.\n"
        "- **MNRE / CEA** — renewable and non-fossil electricity-capacity statistics.\n"
        "- **IEA / Global Carbon Project** — global energy and emissions indicators.\n"
        "- **BEE** — Indian Carbon Market / CCTS procedures and approved offset methodologies.\n"
        "- **IPCC** — climate-science assessment and scenario context.\n"
        "- **SEBI** — sustainability-reporting framework for listed entities."
    )

    st.markdown("### ⚠️ Key limitations")
    st.warning(
        "Reference years differ across indicators; 2026 is the dashboard's latest-data year, not a claim that every "
        "indicator is a completed 2026 observation. Company ESG and some comparative risk datasets are analytical/illustrative "
        "and should be replaced with traceable licensed or primary-source datasets for production-grade use."
    )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#609070;font-size:0.82rem'>"
    "🌍 Climate Risk & ESG Dashboard · Data updated to 2026 · "
    "Global: <a href='https://www.ipcc.ch' style='color:#4dff91'>IPCC AR6</a> + "
    "<a href='https://www.iea.org' style='color:#4dff91'>IEA 2025</a> | "
    "India: <a href='https://moef.gov.in' style='color:#4dff91'>MoEF SoE 2025</a> + "
    "<a href='https://mnre.gov.in' style='color:#4dff91'>MNRE 2026</a>"
    "</p>",
    unsafe_allow_html=True
)
