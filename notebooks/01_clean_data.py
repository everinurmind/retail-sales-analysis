import pandas as pd

# Load raw data
df = pd.read_csv('data/raw/Transaction_03122026.csv')

print("=== RAW DATA ===")
print(f"Rows: {len(df)}")

# Drop sensitive columns
drop_cols = ['Account Number', 'DBA', 'Invoice', 'Auth', 'BRIC',
             'Sold By', 'Customer Name', 'First 6', 'Last 4', 'Routing Number', 'Comment']
df = df.drop(columns=drop_cols)

# Clean amount columns - remove $ and commas
amount_cols = ['Total Transaction Amount', 'Payment Amount', 'Authorized Amount',
               'Tip', '$ Discount', '$ Tax', 'Cash Discounting Amount']
for col in amount_cols:
    df[col] = df[col].replace(r'[\$,]', '', regex=True).astype(float)

# Clean date
df['Date'] = pd.to_datetime(df['Date'], format='mixed')
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['DayOfWeek'] = df['Date'].dt.day_name()
df['Hour'] = df['Date'].dt.hour

# Filter only completed sales
df = df[df['Transaction Type'].isin(['Contactless EMV', 'EMV', 'Swiped', 'Keyed'])]

print(f"Clean rows: {len(df)}")
print(f"Columns kept: {list(df.columns)}")
print(f"\nDate range: {df['Date'].min()} to {df['Date'].max()}")
print(f"\nPayment types:\n{df['Payment Type'].value_counts()}")
print(f"\nCard brands:\n{df['Card Brand'].value_counts()}")

# Save clean data
df.to_csv('data/clean/transactions_clean.csv', index=False)
print("\nSaved clean data to data/clean/transactions_clean.csv")