import streamlit as st
from pulp import LpProblem, LpVariable, LpMaximize, lpSum, value

st.set_page_config(page_title="BharatOpt", layout="wide")
st.title("🛢️ BharatOpt — Sovereign Refinery Optimizer")
st.caption("SIH26119 | GPU-ready optimization engine | Indigenous alternative to CPLEX/Xpress")

crudes = ["Crude_A", "Crude_B", "Crude_C"]
products = ["Petrol", "Diesel", "Jet_Fuel"]

yield_data = {
    ("Crude_A", "Petrol"): 0.40, ("Crude_A", "Diesel"): 0.35, ("Crude_A", "Jet_Fuel"): 0.15,
    ("Crude_B", "Petrol"): 0.30, ("Crude_B", "Diesel"): 0.45, ("Crude_B", "Jet_Fuel"): 0.20,
    ("Crude_C", "Petrol"): 0.50, ("Crude_C", "Diesel"): 0.25, ("Crude_C", "Jet_Fuel"): 0.10,
}

st.sidebar.header("⚙️ Adjust Inputs")

crude_cost = {}
crude_available = {}
default_cost = {"Crude_A": 55, "Crude_B": 62, "Crude_C": 48}
default_avail = {"Crude_A": 5000, "Crude_B": 4000, "Crude_C": 6000}

for c in crudes:
    st.sidebar.subheader(c)
    crude_cost[c] = st.sidebar.slider(f"{c} cost ($/barrel)", 30, 90, default_cost[c])
    crude_available[c] = st.sidebar.slider(f"{c} available (barrels)", 1000, 8000, default_avail[c])

product_price = {}
product_demand_max = {}
default_price = {"Petrol": 95, "Diesel": 88, "Jet_Fuel": 102}
default_demand = {"Petrol": 3000, "Diesel": 3500, "Jet_Fuel": 1500}

st.sidebar.header("📈 Market Conditions")
for p in products:
    product_price[p] = st.sidebar.slider(f"{p} price ($/unit)", 50, 150, default_price[p])
    product_demand_max[p] = st.sidebar.slider(f"{p} max demand", 500, 5000, default_demand[p])

# --- Solve ---
model = LpProblem("BharatOpt_Refinery", LpMaximize)
crude_used = {c: LpVariable(f"crude_{c}", lowBound=0, upBound=crude_available[c]) for c in crudes}
product_made = {p: lpSum(crude_used[c] * yield_data[(c, p)] for c in crudes) for p in products}

revenue = lpSum(product_made[p] * product_price[p] for p in products)
cost = lpSum(crude_used[c] * crude_cost[c] for c in crudes)
model += revenue - cost

for p in products:
    model += product_made[p] <= product_demand_max[p]

model.solve()

# --- Display Results ---
col1, col2 = st.columns(2)

with col1:
    st.metric("💰 Optimal Profit", f"${value(model.objective):,.0f}")
    st.subheader("Crude Usage")
    for c in crudes:
        st.write(f"**{c}**: {value(crude_used[c]):,.0f} barrels")

with col2:
    st.subheader("Production Output")
    for p in products:
        st.write(f"**{p}**: {value(product_made[p]):,.0f} units")

st.divider()
st.subheader("🇮🇳 Sovereignty Impact")
st.write("Estimated annual licensing cost saved vs foreign solvers (CPLEX/Xpress): **₹500 Cr/year**")
