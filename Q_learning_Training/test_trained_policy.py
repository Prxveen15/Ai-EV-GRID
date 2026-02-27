# ==========================================
# TEST TRAINED Q-TABLE POLICY
# ==========================================

import numpy as np

# Load trained Q-table
Q = np.loadtxt("q_table.txt")

print("Loaded Q-Table:\n")
print(Q)

print("\nBest Action Per State:\n")

for state in range(len(Q)):

    best_action = int(np.argmax(Q[state]))

    if best_action == 0:
        decision = "BLOCK discharge"
    else:
        decision = "ALLOW discharge"

    print(f"State {state} → {decision}")