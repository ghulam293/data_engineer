
import pandas as pd
from pathlib import Path
from datetime import datetime
import subprocess
import sys

# Step 1: Find project folder
project_folder = Path(__file__).resolve().parent.parent

# Step 2: File paths
summary_file = project_folder / "reports" / "pipeline_summary.csv"
performance_file = project_folder / "reports" / "pipeline_performance.csv"

# Step 3: Read pipeline summary
df = pd.read_csv(summary_file)

# Step 4: Calculate performance metrics
total_scripts = len(df)

successful_scripts = len(df[df["status"] == "SUCCESS"])
failed_scripts = len(df[df["status"] == "FAILED"])

total_script_duration = round(df["duration_seconds"].sum(), 2)

# Step 40: Check pipeline health

slow_threshold = 5.0

# Count scripts taking more than 5 seconds
slow_scripts = len(
    df[df["duration_seconds"] > slow_threshold]
)

# Determine health status
if failed_scripts > 0:
    pipeline_health = "FAILED"

elif slow_scripts > 0:
    pipeline_health = "WARNING"

else:
    pipeline_health = "HEALTHY"

print("\nPipeline Health:", pipeline_health)
print("Slow Scripts:", slow_scripts)


# Step 5: Find slowest script
if not df.empty:
    slowest_script = df.loc[
        df["duration_seconds"].idxmax(), "script"
    ]
else:
    slowest_script = "None"

# Step 6: Create performance report

# Step 6: Create performance report
performance = pd.DataFrame({
    "metric": [
        "Total Scripts",
        "Successful Scripts",
        "Failed Scripts",
        "Slow Scripts",
        "Pipeline Health",
        "Slowest Script",
        "Combined Script Duration (seconds)"
    ],
    "value": [
        total_scripts,
        successful_scripts,
        failed_scripts,
        slow_scripts,
        pipeline_health,
        slowest_script,
        total_script_duration
    ]
})

# Step 7: Save report
performance.to_csv(performance_file, index=False)

# Step 41: Save pipeline health history

history_file = project_folder / "reports" / "pipeline_health_history.csv"

# Create a record for the current run
history = pd.DataFrame([{
    "run_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "pipeline_health": pipeline_health,
    "total_scripts": total_scripts,
    "successful_scripts": successful_scripts,
    "failed_scripts": failed_scripts,
    "slow_scripts": slow_scripts,
    "total_duration_seconds": total_script_duration
}])

# Check whether the history file already exists
file_exists = history_file.exists()

# Append the new record without deleting previous records
history.to_csv(
    history_file,
    mode="a",
    header=not file_exists,
    index=False
)

# Step 44: Automatically generate health trend chart

chart_script = project_folder / "scripts" / "pipeline_health_trend.py"

print("\nGenerating pipeline health trend chart...")

subprocess.run(
    [sys.executable, str(chart_script)],
    check=True
)

print("Pipeline health trend chart generated successfully!")

# Step 46: Automatically generate monitoring dashboard

dashboard_script = (
    project_folder / "scripts" / "pipeline_monitoring_dashboard.py"
)

print("\nGenerating pipeline monitoring dashboard...")

subprocess.run(
    [sys.executable, str(dashboard_script)],
    check=True
)

print("Pipeline monitoring dashboard generated successfully!")

# Step 46: Automatically generate monitoring dashboard

dashboard_script = (
    project_folder / "scripts" / "pipeline_monitoring_dashboard.py"
)

print("\nGenerating pipeline monitoring dashboard...")

subprocess.run(
    [sys.executable, str(dashboard_script)],
    check=True
)

print("Pipeline monitoring dashboard generated successfully!")

# Step 46: Automatically generate monitoring dashboard

dashboard_script = (
    project_folder / "scripts" / "pipeline_monitoring_dashboard.py"
)

print("\nGenerating pipeline monitoring dashboard...")

subprocess.run(
    [sys.executable, str(dashboard_script)],
    check=True
)

print("Pipeline monitoring dashboard generated successfully!")

print("Pipeline health history saved to:", history_file)

print("\nPIPELINE PERFORMANCE REPORT")
print(performance.to_string(index=False))

print("\nReport saved to:", performance_file)
