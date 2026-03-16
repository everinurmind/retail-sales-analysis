import pandas as pd
import sqlite3

# Load clean data into SQLite
df = pd.read_csv('data/clean/transactions_clean.csv')
df['Date'] = pd.to_datetime(df['Date'], format='mixed')
conn = sqlite3.connect(':memory:')
df.to_sql('transactions', conn, index=False)

print("=== 1. REVENUE SUMMARY ===")
print(pd.read_sql("""
    SELECT
        COUNT(*) AS total_transactions,
        ROUND(SUM("Total Transaction Amount"), 2) AS total_revenue,
        ROUND(AVG("Total Transaction Amount"), 2) AS avg_transaction,
        ROUND(MIN("Total Transaction Amount"), 2) AS min_transaction,
        ROUND(MAX("Total Transaction Amount"), 2) AS max_transaction
    FROM transactions
    WHERE "Payment Type" = 'Credit Sale'
""", conn))

print("\n=== 2. REVENUE BY DAY OF WEEK ===")
print(pd.read_sql("""
    SELECT
        DayOfWeek,
        COUNT(*) AS transactions,
        ROUND(SUM("Total Transaction Amount"), 2) AS revenue,
        ROUND(AVG("Total Transaction Amount"), 2) AS avg_transaction
    FROM transactions
    WHERE "Payment Type" = 'Credit Sale'
    GROUP BY DayOfWeek
    ORDER BY revenue DESC
""", conn))

print("\n=== 3. PEAK HOURS BY REVENUE ===")
print(pd.read_sql("""
    SELECT
        Hour,
        COUNT(*) AS transactions,
        ROUND(SUM("Total Transaction Amount"), 2) AS revenue,
        ROUND(AVG("Total Transaction Amount"), 2) AS avg_transaction
    FROM transactions
    WHERE "Payment Type" = 'Credit Sale'
    GROUP BY Hour
    ORDER BY revenue DESC
    LIMIT 10
""", conn))

print("\n=== 4. CARD BRAND ANALYSIS ===")
print(pd.read_sql("""
    SELECT
        "Card Brand",
        COUNT(*) AS transactions,
        ROUND(SUM("Total Transaction Amount"), 2) AS total_revenue,
        ROUND(AVG("Total Transaction Amount"), 2) AS avg_transaction,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) AS pct_of_transactions
    FROM transactions
    WHERE "Payment Type" = 'Credit Sale'
    GROUP BY "Card Brand"
    ORDER BY total_revenue DESC
""", conn))

print("\n=== 5. WEEKLY PERFORMANCE ===")
print(pd.read_sql("""
    SELECT
        strftime('%Y-W%W', Date) AS week,
        COUNT(*) AS transactions,
        ROUND(SUM("Total Transaction Amount"), 2) AS revenue,
        ROUND(AVG("Total Transaction Amount"), 2) AS avg_transaction
    FROM transactions
    WHERE "Payment Type" = 'Credit Sale'
    GROUP BY strftime('%Y-W%W', Date)
    ORDER BY week
""", conn))

print("\n=== 6. BEST SINGLE DAYS ===")
print(pd.read_sql("""
    SELECT
        DATE(Date) AS date,
                CASE strftime('%w', Date)
            WHEN '0' THEN 'Sunday'
            WHEN '1' THEN 'Monday'
            WHEN '2' THEN 'Tuesday'
            WHEN '3' THEN 'Wednesday'
            WHEN '4' THEN 'Thursday'
            WHEN '5' THEN 'Friday'
            WHEN '6' THEN 'Saturday'
        END AS day_of_week,
        COUNT(*) AS transactions,
        ROUND(SUM("Total Transaction Amount"), 2) AS revenue
    FROM transactions
    WHERE "Payment Type" = 'Credit Sale'
    GROUP BY DATE(Date)
    ORDER BY revenue DESC
    LIMIT 10
""", conn))

print("\n=== 7. MONTHLY COMPARISON ===")
print(pd.read_sql("""
    SELECT
        strftime('%Y-%m', Date) AS month,
        COUNT(*) AS transactions,
        ROUND(SUM("Total Transaction Amount"), 2) AS revenue,
        ROUND(AVG("Total Transaction Amount"), 2) AS avg_transaction,
        COUNT(DISTINCT DATE(Date)) AS active_days,
        ROUND(SUM("Total Transaction Amount") / COUNT(DISTINCT DATE(Date)), 2) AS revenue_per_day
    FROM transactions
    WHERE "Payment Type" = 'Credit Sale'
    GROUP BY strftime('%Y-%m', Date)
    ORDER BY month
""", conn))

conn.close()
print("\nSQL analysis complete.")