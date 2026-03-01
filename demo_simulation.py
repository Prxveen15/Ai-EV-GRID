# ==========================================
# EV GRID RL DEMO SIMULATION
# ==========================================

import numpy as np
import random
import time
import matplotlib.pyplot as plt

# ==========================================
# LOAD TRAINED Q TABLE
# ==========================================

Q = np.loadtxt("Q_learning_Training/q_table.txt")

# ==========================================
# BATTERY SCORE CALCULATION
# ==========================================

def calculate_battery_score(voltage, temperature):

    V_min = 10.5
    V_max = 12.6
    T_ideal = 25
    T_max = 45

    V_norm = (voltage - V_min) / (V_max - V_min)
    T_norm = 1 - ((temperature - T_ideal) / (T_max - T_ideal))

    V_norm = max(0, min(1, V_norm))
    T_norm = max(0, min(1, T_norm))

    score = 0.6 * V_norm + 0.4 * T_norm

    return score * 100

# ==========================================
# STATE MAPPING
# ==========================================

def get_state(voltage, health_score, grid_load):

    if grid_load > 80 and health_score > 70:
        return 0
    elif grid_load > 80 and health_score <= 70:
        return 1
    elif grid_load <= 80 and health_score > 70:
        return 2
    else:
        return 3

# ==========================================
# ACTION SELECTION
# ==========================================

def choose_action(state):
    return np.argmax(Q[state])

# ==========================================
# SIMULATION START
# ==========================================

print("\n🔵 Starting AI-Based EV Grid Simulation...\n")

battery_voltage = 12.4
battery_levels = []

for step in range(20):

    temperature = random.uniform(20, 45)
    grid_load = random.randint(40, 100)

    health_score = calculate_battery_score(battery_voltage, temperature)
    state = get_state(battery_voltage, health_score, grid_load)
    action = choose_action(state)

    if action == 1:
        decision = "ALLOW discharge"
        battery_voltage -= 0.2
    else:
        decision = "BLOCK discharge"
        battery_voltage += 0.05

    battery_voltage = max(10.5, min(12.6, battery_voltage))
    battery_levels.append(battery_voltage)

    print(f"Step {step+1}")
    print(f"Voltage: {round(battery_voltage,2)} V")
    print(f"Temperature: {round(temperature,2)} °C")
    print(f"Battery Health Score: {round(health_score,2)}")
    print(f"Grid Load: {grid_load}%")
    print(f"Decision: {decision}")
    print("-" * 40)

    time.sleep(1)

# ==========================================
# PLOT RESULTS
# ==========================================

plt.figure()
plt.plot(battery_levels)
plt.title("Battery Voltage Over Time (RL Controlled)")
plt.xlabel("Time Step")
plt.ylabel("Voltage (V)")
plt.show()