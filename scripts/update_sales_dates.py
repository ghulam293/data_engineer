import duckdb
from pathlib import Path

# Find the project folder
project_folder = Path(__file__).resolve().parent.parent

# Find the database
db_path = project_folder / "sales.duckdb"

# Connect to DuckDB
con = duckdb.connect(str(db_path))

# Assign sample dates to existing sales
con.execute("""
UPDATE sales
SET sale_date = CASE sale_id
    WHEN 1 THEN DATE '2026-10-01'
    WHEN 2 THEN DATE '2026-10-01'
    WHEN 3 THEN DATE '2026-10-02'
    WHEN 4 THEN DATE '2026-10-02'
    WHEN 5 THEN DATE '2026-10-03'
END
WHERE sale_id BETWEEN 1 AND 5
""")

# Verify the updated records
df = con.execute("""
SELECT sale_id, product_id, sale_date
FROM sales
ORDER BY sale_id
""").df()

print(df)

# Close the connection
con.close()