
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Step 1: Find project folder
project_folder = Path(__file__).resolve().parent.parent

# Step 2: File paths
history_file = project_folder / "reports" / "pipeline_health_history.csv"
chart_file = project_folder / "reports" / "pipeline_health_trend.png"

# Step 3: Read pipeline history
df = pd.read_csv(history_file)

# Step 4: Convert date column
df["run_time"] = pd.to_datetime(df["run_time"])

# Step 5: Convert health status into numbers
health_scores = {
    "HEALTHY": 2,
    "WARNING": 1,
    "FAILED": 0
}

df["health_score"] = df["pipeline_health"].map(health_scores)

# Step 6: Sort runs by date and time
df = df.sort_values("run_time")

# Step 7: Create line chart
plt.figure(figsize=(10, 5))

plt.plot(
    df["run_time"],
    df["health_score"],
    marker="o"
)

plt.title("Pipeline Health Trend")
plt.xlabel("Pipeline Run Time")
plt.ylabel("Health Status")

# Show health labels instead of numbers
plt.yticks(
    [0, 1, 2],
    ["FAILED", "WARNING", "HEALTHY"]
)

plt.ylim(-0.2, 2.2)
plt.xticks(rotation=45)
plt.grid(True)

# Step 8: Save chart
plt.tight_layout()
plt.savefig(chart_file)
plt.close()

print("Pipeline health trend chart saved to:", chart_file)
