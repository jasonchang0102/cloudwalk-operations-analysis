import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

# Load data
print("Loading data...")
df = pd.read_excel('/mnt/user-data/uploads/--_Data--_Operations_Intelligence_Analyst.xlsx')

print(f"Dataset loaded: {df.shape[0]:,} rows, {df.shape[1]} columns")
print(f"Date range: {df['day'].min()} to {df['day'].max()}")
print("\n" + "="*80 + "\n")

# ============================================================================
# DATA PREPARATION
# ============================================================================

# Calculate TPV and Average Ticket
df['tpv'] = df['amount_transacted']
df['avg_ticket'] = df['amount_transacted'] / df['quantity_transactions']

# Add date features
df['day_of_week'] = df['day'].dt.day_name()
df['week'] = df['day'].dt.isocalendar().week
df['month'] = df['day'].dt.month
df['is_weekend'] = df['day'].dt.dayofweek.isin([5, 6])

# ============================================================================
# 1. KEY PERFORMANCE INDICATORS (KPIs)
# ============================================================================

print("EXECUTIVE SUMMARY - KEY METRICS")
print("="*80)

total_tpv = df['tpv'].sum()
total_transactions = df['quantity_transactions'].sum()
total_merchants = df['quantity_of_merchants'].sum()
overall_avg_ticket = total_tpv / total_transactions
avg_daily_tpv = df.groupby('day')['tpv'].sum().mean()

print(f"\n📊 OVERALL PERFORMANCE (Jan 1 - Mar 31, 2025)")
print(f"   Total Payment Volume (TPV): R$ {total_tpv:,.2f}")
print(f"   Total Transactions: {total_transactions:,}")
print(f"   Total Merchants: {total_merchants:,}")
print(f"   Overall Average Ticket: R$ {overall_avg_ticket:,.2f}")
print(f"   Average Daily TPV: R$ {avg_daily_tpv:,.2f}")

print("\n" + "="*80)
print("TPV BY ENTITY (PF vs PJ)")
print("="*80)
entity_tpv = df.groupby('entity').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum',
    'quantity_of_merchants': 'sum'
}).reset_index()
entity_tpv['avg_ticket'] = entity_tpv['tpv'] / entity_tpv['quantity_transactions']
entity_tpv['pct_tpv'] = (entity_tpv['tpv'] / entity_tpv['tpv'].sum() * 100)

for _, row in entity_tpv.iterrows():
    print(f"\n{row['entity']}:")
    print(f"   TPV: R$ {row['tpv']:,.2f} ({row['pct_tpv']:.1f}%)")
    print(f"   Transactions: {row['quantity_transactions']:,}")
    print(f"   Merchants: {row['quantity_of_merchants']:,}")
    print(f"   Avg Ticket: R$ {row['avg_ticket']:,.2f}")

print("\n" + "="*80)
print("TPV BY PRODUCT")
print("="*80)
product_tpv = df.groupby('product').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum',
    'quantity_of_merchants': 'sum'
}).reset_index().sort_values('tpv', ascending=False)
product_tpv['avg_ticket'] = product_tpv['tpv'] / product_tpv['quantity_transactions']
product_tpv['pct_tpv'] = (product_tpv['tpv'] / product_tpv['tpv'].sum() * 100)

for _, row in product_tpv.iterrows():
    print(f"\n{row['product'].upper()}:")
    print(f"   TPV: R$ {row['tpv']:,.2f} ({row['pct_tpv']:.1f}%)")
    print(f"   Transactions: {row['quantity_transactions']:,}")
    print(f"   Avg Ticket: R$ {row['avg_ticket']:,.2f}")

print("\n" + "="*80)
print("TPV BY PAYMENT METHOD")
print("="*80)
payment_tpv = df.groupby('payment_method').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum'
}).reset_index().sort_values('tpv', ascending=False)
payment_tpv['avg_ticket'] = payment_tpv['tpv'] / payment_tpv['quantity_transactions']
payment_tpv['pct_tpv'] = (payment_tpv['tpv'] / payment_tpv['tpv'].sum() * 100)

for _, row in payment_tpv.iterrows():
    print(f"\n{row['payment_method'].upper()}:")
    print(f"   TPV: R$ {row['tpv']:,.2f} ({row['pct_tpv']:.1f}%)")
    print(f"   Transactions: {row['quantity_transactions']:,}")
    print(f"   Avg Ticket: R$ {row['avg_ticket']:,.2f}")

print("\n" + "="*80)
print("INSTALLMENTS ANALYSIS")
print("="*80)
installments_analysis = df.groupby('installments').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum'
}).reset_index().sort_values('installments')
installments_analysis['avg_ticket'] = installments_analysis['tpv'] / installments_analysis['quantity_transactions']
installments_analysis['pct_tpv'] = (installments_analysis['tpv'] / installments_analysis['tpv'].sum() * 100)

print("\nTop 5 installment options by TPV:")
for _, row in installments_analysis.nlargest(5, 'tpv').iterrows():
    print(f"   {int(row['installments'])}x: R$ {row['tpv']:,.2f} ({row['pct_tpv']:.1f}%) - Avg Ticket: R$ {row['avg_ticket']:,.2f}")

print("\n" + "="*80)
print("PRICE TIER ANALYSIS")
print("="*80)
tier_analysis = df.groupby('price_tier').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum',
    'quantity_of_merchants': 'sum'
}).reset_index().sort_values('tpv', ascending=False)
tier_analysis['avg_ticket'] = tier_analysis['tpv'] / tier_analysis['quantity_transactions']
tier_analysis['pct_tpv'] = (tier_analysis['tpv'] / tier_analysis['tpv'].sum() * 100)

for _, row in tier_analysis.iterrows():
    print(f"\n{row['price_tier'].upper()}:")
    print(f"   TPV: R$ {row['tpv']:,.2f} ({row['pct_tpv']:.1f}%)")
    print(f"   Transactions: {row['quantity_transactions']:,}")
    print(f"   Merchants: {row['quantity_of_merchants']:,}")
    print(f"   Avg Ticket: R$ {row['avg_ticket']:,.2f}")

print("\n" + "="*80)
print("ANTICIPATION METHOD BY ENTITY")
print("="*80)
anticipation_by_entity = df.groupby(['entity', 'anticipation_method']).agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum'
}).reset_index()

for entity in ['PF', 'PJ']:
    print(f"\n{entity}:")
    entity_data = anticipation_by_entity[anticipation_by_entity['entity'] == entity].sort_values('tpv', ascending=False)
    entity_total = entity_data['tpv'].sum()
    for _, row in entity_data.iterrows():
        pct = (row['tpv'] / entity_total * 100)
        print(f"   {row['anticipation_method']}: R$ {row['tpv']:,.2f} ({pct:.1f}%)")

print("\n" + "="*80)
print("WEEKDAY ANALYSIS")
print("="*80)
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_analysis = df.groupby('day_of_week').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum'
}).reset_index()
weekday_analysis['avg_ticket'] = weekday_analysis['tpv'] / weekday_analysis['quantity_transactions']
weekday_analysis['day_of_week'] = pd.Categorical(weekday_analysis['day_of_week'], categories=day_order, ordered=True)
weekday_analysis = weekday_analysis.sort_values('day_of_week')

print("\nTPV by Day of Week:")
for _, row in weekday_analysis.iterrows():
    print(f"   {row['day_of_week']}: R$ {row['tpv']:,.2f}")

weekend_tpv = df[df['is_weekend']]['tpv'].sum()
weekday_tpv = df[~df['is_weekend']]['tpv'].sum()
print(f"\nWeekend vs Weekday:")
print(f"   Weekday TPV: R$ {weekday_tpv:,.2f} ({weekday_tpv/(weekend_tpv+weekday_tpv)*100:.1f}%)")
print(f"   Weekend TPV: R$ {weekend_tpv:,.2f} ({weekend_tpv/(weekend_tpv+weekday_tpv)*100:.1f}%)")

print("\n" + "="*80)
print("Analysis complete! Now generating visualizations...")
print("="*80 + "\n")
