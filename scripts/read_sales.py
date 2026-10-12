
import pandas as pd
from pathlib import Path

# Step 1: Find the main project folder
project_folder = Path(__file__).resolve().parent.parent

# Step 2: Locate the sales CSV file
csv_file = project_folder / "reports" / "sales_report.csv"

# Step 3: Read CSV into a DataFrame
df = pd.read_csv(csv_file)

print("Original Sales Data:")
print(df)

# Step 4: Sort products by revenue (highest first)
df = df.sort_values(
    by="total_revenue",
    ascending=False
).reset_index(drop=True)

print("\nSorted Sales Data:")
print(df)

# Step 5: Display top 3 products
print("\nTop 3 Products:")
print(df.head(3))

# Step 6: Calculate total revenue
total_revenue = df["total_revenue"].sum()
print("\nTotal Revenue:", total_revenue)

# Step 7: Calculate average revenue
average_revenue = df["total_revenue"].mean()
print("Average Revenue:", average_revenue)

# Step 8: Find highest and lowest revenue
highest = df["total_revenue"].max()
lowest = df["total_revenue"].min()

print("\nHighest Revenue:", highest)
print("Lowest Revenue:", lowest)

# Step 9: Find highest revenue product
highest_index = df["total_revenue"].idxmax()
highest_product = df.loc[highest_index, "product_name"]

print("Highest Revenue Product:", highest_product)

# Step 10: Find lowest revenue product
lowest_index = df["total_revenue"].idxmin()
lowest_product = df.loc[lowest_index, "product_name"]

print("Lowest Revenue Product:", lowest_product)

# Step 11: Filter high-value products
high_sales = df[df["total_revenue"] > 500]

print("\nProducts with Revenue > 500:")
print(high_sales)

# Step 12: Filter low-value products
low_sales = df[df["total_revenue"] < 500]

print("\nProducts with Revenue < 500:")
print(low_sales)

# Step 13: Create a copy for duplicate testing
test_df = df.copy()

# Add a duplicate of the first row
test_df = pd.concat(
    [test_df, test_df.iloc[[0]]],
    ignore_index=True
)

# Step 14: Count duplicate rows
duplicate_count = test_df.duplicated().sum()

print("\nDuplicate Rows:", duplicate_count)

# Step 15: Remove duplicate rows
clean_df = test_df.drop_duplicates().reset_index(drop=True)

print("\nCleaned Sales Data:")
print(clean_df)

# Step 16: Save cleaned data to CSV
reports_folder = project_folder / "reports"
reports_folder.mkdir(parents=True, exist_ok=True)

output_file = reports_folder / "cleaned_sales.csv"

clean_df.to_csv(output_file, index=False)

print("\nCleaned sales saved successfully!")
print("File location:", output_file)
print("Total clean records:", len(clean_df))
