import duckdb
from pathlib import Path

# Find the existing database
project_folder = Path(__file__).resolve().parent.parent
db_path = project_folder / "sales.duckdb"

# Connect to the database
con = duckdb.connect(str(db_path))

# Add a date column
con.execute("""
ALTER TABLE sales
ADD COLUMN IF NOT EXISTS sale_date DATE
""")

print("Date column added successfully!")

# Display the table structure
print(con.execute("DESCRIBE sales").df())

# Close the connection LAST
con.close()