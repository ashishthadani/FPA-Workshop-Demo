import streamlit as st

import pandas as pd

import numpy as np
 
# -----------------------------

# Page Config

# -----------------------------
 
st.set_page_config(

    page_title="Global Cooler CAPEX Optimizer",

    page_icon="🍺",

    layout="wide"

)
 
# -----------------------------

# Custom CSS

# -----------------------------
 
st.markdown("""
<style>

.main {

    background-color: #f7f8fa;

}
 
.block-container {

    padding-top: 1.5rem;

}
 
.hero {

    background: linear-gradient(90deg, #061A40 0%, #123C69 100%);

    padding: 28px;

    border-radius: 18px;

    color: white;

    margin-bottom: 24px;

}
 
.hero h1 {

    color: white;

    font-size: 38px;

    margin-bottom: 6px;

}
 
.hero p {

    color: #dbe7ff;

    font-size: 17px;

}
 
.metric-card {

    background-color: white;

    padding: 20px;

    border-radius: 16px;

    box-shadow: 0 2px 10px rgba(0,0,0,0.06);

    text-align: center;

}
 
.green-box {

    background-color: #d9f7e5;

    color: #0b6b35;

    padding: 18px;

    border-radius: 14px;

    font-weight: 700;

    font-size: 24px;

    text-align: center;

}
 
.yellow-box {

    background-color: #fff4cc;

    color: #8a6400;

    padding: 18px;

    border-radius: 14px;

    font-weight: 700;

    font-size: 24px;

    text-align: center;

}
 
.orange-box {

    background-color: #ffe3c2;

    color: #9a4b00;

    padding: 18px;

    border-radius: 14px;

    font-weight: 700;

    font-size: 24px;

    text-align: center;

}
 
.red-box {

    background-color: #ffd6d6;

    color: #9b111e;

    padding: 18px;

    border-radius: 14px;

    font-weight: 700;

    font-size: 24px;

    text-align: center;

}
</style>

""", unsafe_allow_html=True)
 
# -----------------------------

# Logo

# -----------------------------

# Recommended: create a folder called "assets" and place the official ABI logo there as "abi_logo.png".

# Source it from the official ABI Creative Hub / brand portal, respecting company brand guidelines.
 
try:

    st.image("assets/abi_logo.png", width=180)

except:

    st.caption("AB InBev logo placeholder — add official logo as assets/abi_logo.png")
 
# -----------------------------

# Hero Section

# -----------------------------
 
st.markdown("""
<div class="hero">
<h1>Global Cooler CAPEX Optimizer</h1>
<p>

    AI-powered decision support to allocate cooler investment across ABI Zones and Countries

    based on Opportunity, Return and Risk.
</p>
</div>

""", unsafe_allow_html=True)
 
# -----------------------------

# Dummy ABI-style data

# -----------------------------
 
dummy_data = pd.DataFrame([

    ["MAZ", "Mexico", 42, 51, 18, 7, 650, 9, 14, 16, 12000000],

    ["MAZ", "Colombia", 34, 45, 24, 8, 620, 11, 9, 13, 7200000],

    ["MAZ", "Peru", 36, 43, 21, 6, 610, 10, 10, 14, 4600000],

    ["MAZ", "Ecuador", 48, 39, 17, 4, 600, 6, 18, 22, 1800000],

    ["LAS", "Argentina", 55, 47, 14, 3, 700, 5, 20, 24, 5500000],

    ["LAS", "Brazil", 58, 52, 16, 2, 680, 6, 17, 22, 15000000],

    ["Europe", "UK", 70, 38, 8, 1, 850, 3, 6, 28, 6000000],

    ["Europe", "Germany", 75, 36, 6, 1, 900, 2, 5, 30, 8000000],

    ["Africa", "South Africa", 30, 41, 26, 9, 580, 12, 15, 12, 4000000],

    ["Africa", "Nigeria", 25, 35, 32, 11, 540, 14, 22, 11, 3500000],

    ["APAC", "China", 60, 22, 20, 5, 780, 7, 16, 20, 9000000],

    ["APAC", "India", 28, 18, 35, 13, 500, 16, 19, 10, 7500000],

    ["North America", "USA", 78, 31, 5, 1, 950, 2, 4, 34, 15000000],

    ["North America", "Canada", 74, 29, 6, 1, 920, 2, 5, 33, 3000000],

], columns=[

    "Zone",

    "Country",

    "Cooler Coverage %",

    "Market Share %",

    "Zero Sales %",

    "Volume Growth %",

    "Cost per Cooler USD",

    "Expected Volume Uplift %",

    "Historical Impairment %",

    "Payback Months",

    "Annual Volume HL"

])
 
# -----------------------------

# Scoring Functions

# -----------------------------
 
def calculate_score(row):

    opportunity_score = (

        (100 - row["Cooler Coverage %"]) * 0.35 +

        (100 - row["Market Share %"]) * 0.15 +

        row["Zero Sales %"] * 0.25 +

        row["Volume Growth %"] * 2.5

    )
 
    return_score = (

        row["Expected Volume Uplift %"] * 4 +

        max(0, 36 - row["Payback Months"]) * 1.6 +

        max(0, 1000 - row["Cost per Cooler USD"]) / 20

    )
 
    risk_score = (

        row["Historical Impairment %"] * 2.0 +

        max(0, row["Payback Months"] - 18) * 1.8

    )
 
    final_score = opportunity_score * 0.40 + return_score * 0.45 - risk_score * 0.25

    return round(max(0, min(100, final_score)), 1)
 
 
def recommendation(score):

    if score >= 80:

        return "GO - Invest"

    elif score >= 65:

        return "Selective Invest"

    elif score >= 50:

        return "Hold / Reassess"

    else:

        return "NO GO"
 
 
def traffic_light_class(decision):

    if decision == "GO - Invest":

        return "green-box"

    elif decision == "Selective Invest":

        return "yellow-box"

    elif decision == "Hold / Reassess":

        return "orange-box"

    else:

        return "red-box"
 
 
def generate_rationale(row):

    decision = row["Decision"]
 
    if decision == "GO - Invest":

        return (

            f"{row['Country']} should receive cooler CAPEX because it combines a meaningful coverage gap, "

            f"strong expected volume uplift and an attractive payback profile. Risk is manageable based on "

            f"historical impairment levels."

        )
 
    if decision == "Selective Invest":

        return (

            f"{row['Country']} has an investable case, but deployment should be selective. "

            f"Focus on high-potential outlets, regions with low cooler coverage and customers with proven rotation."

        )
 
    if decision == "Hold / Reassess":

        return (

            f"{row['Country']} shows some opportunity, but the case is not strong enough for broad deployment. "

            f"The team should validate payback, execution risk and asset productivity before scaling."

        )
 
    return (

        f"{row['Country']} is not recommended for cooler investment at this stage. "

        f"The market should first reduce impairment risk, improve cooler productivity or strengthen expected return."

    )
 
 
# -----------------------------

# Sidebar Inputs

# -----------------------------
 
st.sidebar.title("Input Panel")
 
mode = st.sidebar.radio(

    "Select Mode",

    ["Use Dummy Portfolio", "Create Custom Market"]

)
 
global_budget = st.sidebar.number_input(

    "Total Available CAPEX Budget USD",

    min_value=0,

    value=10_000_000,

    step=500_000

)
 
if mode == "Use Dummy Portfolio":

    working_df = dummy_data.copy()
 
else:

    st.sidebar.subheader("Custom Market KPIs")
 
    zone = st.sidebar.selectbox(

        "Zone",

        ["MAZ", "LAS", "Europe", "Africa", "APAC", "North America"]

    )
 
    country = st.sidebar.text_input("Country", "New Market")
 
    cooler_coverage = st.sidebar.slider("Cooler Coverage %", 0, 100, 40)

    market_share = st.sidebar.slider("Market Share %", 0, 100, 35)

    zero_sales = st.sidebar.slider("Zero Sales Outlets %", 0, 100, 20)

    volume_growth = st.sidebar.slider("Volume Growth %", -10, 30, 6)

    cost_per_cooler = st.sidebar.number_input("Cost per Cooler USD", 100, 3000, 650, 50)

    expected_uplift = st.sidebar.slider("Expected Volume Uplift %", 0, 30, 8)

    impairment = st.sidebar.slider("Historical Impairment %", 0, 50, 12)

    payback = st.sidebar.slider("Payback Months", 1, 60, 18)

    annual_volume = st.sidebar.number_input("Annual Volume HL", 0, 100_000_000, 3_000_000, 100_000)
 
    working_df = pd.DataFrame([[

        zone,

        country,

        cooler_coverage,

        market_share,

        zero_sales,

        volume_growth,

        cost_per_cooler,

        expected_uplift,

        impairment,

        payback,

        annual_volume

    ]], columns=dummy_data.columns)
 
# -----------------------------

# Model Calculation

# -----------------------------
 
working_df["Investment Score"] = working_df.apply(calculate_score, axis=1)

working_df["Decision"] = working_df["Investment Score"].apply(recommendation)

working_df["AI Rationale"] = working_df.apply(generate_rationale, axis=1)
 
positive_df = working_df[working_df["Decision"].isin(["GO - Invest", "Selective Invest"])].copy()
 
if len(positive_df) > 0:

    positive_df["Recommended CAPEX USD"] = (

        positive_df["Investment Score"] / positive_df["Investment Score"].sum() * global_budget

    )

else:

    positive_df["Recommended CAPEX USD"] = 0
 
working_df = working_df.merge(

    positive_df[["Zone", "Country", "Recommended CAPEX USD"]],

    on=["Zone", "Country"],

    how="left"

)
 
working_df["Recommended CAPEX USD"] = working_df["Recommended CAPEX USD"].fillna(0)

working_df["Recommended Coolers"] = (

    working_df["Recommended CAPEX USD"] / working_df["Cost per Cooler USD"]

).replace([np.inf, -np.inf], 0).fillna(0).astype(int)
 
# -----------------------------

# Filters

# -----------------------------
 
st.subheader("Portfolio Navigation")
 
col_filter1, col_filter2 = st.columns(2)
 
selected_zone = col_filter1.selectbox(

    "Open by Zone",

    ["Global"] + sorted(working_df["Zone"].unique().tolist())

)
 
if selected_zone == "Global":

    view_df = working_df.copy()

else:

    view_df = working_df[working_df["Zone"] == selected_zone].copy()
 
selected_country = col_filter2.selectbox(

    "Open by Country",

    ["All Countries"] + sorted(view_df["Country"].unique().tolist())

)
 
if selected_country != "All Countries":

    view_df = view_df[view_df["Country"] == selected_country].copy()
 
# -----------------------------

# Executive KPIs

# -----------------------------
 
st.subheader("Executive Summary")
 
k1, k2, k3, k4 = st.columns(4)
 
k1.metric("Markets Analyzed", len(view_df))

k2.metric("Average Score", round(view_df["Investment Score"].mean(), 1))

k3.metric("GO / Selective Markets", len(view_df[view_df["Decision"].isin(["GO - Invest", "Selective Invest"])]))

k4.metric("Recommended CAPEX", f"${view_df['Recommended CAPEX USD'].sum():,.0f}")
 
# -----------------------------

# Country Detail

# -----------------------------
 
if selected_country != "All Countries":

    row = view_df.iloc[0]
 
    st.markdown("### Investment Decision")
 
    css_class = traffic_light_class(row["Decision"])
 
    st.markdown(

        f"""
<div class="{css_class}">

            {row["Decision"]} | Score: {row["Investment Score"]}/100
</div>

        """,

        unsafe_allow_html=True

    )
 
    st.write("### AI Recommendation")

    st.info(row["AI Rationale"])
 
    c1, c2, c3 = st.columns(3)

    c1.metric("Recommended CAPEX", f"${row['Recommended CAPEX USD']:,.0f}")

    c2.metric("Recommended Coolers", f"{row['Recommended Coolers']:,}")

    c3.metric("Payback", f"{row['Payback Months']} months")
 
    st.write("### KPI Inputs Used by the Model")

    st.dataframe(

        row[[

            "Zone",

            "Country",

            "Cooler Coverage %",

            "Market Share %",

            "Zero Sales %",

            "Volume Growth %",

            "Cost per Cooler USD",

            "Expected Volume Uplift %",

            "Historical Impairment %",

            "Payback Months",

            "Annual Volume HL"

        ]].to_frame("Value"),

        use_container_width=True

    )
 
else:

    # -----------------------------

    # Portfolio Ranking

    # -----------------------------
 
    st.subheader("Market Ranking and CAPEX Allocation")
 
    display_df = view_df.sort_values("Investment Score", ascending=False)
 
    st.dataframe(

        display_df[[

            "Zone",

            "Country",

            "Investment Score",

            "Decision",

            "Recommended CAPEX USD",

            "Recommended Coolers",

            "Cooler Coverage %",

            "Market Share %",

            "Zero Sales %",

            "Expected Volume Uplift %",

            "Historical Impairment %",

            "Payback Months"

        ]].style.format({

            "Recommended CAPEX USD": "${:,.0f}",

            "Investment Score": "{:.1f}"

        }),

        use_container_width=True,

        hide_index=True

    )
 
    st.write("### Investment Score by Country")

    st.bar_chart(display_df.set_index("Country")["Investment Score"])
 
    st.write("### Recommended CAPEX Allocation")

    st.bar_chart(display_df.set_index("Country")["Recommended CAPEX USD"])
 
# -----------------------------

# Zone Summary

# -----------------------------
 
st.subheader("Zone-Level View")
 
zone_summary = working_df.groupby("Zone").agg(

    Average_Score=("Investment Score", "mean"),

    Recommended_CAPEX_USD=("Recommended CAPEX USD", "sum"),

    Recommended_Coolers=("Recommended Coolers", "sum"),

    Markets=("Country", "count")

).reset_index()
 
st.dataframe(

    zone_summary.style.format({

        "Average_Score": "{:.1f}",

        "Recommended_CAPEX_USD": "${:,.0f}",

        "Recommended_Coolers": "{:,.0f}"

    }),

    use_container_width=True,

    hide_index=True

)
 
# -----------------------------

# Methodology

# -----------------------------
 
with st.expander("Scoring Methodology"):

    st.write("""

    The tool evaluates each market using three dimensions:
 
    **1. Opportunity — 40%**

    - Cooler coverage gap

    - Market share gap

    - Zero-sales outlets

    - Volume growth
 
    **2. Return — 45%**

    - Expected volume uplift

    - Payback period

    - Cost per cooler
 
    **3. Risk — 25% deduction**

    - Historical impairments

    - Extended payback risk
 
    Decision thresholds:
 
    - **80+ = GO - Invest**

    - **65–79 = Selective Invest**

    - **50–64 = Hold / Reassess**

    - **Below 50 = NO GO**

    """)
 
st.caption("Demo tool using dummy data. Public ABI context used only for framing; financial and market KPIs are illustrative.")
 
