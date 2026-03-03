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

battery_voltage = st.slider("Battery Voltage (V)", 10.5, 12.6, 12.4)
temperature = st.slider("Temperature (°C)", 20, 45, 30)
grid_load = st.slider("Grid Demand (%)", 0, 100, 50)

health_score = calculate_battery_score(battery_voltage, temperature)
state = get_state(battery_voltage, health_score, grid_load)
action = choose_action(state)
# ---------- KPI SECTION ----------
col1, col2, col3 = st.columns(3)

col1.metric("Battery Health (%)", round(health_score, 2))
col2.metric("Grid Demand (%)", grid_load)
col3.metric("Voltage (V)", round(battery_voltage, 2))
state_names = {
    0: "High Demand + Good Health",
    1: "High Demand + Poor Health",
    2: "Low Demand + Good Health",
    3: "Low Demand + Poor Health"
}

st.info(f"Current RL State: {state_names[state]}")


if action == 1:
    decision = "ALLOW DISCHARGE"
    decision_color = "green"
else:
    decision = "BLOCK DISCHARGE"
    decision_color = "red"

st.subheader("System Parameters")
st.write(f"🔋 Battery Health Score: {round(health_score,2)}")
st.write(f"⚡ Grid Demand: {grid_load}%")

st.subheader("AI Decision")
st.markdown(f"<h2 style='color:{decision_color};'>{decision}</h2>", unsafe_allow_html=True)