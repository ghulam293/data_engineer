import duckdb
from pathlib import Path

# Find project folder and database
project_folder = Path(__file__).resolve().parent.parent
db_path = project_folder / "sales.duckdb"

# Connect to database
con = duckdb.connect(str(db_path), read_only=True)

# Calculate revenue for each date
query = """
SELECT
    sale_date,
    COUNT(*) AS total_sales,
    SUM(quantity * price) AS daily_revenue
FROM sales
WHERE sale_date IS NOT NULL
GROUP BY sale_date
ORDER BY sale_date
"""

# Run query and convert to Pandas
df = con.execute(query).df()

# Display the daily report
print(df)
# Locate the reports folder
reports_folder = project_folder / "reports"

# Create the folder if it does not exist
reports_folder.mkdir(parents=True, exist_ok=True)

# Set the output filename
output_file = reports_folder / "daily_sales_report.csv"

# Save the DataFrame to CSV
df.to_csv(output_file, index=False)

# Display confirmation
print("Daily sales report saved successfully!")
print("File:", output_file)
print("Total days exported:", len(df))
# Calculate total revenue across all dates
overall_revenue = df["daily_revenue"].sum()

print("Overall Revenue sum  :", overall_revenue)
# Close connection
con.close()