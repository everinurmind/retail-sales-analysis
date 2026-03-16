import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# Load data
df = pd.read_csv('data/clean/transactions_clean.csv')
df['Date'] = pd.to_datetime(df['Date'], format='mixed')
df = df[df['Payment Type'] == 'Credit Sale']

conn = sqlite3.connect(':memory:')
df.to_sql('transactions', conn, index=False)

# ── 1. WEEK-OVER-WEEK TREND
weekly = pd.read_sql("""
    SELECT
        strftime('%Y-W%W', Date) AS week,
        ROUND(SUM("Total Transaction Amount"), 2) AS revenue,
        COUNT(*) AS transactions,
        ROUND(AVG("Total Transaction Amount"), 2) AS avg_transaction
    FROM transactions
    GROUP BY strftime('%Y-W%W', Date)
    ORDER BY week
""", conn)

weekly['revenue_growth'] = weekly['revenue'].pct_change() * 100
print("=== WEEK-OVER-WEEK REVENUE GROWTH ===")
print(weekly[['week','revenue','revenue_growth']].round(1))

# ── 2. END OF MONTH EFFECT
df['day_of_month'] = df['Date'].dt.day
df['month_period'] = pd.cut(df['day_of_month'],
    bins=[0,10,20,31],
    labels=['Start (1-10)', 'Mid (11-20)', 'End (21-31)'])

period_analysis = df.groupby('month_period', observed=True)['Total Transaction Amount'].agg(
    ['mean','count','sum']).round(2)
period_analysis.columns = ['avg_transaction','transactions','revenue']
print("\n=== PAYCHECK EFFECT - REVENUE BY MONTH PERIOD ===")
print(period_analysis)

# ── 3. MASTERCARD VS VISA DEEP DIVE
card_analysis = df.groupby('Card Brand')['Total Transaction Amount'].agg(
    ['mean','median','count','sum']).round(2)
card_analysis.columns = ['avg','median','count','total']
print("\n=== CARD BRAND DEEP DIVE ===")
print(card_analysis)

# ── 4. FRIDAY VS OTHER DAYS
df['is_friday'] = df['DayOfWeek'] == 'Friday'
friday_comparison = df.groupby('is_friday')['Total Transaction Amount'].agg(
    ['mean','median','count','sum']).round(2)
friday_comparison.columns = ['avg','median','count','total']
friday_comparison.index = ['Other Days', 'Friday']
print("\n=== FRIDAY VS OTHER DAYS ===")
print(friday_comparison)

# ── 5. OPENING HOUR VS PEAK HOUR
hour_analysis = df.groupby('Hour')['Total Transaction Amount'].agg(['mean','count','sum']).round(2)
hour_analysis.columns = ['avg_transaction','transactions','revenue']
print("\n=== 5PM (OPENING) VS 10PM (PEAK VOLUME) ===")
print(hour_analysis.loc[hour_analysis.index.isin([17, 22])])

# ── VISUALIZATIONS
sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Retail Sales Deep Dive - Business Insights', fontsize=16, fontweight='bold')

# Plot 1 - Weekly revenue trend
axes[0,0].plot(weekly['week'], weekly['revenue'], marker='o', color='steelblue', linewidth=2)
axes[0,0].set_title('Weekly Revenue Trend')
axes[0,0].set_xlabel('Week')
axes[0,0].set_ylabel('Revenue ($)')
axes[0,0].tick_params(axis='x', rotation=45)
for i, row in weekly.iterrows():
    axes[0,0].annotate(f"${row['revenue']:,.0f}", (row['week'], row['revenue']),
                       textcoords="offset points", xytext=(0,8), ha='center', fontsize=7)

# Plot 2 - Paycheck effect
period_revenue = period_analysis['revenue']
axes[0,1].bar(period_revenue.index, period_revenue.values, color=['#ff9999','#66b3ff','#99ff99'])
axes[0,1].set_title('Revenue by Month Period (Paycheck Effect)')
axes[0,1].set_xlabel('Period')
axes[0,1].set_ylabel('Total Revenue ($)')
for i, val in enumerate(period_revenue.values):
    axes[0,1].text(i, val + 200, f'${val:,.0f}', ha='center', fontsize=9)

# Plot 3 - Avg transaction by card brand
card_avg = card_analysis['avg'].sort_values(ascending=False)
axes[1,0].bar(card_avg.index, card_avg.values, color='darkorange')
axes[1,0].set_title('Avg Transaction by Card Brand')
axes[1,0].set_xlabel('Card Brand')
axes[1,0].set_ylabel('Avg Transaction ($)')
for i, val in enumerate(card_avg.values):
    axes[1,0].text(i, val + 0.3, f'${val:.2f}', ha='center', fontsize=9)

# Plot 4 - Friday vs other days
friday_avg = friday_comparison['avg']
colors = ['#66b3ff', '#ff9999']
axes[1,1].bar(friday_avg.index, friday_avg.values, color=colors)
axes[1,1].set_title('Avg Transaction: Friday vs Other Days')
axes[1,1].set_xlabel('Day Type')
axes[1,1].set_ylabel('Avg Transaction ($)')
for i, val in enumerate(friday_avg.values):
    axes[1,1].text(i, val + 0.2, f'${val:.2f}', ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('data/insights_analysis.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nInsights chart saved.")

conn.close()