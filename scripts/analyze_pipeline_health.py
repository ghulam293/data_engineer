
import pandas as pd
from pathlib import Path

# Step 1: Find project folder
project_folder = Path(__file__).resolve().parent.parent

# Step 2: Set file paths
history_file = project_folder / "reports" / "pipeline_health_history.csv"
analysis_file = project_folder / "reports" / "pipeline_health_analysis.csv"

# Step 3: Read health history
df = pd.read_csv(history_file)

# Step 4: Count pipeline runs
total_runs = len(df)

healthy_runs = len(
    df[df["pipeline_health"] == "HEALTHY"]
)

warning_runs = len(
    df[df["pipeline_health"] == "WARNING"]
)

failed_runs = len(
    df[df["pipeline_health"] == "FAILED"]
)

# Step 5: Calculate healthy rate
if total_runs > 0:
    healthy_rate = round(
        (healthy_runs / total_runs) * 100, 2
    )
else:
    healthy_rate = 0

# Step 6: Create analysis report
analysis = pd.DataFrame({
    "metric": [
        "Total Runs",
        "Healthy Runs",
        "Warning Runs",
        "Failed Runs",
        "Healthy Rate (%)"
    ],
    "value": [
        total_runs,
        healthy_runs,
        warning_runs,
        failed_runs,
        healthy_rate
    ]
})

# Step 7: Save analysis
analysis.to_csv(analysis_file, index=False)

print("\nPIPELINE HEALTH ANALYSIS")
print(analysis.to_string(index=False))

print("\nReport saved to:", analysis_file)
