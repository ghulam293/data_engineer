import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Find the project folder
project_folder = Path(__file__).resolve().parent.parent

# Locate the CSV file
csv_file = project_folder / "reports" / "daily_sales_report.csv"

# Read CSV data
df = pd.read_csv(csv_file)

# Convert dates to datetime
df["sale_date"] = pd.to_datetime(df["sale_date"])

# Sort dates in ascending order
df = df.sort_values("sale_date")

# Create line chart
plt.plot(
    df["sale_date"],
    df["daily_revenue"],
    marker="o",
    color="blue",
    linewidth=2
)

# Add chart title and labels
plt.title("Daily Sales Revenue Trend")
plt.xlabel("Sale Date")
plt.ylabel("Revenue (PKR)")

# Improve chart appearance
plt.grid(True, linestyle="--", alpha=0.3)
plt.xticks(rotation=30)
plt.tight_layout()

# Save chart as PNG
output_file = project_folder / "reports" / "sales_trend.png"
plt.savefig(output_file, dpi=300)

print("Sales trend chart saved successfully!")
print("File:", output_file)

# Display chart
plt.show()