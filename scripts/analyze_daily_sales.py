import pandas as pd
from pathlib import Path

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Locate the daily sales report
csv_file = project_folder / "reports" / "daily_sales_report.csv"

# Read the CSV
df = pd.read_csv(csv_file)

# Display daily sales
print(df)
# Find the day with the highest revenue
highest_day = df.loc[df["daily_revenue"].idxmax()]

# Display the result
print("\nHighest Revenue Day:")
print(highest_day)
# Find the day with the lowest revenue
lowest_day = df.loc[df["daily_revenue"].idxmin()]

# Display the result
print("\nLowest Revenue Day:")
print(lowest_day)
# Calculate average daily revenue
average_revenue = df["daily_revenue"].mean()

# Display the result
print("\nAverage Daily Revenue:", average_revenue)
# Calculate overall revenue
overall_revenue = df["daily_revenue"].sum()

# Display total revenue
print("\nOverall Revenue:", overall_revenue)