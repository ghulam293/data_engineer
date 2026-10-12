
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Step 1: Find project folder
project_folder = Path(__file__).resolve().parent.parent

# Step 2: File paths
history_file = project_folder / "reports" / "pipeline_health_history.csv"
dashboard_file = project_folder / "reports" / "pipeline_monitoring_dashboard.png"

# Step 3: Read health history
df = pd.read_csv(history_file)

# Step 4: Calculate monitoring metrics
total_runs = len(df)

healthy_runs = len(df[df["pipeline_health"] == "HEALTHY"])
warning_runs = len(df[df["pipeline_health"] == "WARNING"])
failed_runs = len(df[df["pipeline_health"] == "FAILED"])

healthy_rate = round(
    (healthy_runs / total_runs) * 100, 2
) if total_runs > 0 else 0

# Step 5: Get latest recorded status
if not df.empty:
    df["run_time"] = pd.to_datetime(df["run_time"])
    latest_status = df.sort_values("run_time").iloc[-1]["pipeline_health"]
else:
    latest_status = "NO DATA"

# Step 6: Create dashboard
fig, ax = plt.subplots(figsize=(10, 6))

ax.axis("off")

dashboard_text = (
    "PIPELINE MONITORING DASHBOARD\n\n"
    f"Total Runs: {total_runs}\n"
    f"Healthy Runs: {healthy_runs}\n"
    f"Warning Runs: {warning_runs}\n"
    f"Failed Runs: {failed_runs}\n"
    f"Healthy Rate: {healthy_rate}%\n"
    f"Latest Status: {latest_status}"
)

ax.text(
    0.1, 0.85,
    dashboard_text,
    fontsize=17,
    verticalalignment="top",
    linespacing=1.7
)

# Step 7: Save dashboard
plt.tight_layout()
plt.savefig(dashboard_file)
plt.close()

print("Monitoring dashboard saved to:", dashboard_file)
