import duckdb
from pathlib import Path

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Locate the database
db_path = project_folder / "sales.duckdb"

# Connect to DuckDB
con = duckdb.connect(str(db_path), read_only=True)

# Calculate revenue for each product
query = """
SELECT
    p.product_name,
    SUM(s.quantity * s.price) AS total_revenue
FROM sales AS s
JOIN products AS p
    ON s.product_id = p.product_id
GROUP BY p.product_name
ORDER BY total_revenue DESC
"""

# Execute SQL and convert results to Pandas
df = con.execute(query).df()

# Display the summary
print(df)
total_revenue = df["total_revenue"].sum()
print("Overall Revenue:", total_revenue)

# Prepare the output folder
reports_folder = project_folder / "reports"
reports_folder.mkdir(parents=True, exist_ok=True)

# Save the report
output_file = reports_folder / "sales_summary.csv"
df.to_csv(output_file, index=False)

print("Sales summary generated successfully!")

# Close the connection
con.close()