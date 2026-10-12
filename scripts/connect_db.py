import duckdb
from pathlib import Path

# Find the project folder
project_folder = Path(__file__).resolve().parent.parent

# Find the DuckDB database file
db_path = project_folder / "sales.duckdb"

# Connect to the existing database
con = duckdb.connect(str(db_path), read_only=True)

## SQL query to join three tables
query = """
SELECT
    c.customer_name,
    p.product_name,
    s.quantity,
    s.price,
    (s.quantity * s.price) AS total_amount
FROM sales AS s
JOIN customers AS c
    ON s.customer_id = c.customer_id
JOIN products AS p
    ON s.product_id = p.product_id
WHERE (s.quantity * s.price) > 300
ORDER BY total_amount DESC
"""

df = con.execute(query).df()
print(df)
# Create the reports folder if needed
reports_folder = project_folder / "reports"
reports_folder.mkdir(parents=True, exist_ok=True)

# Define the output CSV file
output_file = reports_folder / "high_value_sales.csv"

# Export the query result
df.to_csv(output_file, index=False)

# Display confirmation
print("Report saved successfully!")
print("File location:", output_file)
print("Total records exported:", len(df))

# Close database connection
con.close()