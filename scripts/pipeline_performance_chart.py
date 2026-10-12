
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Step 1: Find project folder
project_folder = Path(__file__).resolve().parent.parent

# Step 2: Set file paths
summary_file = project_folder / "reports" / "pipeline_summary.csv"
chart_file = project_folder / "reports" / "pipeline_performance.png"

# Step 3: Read pipeline summary
df = pd.read_csv(summary_file)

# Step 4: Create a bar chart
plt.figure(figsize=(10, 5))

plt.bar(
    df["script"],
    df["duration_seconds"]
)

# Step 5: Add labels
plt.title("Pipeline Script Execution Times")
plt.xlabel("Python Scripts")
plt.ylabel("Execution Time (seconds)")

# Rotate script names for readability
plt.xticks(rotation=45, ha="right")

# Step 6: Save the chart
plt.tight_layout()
plt.savefig(chart_file)

plt.close()

print("Performance chart saved to:", chart_file)
