
import pandas as pd
import duckdb
from pathlib import Path

# Step 1: Locate project files
project_folder = Path(__file__).resolve().parent.parent
db_file = project_folder / "sales.duckdb"
output_file = project_folder / "reports" / "validated_sales.csv"

# Step 2: Read data from DuckDB
con = duckdb.connect(str(db_file), read_only=True)

df = con.execute("""
    SELECT sale_id, customer_id, product_id,
           quantity, price, sale_date
    FROM sales
""").df()

con.close()

print("Original records:", len(df))

# Step 3: Remove records with missing values
df = df.dropna()

# Step 4: Keep only positive quantities and prices
df = df[
    (df["quantity"] > 0) &
    (df["price"] > 0)
].copy()

# Step 5: Remove duplicate sale IDs
df = df.drop_duplicates(subset=["sale_id"])

# Step 6: Calculate revenue
df["total_amount"] = df["quantity"] * df["price"]

# Step 7: Save cleaned data
output_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_file, index=False)

print("Cleaned records:", len(df))
print("Cleaned file saved:", output_file)
