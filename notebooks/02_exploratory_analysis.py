import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load clean data
df = pd.read_csv('data/clean/transactions_clean.csv')
df['Date'] = pd.to_datetime(df['Date'], format='mixed')

print("=== BASIC STATS ===")
print(f"Total transactions: {len(df)}")
print(f"Total revenue: ${df['Total Transaction Amount'].sum():,.2f}")
print(f"Average transaction: ${df['Total Transaction Amount'].mean():,.2f}")
print(f"Median transaction: ${df['Total Transaction Amount'].median():,.2f}")
print(f"Max transaction: ${df['Total Transaction Amount'].max():,.2f}")

print("\n=== REVENUE BY MONTH ===")
monthly = df.groupby(['Year','Month'])['Total Transaction Amount'].agg(['sum','count','mean']).round(2)
monthly.columns = ['Revenue', 'Transactions', 'Avg Transaction']
print(monthly)

print("\n=== REVENUE BY DAY OF WEEK ===")
dow = df.groupby('DayOfWeek')['Total Transaction Amount'].agg(['sum','count','mean']).round(2)
dow.columns = ['Revenue', 'Transactions', 'Avg Transaction']
print(dow)

print("\n=== REVENUE BY HOUR ===")
hourly = df.groupby('Hour')['Total Transaction Amount'].agg(['sum','count']).round(2)
hourly.columns = ['Revenue', 'Transactions']
print(hourly)

print("\n=== PAYMENT TYPE BREAKDOWN ===")
payment = df.groupby('Card Brand')['Total Transaction Amount'].agg(['sum','count','mean']).round(2)
payment.columns = ['Revenue', 'Transactions', 'Avg Transaction']
print(payment.sort_values('Revenue', ascending=False))

# Visualizations - first draft (day of week will have sorting issue)
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Retail Sales Exploratory Analysis', fontsize=16, fontweight='bold')

# Plot 1 - Revenue by month
monthly_plot = df.groupby('Month')['Total Transaction Amount'].sum()
axes[0,0].bar(monthly_plot.index, monthly_plot.values, color='steelblue')
axes[0,0].set_title('Revenue by Month')
axes[0,0].set_xlabel('Month')
axes[0,0].set_ylabel('Revenue ($)')

# Plot 2 - Revenue by day of week (unsorted - will fix next commit)
dow_plot = df.groupby('DayOfWeek')['Total Transaction Amount'].sum()
axes[0,1].bar(dow_plot.index, dow_plot.values, color='darkorange')
axes[0,1].set_title('Revenue by Day of Week')
axes[0,1].set_xlabel('Day')
axes[0,1].set_ylabel('Revenue ($)')
axes[0,1].tick_params(axis='x', rotation=45)

# Plot 3 - Revenue by hour
hourly_plot = df.groupby('Hour')['Total Transaction Amount'].sum()
axes[1,0].bar(hourly_plot.index, hourly_plot.values, color='seagreen')
axes[1,0].set_title('Revenue by Hour of Day')
axes[1,0].set_xlabel('Hour')
axes[1,0].set_ylabel('Revenue ($)')

# Plot 4 - Transaction amount distribution
axes[1,1].hist(df['Total Transaction Amount'], bins=50, color='mediumpurple', edgecolor='white')
axes[1,1].set_title('Transaction Amount Distribution')
axes[1,1].set_xlabel('Amount ($)')
axes[1,1].set_ylabel('Count')

plt.tight_layout()
plt.savefig('data/exploratory_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nChart saved.")