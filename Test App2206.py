import streamlit as st
import pandas as pd

st.set_page_config(page_title="ScenarioPilot", layout="wide")

st.title("ScenarioPilot")
st.write("A simple overhead scenario planner for FP&A teams.")

st.sidebar.header("Base Budget")
people = st.sidebar.number_input("People Costs (£m)", value=10.0)
travel = st.sidebar.number_input("Travel & Expenses (£m)", value=2.0)
consulting = st.sidebar.number_input("Consulting (£m)", value=3.0)
marketing = st.sidebar.number_input("Marketing Support (£m)", value=2.0)
other = st.sidebar.number_input("Other Overheads (£m)", value=1.0)

st.sidebar.header("Scenario Assumptions")
salary_inflation = st.sidebar.slider("Salary Inflation %", 0, 15, 5)
travel_saving = st.sidebar.slider("T&E Saving %", 0, 50, 20)
consulting_saving = st.sidebar.slider("Consulting Saving %", 0, 50, 15)
marketing_saving = st.sidebar.slider("Marketing Saving %", 0, 50, 5)
other_saving = st.sidebar.slider("Other Saving %", 0, 50, 5)

budget = {
    "People Costs": people,
    "Travel & Expenses": travel,
    "Consulting": consulting,
    "Marketing Support": marketing,
    "Other Overheads": other
}

scenario = {
    "People Costs": people * (1 + salary_inflation / 100),
    "Travel & Expenses": travel * (1 - travel_saving / 100),
    "Consulting": consulting * (1 - consulting_saving / 100),
    "Marketing Support": marketing * (1 - marketing_saving / 100),
    "Other Overheads": other * (1 - other_saving / 100)
}

df = pd.DataFrame({
    "Line Item": budget.keys(),
    "Budget £m": budget.values(),
    "Scenario £m": scenario.values()
})

df["Variance £m"] = df["Scenario £m"] - df["Budget £m"]

budget_total = df["Budget £m"].sum()
scenario_total = df["Scenario £m"].sum()
ebitda_impact = budget_total - scenario_total

col1, col2, col3 = st.columns(3)

col1.metric("Budget Overheads", f"£{budget_total:.1f}m")
col2.metric("Scenario Overheads", f"£{scenario_total:.1f}m")
col3.metric("EBITDA Impact", f"£{ebitda_impact:.1f}m")

st.subheader("Scenario Results")
st.dataframe(df)

st.subheader("Overheads by Line Item")
chart_df = df.set_index("Line Item")[["Budget £m", "Scenario £m"]]
st.bar_chart(chart_df)

st.subheader("Finance Commentary")

biggest_saving = df.sort_values("Variance £m").iloc[0]["Line Item"]

if ebitda_impact > 0:
    st.success(
        f"This scenario improves EBITDA by £{ebitda_impact:.1f}m. "
        f"The biggest saving comes from {biggest_saving}. "
        "People costs should still be reviewed carefully, as salary inflation offsets part of the benefit."
    )
elif ebitda_impact < 0:
    st.warning(
        f"This scenario reduces EBITDA by £{abs(ebitda_impact):.1f}m. "
        "The cost pressure outweighs the savings actions, so further mitigation may be needed."
    )
else:
    st.info("This scenario is neutral to EBITDA versus the base budget.")
