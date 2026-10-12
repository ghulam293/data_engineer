CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER REFERENCES customers(customer_id),
    product_id INTEGER REFERENCES products(product_id),
    quantity INTEGER,
    price DECIMAL(10,2)
);
-- Add the column if it does not exist
ALTER TABLE sales
ADD COLUMN IF NOT EXISTS sale_date DATE;

-- Assign sample dates
UPDATE sales
SET sale_date = CASE sale_id
    WHEN 1 THEN DATE '2026-10-01'
    WHEN 2 THEN DATE '2026-10-01'
    WHEN 3 THEN DATE '2026-10-02'
    WHEN 4 THEN DATE '2026-10-02'
    WHEN 5 THEN DATE '2026-10-03'
END
WHERE sale_id BETWEEN 1 AND 5;

-- Check the results
SELECT
    sale_date,
    COUNT(*) AS total_sales,
    SUM(quantity * price) AS daily_revenue
FROM sales
WHERE sale_date IS NOT NULL
GROUP BY sale_date
ORDER BY sale_date;
