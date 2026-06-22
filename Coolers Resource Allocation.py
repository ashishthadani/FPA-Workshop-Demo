import streamlit as st
import pandas as pd
 
st.set_page_config(page_title="Global Cooler CAPEX Optimizer", layout="wide")
 
st.title("Global Cooler CAPEX Optimizer")
st.caption("AI-powered decision support for cooler CAPEX allocation across ABI Zones and Countries")
 
# -----------------------------
# Dummy Data
# -----------------------------
 
data = [
    ["MAZ", "Mexico", 42, 51, 18, 7, 650, 9, 14, 16, 12000000],
    ["MAZ", "Colombia", 34, 45, 24, 8, 620, 11, 9, 13, 7200000],
    ["MAZ", "Peru", 36, 43, 21, 6, 610, 10, 10, 14, 4600000],
    ["MAZ", "Ecuador", 48, 39, 17, 4, 600, 6, 18, 22, 1800000],
    ["LAS", "Argentina", 55, 47, 14, 3, 700, 5, 20, 24, 5500000],
    ["LAS", "Chile", 50, 44, 12, 2, 720, 4, 12, 21, 2500000],
    ["Europe", "UK", 70, 38, 8, 1, 850, 3, 6, 28, 6000000],
    ["Europe", "Germany", 75, 36, 6, 1, 900, 2, 5, 30, 8000000],
    ["Africa", "South Africa", 30, 41, 26, 9, 580, 12, 15, 12, 4000000],
    ["Africa", "Nigeria", 25, 35, 32, 11, 540, 14, 22, 11, 3500000],
    ["APAC", "China", 60, 22, 20, 5, 780, 7, 16, 20, 9000000],
    ["APAC", "India", 28, 18, 35, 13, 500, 16, 19, 10, 7500000],
    ["North America", "USA", 78, 31, 5, 1, 950, 2, 4, 34, 15000000],
    ["North America", "Canada", 74, 29, 6, 1, 920, 2, 5, 33, 3000000],
]
 
columns = [
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
]
 
df = pd.DataFrame(data, columns=columns)
 
# -----------------------------
# Scoring Model
# -----------------------------
 
def calculate_score(row):
    opportunity_score = (
        (100 - row["Cooler Coverage %"]) * 0.35 +
        (100 - row["Market Share %"]) * 0.20 +
        row["Zero Sales %"] * 0.20 +
        row["Volume Growth %"] * 2.5
    )
 
    return_score = (
        row["Expected Volume Uplift %"] * 4 +
        max(0, 36 - row["Payback Months"]) * 1.5 +
        max(0, 900 - row["Cost per Cooler USD"]) / 20
    )
 
    risk_score = (
        row["Historical Impairment %"] * 1.8 +
        max(0, row["Payback Months"] - 18) * 1.5
    )
 
    final_score = opportunity_score * 0.4 + return_score * 0.4 - risk_score * 0.2
    return max(0, min(100, round(final_score, 1)))
 
 
def get_recommendation(score):
    if score >= 80:
        return "Invest"
    elif score >= 65:
        return "Selective Invest"
    elif score >= 50:
        return "Hold / Reassess"
    else:
        return "Do Not Invest"
 
 
def generate_rationale(row):
    score = row["Investment Score"]
    recommendation = row["Recommendation"]
 
    if recommendation == "Invest":
        return (
            f"{row['Country']} shows a strong cooler investment case driven by low cooler coverage, "
            f"attractive expected volume uplift, and a manageable impairment profile. "
            f"The market should be prioritized for CAPEX allocation."
        )
 
    if recommendation == "Selective Invest":
        return (
            f"{row['Country']} has a positive investment case, but deployment should be selective. "
            f"Coolers should be focused on high-potential channels, regions, or outlets with clear execution discipline."
        )
 
    if recommendation == "Hold / Reassess":
        return (
            f"{row['Country']} shows some opportunity, but current payback, impairment risk, or market maturity "
            f"make the investment less attractive. Additional validation is recommended before scaling."
        )
 
    return (
        f"{row['Country']} does not currently show a strong enough return profile to justify cooler CAPEX. "
        f"The market should focus first on improving execution, reducing risk, or increasing asset productivity."
    )
 
 
df["Investment Score"] = df.apply(calculate_score, axis=1)
df["Recommendation"] = df["Investment Score"].apply(get_recommendation)
df["AI Rationale"] = df.apply(generate_rationale, axis=1)
 
# Suggested budget allocation based on score
df["Suggested Budget Allocation %"] = round(
    df["Investment Score"] / df["Investment Score"].sum() * 100, 1
)
 
# -----------------------------
# Sidebar Filters
# -----------------------------
 
st.sidebar.header("Filters")
 
zone_options = ["Global"] + sorted(df["Zone"].unique().tolist())
selected_zone = st.sidebar.selectbox("Select Zone", zone_options)
 
if selected_zone != "Global":
    filtered_df = df[df["Zone"] == selected_zone]
else:
    filtered_df = df.copy()
 
country_options = ["All Countries"] + sorted(filtered_df["Country"].unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", country_options)
 
if selected_country != "All Countries":
    filtered_df = filtered_df[filtered_df["Country"] == selected_country]
 
# -----------------------------
# Main Dashboard
# -----------------------------
 
st.subheader("Investment Overview")
 
col1, col2, col3, col4 = st.columns(4)
 
col1.metric("Markets Analyzed", len(filtered_df))
col2.metric("Average Score", round(filtered_df["Investment Score"].mean(), 1))
col3.metric("Invest Markets", len(filtered_df[filtered_df["Recommendation"] == "Invest"]))
col4.metric("Avg Payback Months", round(filtered_df["Payback Months"].mean(), 1))
 
st.divider()
 
# -----------------------------
# Global / Zone Ranking
# -----------------------------
 
if selected_country == "All Countries":
    st.subheader("Market Ranking")
 
    ranking = filtered_df.sort_values("Investment Score", ascending=False)
 
    st.dataframe(
        ranking[
            [
                "Zone",
                "Country",
                "Investment Score",
                "Recommendation",
                "Suggested Budget Allocation %",
                "Cooler Coverage %",
                "Market Share %",
                "Zero Sales %",
                "Historical Impairment %",
                "Payback Months",
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
 
    st.subheader("Investment Score by Country")
    chart_df = ranking.set_index("Country")["Investment Score"]
    st.bar_chart(chart_df)
 
    st.subheader("Suggested Budget Allocation")
    budget_df = ranking.set_index("Country")["Suggested Budget Allocation %"]
    st.bar_chart(budget_df)
 
# -----------------------------
# Country Detail View
# -----------------------------
 
else:
    row = filtered_df.iloc[0]
 
    st.subheader(f"{row['Country']} Investment Recommendation")
 
    c1, c2, c3 = st.columns(3)
    c1.metric("Investment Score", row["Investment Score"])
    c2.metric("Recommendation", row["Recommendation"])
    c3.metric("Suggested Budget Allocation", f"{row['Suggested Budget Allocation %']}%")
 
    st.write("### AI Rationale")
    st.success(row["AI Rationale"])
 
    st.write("### Key Market Inputs")
 
    input_table = pd.DataFrame({
        "Metric": [
            "Zone",
            "Cooler Coverage %",
            "Market Share %",
            "Zero Sales %",
            "Volume Growth %",
            "Cost per Cooler USD",
            "Expected Volume Uplift %",
            "Historical Impairment %",
            "Payback Months",
            "Annual Volume HL"
        ],
        "Value": [
            row["Zone"],
            row["Cooler Coverage %"],
            row["Market Share %"],
            row["Zero Sales %"],
            row["Volume Growth %"],
            f"${row['Cost per Cooler USD']}",
            row["Expected Volume Uplift %"],
            row["Historical Impairment %"],
            row["Payback Months"],
            f"{row['Annual Volume HL']:,}"
        ]
    })
 
    st.dataframe(input_table, use_container_width=True, hide_index=True)
 
    st.write("### Strategic Interpretation")
 
    if row["Recommendation"] == "Invest":
        st.write(
            "This market should be prioritized for cooler deployment. "
            "The opportunity is strong, the expected return is attractive, and risk is manageable."
        )
    elif row["Recommendation"] == "Selective Invest":
        st.write(
            "This market should receive targeted investment only in high-potential outlets or regions. "
            "A blanket deployment may dilute returns."
        )
    elif row["Recommendation"] == "Hold / Reassess":
        st.write(
            "This market requires further validation before additional cooler investment. "
            "The team should reassess outlet productivity, risk, and payback assumptions."
        )
    else:
        st.write(
            "This market is not recommended for cooler investment at this stage. "
            "Focus should be on improving asset utilization and reducing impairment risk first."
        )
 
# -----------------------------
# Model Explanation
# -----------------------------
 
with st.expander("View Scoring Methodology"):
    st.write("""
    The model calculates an Investment Score from 0 to 100 using three dimensions:
 
    **1. Opportunity Score — 40%**
    - Cooler coverage gap
    - Market share gap
    - Zero-sales outlets
    - Volume growth
 
    **2. Return Score — 40%**
    - Expected volume uplift
    - Payback period
    - Cost per cooler
 
    **3. Risk Score — 20%**
    - Historical impairments
    - Extended payback risk
 
    Final logic:
 
    **Investment Score = Opportunity + Return - Risk**
    """)
 
st.caption("Dummy data for demo purposes only.")
