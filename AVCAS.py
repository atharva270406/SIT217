# -----------------------------------------------
# Patient Monitoring Simulation (Colab Version)
# -----------------------------------------------

import random
import time
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- Configuration ----------------
THRESHOLDS = {
    "hr": {"low": 40, "high": 130},      # heart rate (bpm)
    "sbp": {"low": 70, "high": 200},     # systolic blood pressure (mmHg)
    "spo2": {"low": 85, "high": 100},    # oxygen saturation (%)
    "temp": {"low": 34.0, "high": 41.0}  # temperature (°C)
}

NUM_PATIENTS = 3      # number of patients
ITERATIONS = 30       # number of samples
INTERVAL = 1.0        # seconds between samples (simulation speed)


# ---------------- Simulation Functions ----------------
def simulate_vitals():
    """Generate random vital signs for one patient."""
    return {
        "hr": random.randint(30, 160),
        "sbp": random.randint(60, 210),
        "spo2": random.randint(70, 100),
        "temp": round(random.uniform(33.0, 42.0), 1)
    }

def check_alerts(vitals):
    """Check if vitals cross thresholds. Return list of alerts."""
    alerts = []
    for key, value in vitals.items():
        if value < THRESHOLDS[key]["low"] or value > THRESHOLDS[key]["high"]:
            alerts.append(f"{key.upper()} out of range ({value})")
    return alerts


# ---------------- Data Collection ----------------
records = []

print("=== Running Patient Monitoring Simulation ===")
for i in range(ITERATIONS):
    for pid in range(1, NUM_PATIENTS + 1):
        vitals = simulate_vitals()
        alerts = check_alerts(vitals)

        # save record
        record = {
            "iteration": i,
            "patient_id": pid,
            **vitals,
            "alert": "; ".join(alerts) if alerts else "Stable"
        }
        records.append(record)

        # print to console
        print(f"Iter {i+1} | Patient P{pid} | HR={vitals['hr']} | SBP={vitals['sbp']} | "
              f"SpO2={vitals['spo2']} | Temp={vitals['temp']} -> {record['alert']}")

    time.sleep(INTERVAL)

# ---------------- Save to CSV ----------------
df = pd.DataFrame(records)
df.to_csv("patient_vitals_log.csv", index=False)
print("\nSimulation complete. Data saved to patient_vitals_log.csv")

# ---------------- Plot Results ----------------
plt.figure(figsize=(12,6))

for pid in range(1, NUM_PATIENTS+1):
    subset = df[df["patient_id"] == pid]
    plt.plot(subset["iteration"], subset["hr"], label=f"P{pid} HR")

plt.axhline(THRESHOLDS["hr"]["low"], color="red", linestyle="--", alpha=0.7)
plt.axhline(THRESHOLDS["hr"]["high"], color="red", linestyle="--", alpha=0.7)
plt.title("Heart Rate Trends Across Patients")
plt.xlabel("Iteration")
plt.ylabel("Heart Rate (bpm)")
plt.legend()
plt.show()

# Show last few log entries
df.tail(10)
