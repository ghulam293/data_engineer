
import duckdb
import sys
from pathlib import Path

# Step 1: Define project paths
project_folder = Path(__file__).resolve().parent.parent

db_file = project_folder / "sales.duckdb"

rejected_file = (
    project_folder / "reports" / "rejected_sales.csv"
)

# Step 2: Connect to DuckDB
con = duckdb.connect(str(db_file), read_only=True)

# Step 3: Read sales records
df = con.execute("""
    SELECT
        sale_id,
        customer_id,
        product_id,
        quantity,
        price,
        sale_date
    FROM sales
""").df()

con.close()

print("Total sales records:", len(df))

# Step 4: Check missing values
missing_rows = df.isnull().any(axis=1)

# Check invalid quantities
invalid_quantity = df["quantity"] <= 0

# Check invalid prices
invalid_price = df["price"] <= 0

# Check duplicate sale IDs
duplicate_ids = df.duplicated(
    subset=["sale_id"],
    keep=False
)

# Step 5: Combine validation rules
invalid_rows = (
    missing_rows |
    invalid_quantity |
    invalid_price |
    duplicate_ids
)

# Step 6: Collect rejected records
rejected_df = df[invalid_rows].copy()

# Step 7: Function to explain rejection
def get_rejection_reason(row):

    reasons = []

    # Check missing values
    if row.isnull().any():
        reasons.append("Missing value")

    # Check invalid quantity
    if row["quantity"] <= 0:
        reasons.append("Invalid quantity")

    # Check invalid price
    if row["price"] <= 0:
        reasons.append("Invalid price")

    # Check duplicate sale ID
    if duplicate_ids.loc[row.name]:
        reasons.append("Duplicate sale ID")

    return ", ".join(reasons)


# Step 8: Add rejection_reason column
# Use a loop so empty DataFrames also work
rejected_df["rejection_reason"] = [
    get_rejection_reason(row)
    for _, row in rejected_df.iterrows()
]

# Step 9: Create reports folder
rejected_file.parent.mkdir(
    parents=True,
    exist_ok=True
)

# Step 10: Save rejected records to CSV
rejected_df.to_csv(
    rejected_file,
    index=False
)

# Step 11: Display validation result
if not rejected_df.empty:

    print("\nVALIDATION FAILED!")
    print("Rejected records:", len(rejected_df))

    print("\nRejection details:")
    print(
        rejected_df[
            ["sale_id", "rejection_reason"]
        ]
    )

    print("\nSaved to:", rejected_file)

    # Stop pipeline
    sys.exit(1)

else:

    print("\nVALIDATION PASSED!")
    print("All sales records are valid.")
    print("Rejected records: 0")

    print("\nReport saved to:", rejected_file)

    # Continue pipeline
    sys.exit(0)
