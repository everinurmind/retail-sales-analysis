# Retail Sales & Customer Behavior Analysis

**Tools:** SQL · Python · pandas · Matplotlib · Seaborn  
**Author:** Nurbol Sultanov | [LinkedIn](https://www.linkedin.com/in/everinurmind/) | [GitHub](https://github.com/everinurmind)

---

## Project Overview

Analysis of 4,800+ real retail transactions from a Los Angeles smoke shop (Dec 2025 – Mar 2026). Built to surface actionable business insights around revenue trends, customer behavior, and operational performance.

**Business Questions Answered:**
- What days and hours drive the most revenue?
- Which payment methods correlate with higher spend?
- Is there a paycheck effect in customer purchasing behavior?
- Which weeks had anomalous performance and why?

---

## Dataset

- **Records:** 4,805 transactions (4,714 completed sales)
- **Period:** December 2025 – March 2026
- **Source:** PayAnywhere POS system (anonymized)
- **Fields:** date, transaction type, amount, payment type, card brand

---

## Key Findings

| Insight | Detail |
|---|---|
| Total revenue | $127,373 across 4,714 transactions |
| Avg transaction | $27.02 |
| Top day | Friday ($31.34 avg, $22,848 total) |
| Peak hour | 5pm (highest avg transaction $30.74) |
| Top card brand | Mastercard ($34.07 avg vs $25.57 Visa) |
| Paycheck effect | End-of-month avg $29.35 vs mid-month $25.33 |
| Anomalous week | W04 2026 — $15,710 (2+ std above mean) |
| Revenue per day | ~$1,500/day in Jan-Mar 2026 |

---

## Business Recommendations

1. **Staff up on Fridays** — highest revenue and avg transaction consistently
2. **Focus upsell efforts at 5pm** — customers spend 29% more at opening hour
3. **Target Mastercard/Discover customers** — 33% higher avg spend than Visa
4. **Investigate W04 anomaly** — single week drove $15,710, identify what caused it and replicate
5. **End-of-month promotions** — customers already spend more, capitalize with bundles

---

## Project Structure
```
├── data/
│   ├── raw/                          # Original POS export (not tracked)
│   ├── clean/transactions_clean.csv  # Anonymized clean dataset
│   ├── exploratory_analysis.png      # EDA visualizations
│   └── insights_analysis.png         # Deep dive charts
├── notebooks/
│   ├── 01_clean_data.py              # Data cleaning & anonymization
│   ├── 02_exploratory_analysis.py    # EDA + visualizations
│   ├── 03_sql_analysis.py            # SQL queries via SQLite
│   └── 04_insights.py               # Deep dive analysis + outlier detection
└── README.md
```

---

## How to Run
```bash
# 1. Install dependencies
pip install pandas numpy matplotlib seaborn

# 2. Clean raw data
python notebooks/01_clean_data.py

# 3. Exploratory analysis
python notebooks/02_exploratory_analysis.py

# 4. SQL analysis
python notebooks/03_sql_analysis.py

# 5. Deep dive insights
python notebooks/04_insights.py
```