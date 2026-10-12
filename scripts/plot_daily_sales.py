import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Locate project folder
project_folder = Path(__file__).resolve().parent.parent

# Locate CSV report
csv_file = project_folder / "reports" / "daily_sales_report.csv"

# Read daily sales data
df = pd.read_csv(csv_file)

# Create a bar chart
# Create a bar chart with custom colors
bars = plt.bar(
    df["sale_date"],
    df["daily_revenue"],
    color="skyblue"
)

# Add revenue values above each bar
plt.bar_label(bars, fmt="%.2f", padding=3)

# Add chart title and labels
plt.title("Daily Sales Revenue")
plt.xlabel("Sale Date")
plt.ylabel("Revenue (PKR)")

# Make the chart easier to read
plt.grid(axis="y", linestyle="--", alpha=0.3)
plt.tight_layout()

# Save the chart as an image
output_file = project_folder / "reports" / "daily_sales_chart.png"
plt.savefig(output_file, dpi=300)

print("Chart saved successfully!")
print("File location:", output_file)

# Display the chart
plt.show()