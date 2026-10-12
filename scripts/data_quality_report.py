
import pandas as pd
import duckdb
from pathlib import Path

# Step 1: Locate project files
project_folder = Path(__file__).resolve().parent.parent
db_file = project_folder / "sales.duckdb"
output_file = project_folder / "reports" / "data_quality_report.csv"

# Step 2: Read original sales data
con = duckdb.connect(str(db_file), read_only=True)

df = con.execute("""
    SELECT sale_id, customer_id, product_id,
           quantity, price, sale_date
    FROM sales
""").df()

con.close()

# Step 3: Count all records
total_records = len(df)

# Step 4: Apply validation rules
valid_rows = df.dropna()

valid_rows = valid_rows[
    (valid_rows["quantity"] > 0) &
    (valid_rows["price"] > 0)
].copy()

valid_rows = valid_rows.drop_duplicates(
    subset=["sale_id"]
)

# Step 5: Calculate quality metrics
valid_records = len(valid_rows)
invalid_records = total_records - valid_records

quality_score = (
    (valid_records / total_records) * 100
    if total_records > 0 else 0
)

# Step 6: Display report
print("DATA QUALITY REPORT")
print("-------------------")
print("Total Records:", total_records)
print("Valid Records:", valid_records)
print("Invalid Records:", invalid_records)
print("Quality Score:", round(quality_score, 2), "%")

# Step 7: Save report as CSV
report = pd.DataFrame({
    "total_records": [total_records],
    "valid_records": [valid_records],
    "invalid_records": [invalid_records],
    "quality_score": [round(quality_score, 2)]
})

output_file.parent.mkdir(parents=True, exist_ok=True)
report.to_csv(output_file, index=False)

print("Report saved:", output_file)
