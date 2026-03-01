# ==========================================
# Q-LEARNING TRAINING FOR EV GRID SYSTEM
# ==========================================

import numpy as np
import random

# ----------------------------
# STATE DEFINITIONS
# ----------------------------
# 0 = Low Voltage + Good Health
# 1 = Low Voltage + Poor Health
# 2 = Normal Voltage + Good Health
# 3 = Normal Voltage + Poor Health

states = 4
actions = 2   # 0 = BLOCK, 1 = ALLOW

Q = np.zeros((states, actions))

# ----------------------------
# PARAMETERS
# ----------------------------
alpha = 0.1
gamma = 0.9
epsilon = 0.2
episodes = 3000

# ----------------------------
# REWARD FUNCTION
# ----------------------------
def get_reward(state, action):

    # State 0: High demand + Good health
    if state == 0:
        if action == 1:   # Allow
            return 20     # Very good
        else:
            return -5     # Bad (grid needed help)

    # State 1: High demand + Poor health
    if state == 1:
        if action == 0:   # Block
            return 10
        else:
            return -20

    # State 2: Low demand + Good health
    if state == 2:
        if action == 0:
            return 10
        else:
            return -5

    # State 3: Low demand + Poor health
    if state == 3:
        if action == 0:
            return 15
        else:
            return -25


# ----------------------------
# TRAINING LOOP
# ----------------------------
for episode in range(episodes):

    state = random.randint(0, states - 1)

    # Epsilon-greedy policy
    if random.uniform(0, 1) < epsilon:
        action = random.randint(0, actions - 1)
    else:
        action = np.argmax(Q[state])

    reward = get_reward(state, action)

    next_state = random.randint(0, states - 1)

    # Q-learning update
    Q[state][action] = Q[state][action] + alpha * (
        reward + gamma * np.max(Q[next_state]) - Q[state][action]
    )

print("\nTraining Completed!\n")
print("Final Q-Table:\n")
print(Q)

# ----------------------------
# SAVE Q-TABLE TO FILE
# ----------------------------
np.savetxt("q_table.txt", Q, fmt="%.4f")

print("\nQ-table saved to q_table.txt")