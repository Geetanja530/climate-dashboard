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
          <b style='color:#315A9A'>Baseline:</b> {baseline_emissions:,.0f} tCO₂e<br>
          <b style='color:#315A9A'>Current reduction:</b> {achieved_reduction:,.0f} tCO₂e ({achieved_pct:.1f}%)<br>
          <b style='color:#315A9A'>Selected target:</b> {target_reduction_pct}% reduction<br>
          <b style='color:#315A9A'>Projected emissions:</b> {projected_emissions:,.0f} tCO₂e<br>
          <b style='color:#315A9A'>Target status:</b> {status_text}<br>
          <b style='color:#315A9A'>Selected pathway:</b> {selected_project}<br>
          <b style='color:#315A9A'>Potential methodology:</b> {p['method']}
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

# ─────────────────────────────────────────────────────────────────────────────
# TAB 11 — INSIGHTS & BLOG
# ─────────────────────────────────────────────────────────────────────────────
with tab11:
    st.subheader("Insights & Blog")
    st.markdown("Short explainers turn the dashboard's charts into practical climate and ESG context. This section is deliberately text-led to balance the analytical pages.")
    st.markdown("""
    <div class="blog-card"><h3>Why climate risk belongs in business decisions</h3><p>Climate risk is not only an environmental topic. Physical hazards can disrupt facilities, logistics and suppliers, while transition policies can change energy costs, technology choices and capital requirements. A useful dashboard therefore connects risk indicators with the business channels through which those risks may be felt.</p></div>
    <div class="blog-card"><h3>Reading an ESG score with context</h3><p>An ESG score is a starting point rather than a complete conclusion. The underlying issues differ by sector: emissions and energy can dominate heavy industry, while financed emissions, governance and data privacy can be more material in financial services. Always read the score alongside its methodology and source period.</p></div>
    <div class="blog-card"><h3>From carbon data to management action</h3><p>Carbon data becomes more useful when it answers a decision question. Where are emissions concentrated? What reduction pathway is technically realistic? What would a carbon-cost scenario mean for operations? The dashboard's carbon tools are designed to support those questions without presenting scenario outputs as official compliance results.</p></div>
    """, unsafe_allow_html=True)
    st.markdown("### Environment in focus")
    st.image("https://images.unsplash.com/photo-1473448912268-2022ce9509d8?auto=format&fit=crop&w=1600&q=80", use_container_width=True)
    st.caption("Forests act as carbon stores, support biodiversity and influence water systems. The image is used as visual context; dashboard metrics should still be interpreted using the cited datasets and methodologies.")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:#60708C;font-size:0.82rem'>"
    "🌍 Climate Risk & ESG Dashboard · Data updated to 2026 · "
    "Global: <a href='https://www.ipcc.ch' style='color:#315A9A'>IPCC AR6</a> + "
    "<a href='https://www.iea.org' style='color:#315A9A'>IEA 2025</a> | "
    "India: <a href='https://moef.gov.in' style='color:#315A9A'>MoEF SoE 2025</a> + "
    "<a href='https://mnre.gov.in' style='color:#315A9A'>MNRE 2026</a>"
