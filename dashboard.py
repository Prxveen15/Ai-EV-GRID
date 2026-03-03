import streamlit as st
import numpy as np
import random
import time

# Load trained Q-table
Q = np.loadtxt("Q_learning_Training/q_table.txt")

def calculate_battery_score(voltage, temperature):
    V_min = 10.5
    V_max = 12.6
    T_ideal = 25
    T_max = 45

    V_norm = (voltage - V_min) / (V_max - V_min)
    T_norm = 1 - ((temperature - T_ideal) / (T_max - T_ideal))

    V_norm = max(0, min(1, V_norm))
    T_norm = max(0, min(1, T_norm))

    return (0.6 * V_norm + 0.4 * T_norm) * 100

def get_state(voltage, health_score, grid_load):
    if grid_load > 80 and health_score > 70:
        return 0
    elif grid_load > 80 and health_score <= 70:
        return 1
    elif grid_load <= 80 and health_score > 70:
        return 2
    else:
        return 3

def choose_action(state):
    return np.argmax(Q[state])

st.title("⚡ AI-Enabled EV Grid Stabilization Dashboard")
mode = st.selectbox("Operating Mode", ["Normal Simulation", "Peak Demand Mode"])
st.subheader("EV Fleet Status")

num_evs = 3
ev_data = []

for i in range(num_evs):
    voltage = random.uniform(11.5, 12.6)
    temperature = random.uniform(25, 40)
    health = calculate_battery_score(voltage, temperature)

    ev_data.append({
        "id": f"EV{i+1}",
        "voltage": voltage,
        "temperature": temperature,
        "health": health
    })
    st.subheader("🚗 EV Fleet Overview")

cols = st.columns(len(ev_data))

for i, ev in enumerate(ev_data):
    with cols[i]:
        st.metric(
            label=ev["id"],
            value=f"{round(ev['health'],2)} %",
            delta=f"{round(ev['voltage'],2)} V"
        )
        import pandas as pd

ev_df = pd.DataFrame(ev_data)

st.subheader("📊 EV Health Comparison")
st.bar_chart(ev_df.set_index("id")["health"])
     # Select EV with highest health above 70%
healthy_evs = [ev for ev in ev_data if ev["health"] > 70]

if healthy_evs:
    selected_ev = max(healthy_evs, key=lambda x: x["health"])
else:
    selected_ev = None
if mode == "Peak Demand Mode":
    grid_load = 95
else:
    grid_load = st.slider("Grid Demand (%)", 0, 100, 50)
    # ---------------------------
# STEP 5: Select Best EV
# ---------------------------

healthy_evs = [ev for ev in ev_data if ev["health"] > 70]

if healthy_evs:
    selected_ev = max(healthy_evs, key=lambda x: x["health"])

    health_score = selected_ev["health"]
    battery_voltage = selected_ev["voltage"]

    state = get_state(battery_voltage, health_score, grid_load)
    action = choose_action(state)

    st.markdown(f"### 🔌 Selected EV for Discharge: **{selected_ev['id']}**")

else:
    st.error("No EV available with sufficient health")
    action = 0
    # ---------------------------
# STEP 6: AI Decision Display
# ---------------------------

if action == 1:
    st.success("✅ ALLOW DISCHARGE")
else:
    st.error("⛔ BLOCK DISCHARGE")
# Select healthiest EV above 70%
healthy_evs = [ev for ev in ev_data if ev["health"] > 70]

if healthy_evs:
    selected_ev = max(healthy_evs, key=lambda x: x["health"])

    health_score = selected_ev["health"]
    battery_voltage = selected_ev["voltage"]

    state = get_state(battery_voltage, health_score, grid_load)
    action = choose_action(state)

    st.success(f"Selected EV: {selected_ev['id']}")

else:
    st.error("No EV with sufficient health available")
    action = 0

if action == 1:
    decision = "ALLOW DISCHARGE"
    decision_color = "green"
else:
    decision = "BLOCK DISCHARGE"
    decision_color = "red"
    # ---------- KPI SECTION ----------

state_names = {
    0: "High Demand + Good Health",
    1: "High Demand + Poor Health",
    2: "Low Demand + Good Health",
    3: "Low Demand + Poor Health"
}

if healthy_evs:
    st.info(f"Current RL State: {state_names[state]}")
col1, col2, col3 = st.columns(3)

if healthy_evs:

    col1, col2, col3 = st.columns(3)

    col1.metric("Battery Health (%)", round(health_score, 2))
    col2.metric("Grid Demand (%)", grid_load)
    col3.metric("Voltage (V)", round(battery_voltage, 2))

else:
    st.warning("⚠ No EV selected — KPI unavailable")
st.subheader("System Parameters")
st.write(f"⚡ Grid Demand: {grid_load}%")

st.subheader("AI Decision")

if action == 1:
    st.success("✅ ALLOW DISCHARGE")
else:
    st.error("⛔ BLOCK DISCHARGE")
    # -------- Voltage Trend Graph --------
if "voltage_history" not in st.session_state:
    st.session_state.voltage_history = []

st.session_state.voltage_history.append(battery_voltage)

st.subheader("Battery Voltage Trend")
st.line_chart(st.session_state.voltage_history)