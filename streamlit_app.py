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
