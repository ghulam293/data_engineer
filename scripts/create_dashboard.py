
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Step 1: Locate project folder
project_folder = Path(__file__).resolve().parent.parent

# Step 2: Read daily sales CSV
csv_file = project_folder / "reports" / "daily_sales_report.csv"
df = pd.read_csv(csv_file)

# Step 3: Convert dates and sort
df["sale_date"] = pd.to_datetime(df["sale_date"])
df = df.sort_values("sale_date")

# Step 4: Calculate KPIs
total_revenue = df["daily_revenue"].sum()
average_revenue = df["daily_revenue"].mean()
total_sales = df["total_sales"].sum()
best_day = df.loc[df["daily_revenue"].idxmax(), "sale_date"]

# Display KPIs
print("Total Revenue:", total_revenue)
print("Average Daily Revenue:", round(average_revenue, 2))
print("Total Sales:", total_sales)
print("Best Sales Day:", best_day.date())

# Step 5: Create dashboard with two charts
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# First chart: Daily revenue
axes[0].bar(
    df["sale_date"].dt.strftime("%Y-%m-%d"),
    df["daily_revenue"],
    color="skyblue"
)

axes[0].set_title("Daily Sales Revenue")
axes[0].set_xlabel("Date")
axes[0].set_ylabel("Revenue")
axes[0].tick_params(axis="x", rotation=30)

# Second chart: Revenue trend
axes[1].plot(
    df["sale_date"],
    df["daily_revenue"],
    marker="o",
    color="blue",
    linewidth=2
)

axes[1].set_title("Sales Revenue Trend")
axes[1].set_xlabel("Date")
axes[1].set_ylabel("Revenue")
axes[1].tick_params(axis="x", rotation=30)

# Step 6: Dashboard title
fig.suptitle(
    "Sales Performance Dashboard",
    fontsize=16
)

# Step 7: KPI summary
kpi_text = (
    f"Total Revenue: {total_revenue:,.2f}   |   "
    f"Average Daily Revenue: {average_revenue:,.2f}   |   "
    f"Total Sales: {total_sales}   |   "
    f"Best Day: {best_day:%Y-%m-%d}"
)

fig.text(
    0.5,
    0.91,
    kpi_text,
    ha="center",
    fontsize=10
)

# Step 8: Adjust layout
plt.tight_layout(rect=[0, 0, 1, 0.84])

# Step 9: Save dashboard
output_file = project_folder / "reports" / "sales_dashboard.png"

plt.savefig(output_file, dpi=300)

print("Dashboard saved successfully!")
print("File:", output_file)

# Step 10: Display dashboard
plt.show()
