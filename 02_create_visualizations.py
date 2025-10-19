import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Load data
df = pd.read_excel('/mnt/user-data/uploads/--_Data--_Operations_Intelligence_Analyst.xlsx')
df['tpv'] = df['amount_transacted']
df['avg_ticket'] = df['amount_transacted'] / df['quantity_transactions']
df['day_of_week'] = df['day'].dt.day_name()
df['week'] = df['day'].dt.isocalendar().week
df['month'] = df['day'].dt.month
df['is_weekend'] = df['day'].dt.dayofweek.isin([5, 6])

# Create output directory
import os
os.makedirs('/mnt/user-data/outputs/visualizations', exist_ok=True)

print("Generating visualizations...\n")

# ============================================================================
# 1. TPV BY ENTITY
# ============================================================================
print("1. Creating TPV by Entity visualizations...")

entity_tpv = df.groupby('entity').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum'
}).reset_index()
entity_tpv['avg_ticket'] = entity_tpv['tpv'] / entity_tpv['quantity_transactions']

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Total Payment Volume by Entity', 'Average Ticket by Entity'),
    specs=[[{'type': 'bar'}, {'type': 'bar'}]]
)

fig.add_trace(
    go.Bar(x=entity_tpv['entity'], y=entity_tpv['tpv']/1e9, 
           text=[f'R$ {v/1e9:.2f}B' for v in entity_tpv['tpv']],
           textposition='auto',
           marker_color=['#2E86AB', '#A23B72'],
           name='TPV'),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=entity_tpv['entity'], y=entity_tpv['avg_ticket'],
           text=[f'R$ {v:.2f}' for v in entity_tpv['avg_ticket']],
           textposition='auto',
           marker_color=['#2E86AB', '#A23B72'],
           name='Avg Ticket'),
    row=1, col=2
)

fig.update_xaxes(title_text="Entity", row=1, col=1)
fig.update_xaxes(title_text="Entity", row=1, col=2)
fig.update_yaxes(title_text="TPV (Billions R$)", row=1, col=1)
fig.update_yaxes(title_text="Average Ticket (R$)", row=1, col=2)
fig.update_layout(height=500, showlegend=False, title_text="Entity Performance Analysis")
fig.write_html('/mnt/user-data/outputs/visualizations/01_tpv_by_entity.html')
print("   ✓ Saved: 01_tpv_by_entity.html")

# ============================================================================
# 2. TPV BY PRODUCT
# ============================================================================
print("2. Creating TPV by Product visualizations...")

product_tpv = df.groupby('product').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum'
}).reset_index().sort_values('tpv', ascending=False)
product_tpv['avg_ticket'] = product_tpv['tpv'] / product_tpv['quantity_transactions']

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('TPV by Product', 'Average Ticket by Product', 
                    'Transaction Count by Product', 'TPV Distribution'),
    specs=[[{'type': 'bar'}, {'type': 'bar'}],
           [{'type': 'bar'}, {'type': 'pie'}]]
)

# TPV by Product
fig.add_trace(
    go.Bar(x=product_tpv['product'], y=product_tpv['tpv']/1e9,
           text=[f'R$ {v/1e9:.2f}B' for v in product_tpv['tpv']],
           textposition='auto',
           marker_color='#F18F01',
           name='TPV'),
    row=1, col=1
)

# Avg Ticket by Product
fig.add_trace(
    go.Bar(x=product_tpv['product'], y=product_tpv['avg_ticket'],
           text=[f'R$ {v:.2f}' for v in product_tpv['avg_ticket']],
           textposition='auto',
           marker_color='#C73E1D',
           name='Avg Ticket'),
    row=1, col=2
)

# Transaction Count
fig.add_trace(
    go.Bar(x=product_tpv['product'], y=product_tpv['quantity_transactions']/1e6,
           text=[f'{v/1e6:.1f}M' for v in product_tpv['quantity_transactions']],
           textposition='auto',
           marker_color='#6A994E',
           name='Transactions'),
    row=2, col=1
)

# Pie chart
fig.add_trace(
    go.Pie(labels=product_tpv['product'], values=product_tpv['tpv'],
           textinfo='label+percent',
           marker=dict(colors=['#F18F01', '#C73E1D', '#6A994E', '#2E86AB', '#A23B72'])),
    row=2, col=2
)

fig.update_xaxes(title_text="Product", row=1, col=1)
fig.update_xaxes(title_text="Product", row=1, col=2)
fig.update_xaxes(title_text="Product", row=2, col=1)
fig.update_yaxes(title_text="TPV (Billions R$)", row=1, col=1)
fig.update_yaxes(title_text="Avg Ticket (R$)", row=1, col=2)
fig.update_yaxes(title_text="Transactions (Millions)", row=2, col=1)
fig.update_layout(height=800, showlegend=False, title_text="Product Performance Analysis")
fig.write_html('/mnt/user-data/outputs/visualizations/02_tpv_by_product.html')
print("   ✓ Saved: 02_tpv_by_product.html")

# ============================================================================
# 3. TPV BY PAYMENT METHOD
# ============================================================================
print("3. Creating Payment Method visualizations...")

payment_tpv = df.groupby('payment_method').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum'
}).reset_index().sort_values('tpv', ascending=False)
payment_tpv['avg_ticket'] = payment_tpv['tpv'] / payment_tpv['quantity_transactions']

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('TPV by Payment Method', 'Average Ticket by Payment Method'),
    specs=[[{'type': 'bar'}, {'type': 'bar'}]]
)

fig.add_trace(
    go.Bar(x=payment_tpv['payment_method'], y=payment_tpv['tpv']/1e9,
           text=[f'R$ {v/1e9:.2f}B' for v in payment_tpv['tpv']],
           textposition='auto',
           marker_color=['#2E86AB', '#F18F01', '#6A994E'],
           name='TPV'),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=payment_tpv['payment_method'], y=payment_tpv['avg_ticket'],
           text=[f'R$ {v:.2f}' for v in payment_tpv['avg_ticket']],
           textposition='auto',
           marker_color=['#2E86AB', '#F18F01', '#6A994E'],
           name='Avg Ticket'),
    row=1, col=2
)

fig.update_xaxes(title_text="Payment Method", row=1, col=1)
fig.update_xaxes(title_text="Payment Method", row=1, col=2)
fig.update_yaxes(title_text="TPV (Billions R$)", row=1, col=1)
fig.update_yaxes(title_text="Average Ticket (R$)", row=1, col=2)
fig.update_layout(height=500, showlegend=False, title_text="Payment Method Analysis")
fig.write_html('/mnt/user-data/outputs/visualizations/03_payment_method.html')
print("   ✓ Saved: 03_payment_method.html")

# ============================================================================
# 4. INSTALLMENTS ANALYSIS
# ============================================================================
print("4. Creating Installments Analysis...")

installments_analysis = df.groupby('installments').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum'
}).reset_index()
installments_analysis['avg_ticket'] = installments_analysis['tpv'] / installments_analysis['quantity_transactions']

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('TPV by Installments', 'Transaction Count by Installments',
                    'Average Ticket by Installments', 'TPV Distribution by Installments'),
    specs=[[{'type': 'bar'}, {'type': 'bar'}],
           [{'type': 'bar'}, {'type': 'bar'}]]
)

fig.add_trace(
    go.Bar(x=installments_analysis['installments'], y=installments_analysis['tpv']/1e9,
           marker_color='#2E86AB',
           name='TPV'),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=installments_analysis['installments'], y=installments_analysis['quantity_transactions']/1e6,
           marker_color='#F18F01',
           name='Transactions'),
    row=1, col=2
)

fig.add_trace(
    go.Bar(x=installments_analysis['installments'], y=installments_analysis['avg_ticket'],
           marker_color='#6A994E',
           name='Avg Ticket'),
    row=2, col=1
)

# Cumulative percentage
installments_sorted = installments_analysis.sort_values('tpv', ascending=False)
installments_sorted['cumulative_pct'] = (installments_sorted['tpv'].cumsum() / installments_sorted['tpv'].sum() * 100)
fig.add_trace(
    go.Bar(x=installments_sorted['installments'], y=installments_sorted['cumulative_pct'],
           marker_color='#C73E1D',
           name='Cumulative %'),
    row=2, col=2
)

fig.update_xaxes(title_text="Installments", row=1, col=1)
fig.update_xaxes(title_text="Installments", row=1, col=2)
fig.update_xaxes(title_text="Installments", row=2, col=1)
fig.update_xaxes(title_text="Installments (sorted by TPV)", row=2, col=2)
fig.update_yaxes(title_text="TPV (Billions R$)", row=1, col=1)
fig.update_yaxes(title_text="Transactions (Millions)", row=1, col=2)
fig.update_yaxes(title_text="Avg Ticket (R$)", row=2, col=1)
fig.update_yaxes(title_text="Cumulative % of TPV", row=2, col=2)
fig.update_layout(height=800, showlegend=False, title_text="Installments Deep Dive")
fig.write_html('/mnt/user-data/outputs/visualizations/04_installments_analysis.html')
print("   ✓ Saved: 04_installments_analysis.html")

# ============================================================================
# 5. PRICE TIER ANALYSIS
# ============================================================================
print("5. Creating Price Tier Analysis...")

tier_analysis = df.groupby('price_tier').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum',
    'quantity_of_merchants': 'sum'
}).reset_index().sort_values('tpv', ascending=False)
tier_analysis['avg_ticket'] = tier_analysis['tpv'] / tier_analysis['quantity_transactions']

fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=('TPV by Price Tier', 'Average Ticket by Price Tier',
                    'Transaction Count by Price Tier', 'Merchant Count by Price Tier'),
    specs=[[{'type': 'bar'}, {'type': 'bar'}],
           [{'type': 'bar'}, {'type': 'bar'}]]
)

fig.add_trace(
    go.Bar(x=tier_analysis['price_tier'], y=tier_analysis['tpv']/1e9,
           text=[f'R$ {v/1e9:.2f}B' for v in tier_analysis['tpv']],
           textposition='auto',
           marker_color='#2E86AB'),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=tier_analysis['price_tier'], y=tier_analysis['avg_ticket'],
           text=[f'R$ {v:.2f}' for v in tier_analysis['avg_ticket']],
           textposition='auto',
           marker_color='#F18F01'),
    row=1, col=2
)

fig.add_trace(
    go.Bar(x=tier_analysis['price_tier'], y=tier_analysis['quantity_transactions']/1e6,
           text=[f'{v/1e6:.1f}M' for v in tier_analysis['quantity_transactions']],
           textposition='auto',
           marker_color='#6A994E'),
    row=2, col=1
)

fig.add_trace(
    go.Bar(x=tier_analysis['price_tier'], y=tier_analysis['quantity_of_merchants']/1e6,
           text=[f'{v/1e6:.1f}M' for v in tier_analysis['quantity_of_merchants']],
           textposition='auto',
           marker_color='#C73E1D'),
    row=2, col=2
)

fig.update_xaxes(title_text="Price Tier", row=1, col=1)
fig.update_xaxes(title_text="Price Tier", row=1, col=2)
fig.update_xaxes(title_text="Price Tier", row=2, col=1)
fig.update_xaxes(title_text="Price Tier", row=2, col=2)
fig.update_yaxes(title_text="TPV (Billions R$)", row=1, col=1)
fig.update_yaxes(title_text="Avg Ticket (R$)", row=1, col=2)
fig.update_yaxes(title_text="Transactions (Millions)", row=2, col=1)
fig.update_yaxes(title_text="Merchants (Millions)", row=2, col=2)
fig.update_layout(height=800, showlegend=False, title_text="Price Tier Performance Analysis")
fig.write_html('/mnt/user-data/outputs/visualizations/05_price_tier_analysis.html')
print("   ✓ Saved: 05_price_tier_analysis.html")

# ============================================================================
# 6. TIME SERIES ANALYSIS
# ============================================================================
print("6. Creating Time Series Analysis...")

daily_tpv = df.groupby('day').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum'
}).reset_index()
daily_tpv['avg_ticket'] = daily_tpv['tpv'] / daily_tpv['quantity_transactions']

fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Daily TPV Trend', 'Daily Average Ticket Trend'),
    specs=[[{'type': 'scatter'}], [{'type': 'scatter'}]]
)

fig.add_trace(
    go.Scatter(x=daily_tpv['day'], y=daily_tpv['tpv']/1e6,
               mode='lines+markers',
               name='Daily TPV',
               line=dict(color='#2E86AB', width=2),
               marker=dict(size=4)),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=daily_tpv['day'], y=daily_tpv['avg_ticket'],
               mode='lines+markers',
               name='Daily Avg Ticket',
               line=dict(color='#F18F01', width=2),
               marker=dict(size=4)),
    row=2, col=1
)

fig.update_xaxes(title_text="Date", row=1, col=1)
fig.update_xaxes(title_text="Date", row=2, col=1)
fig.update_yaxes(title_text="TPV (Millions R$)", row=1, col=1)
fig.update_yaxes(title_text="Avg Ticket (R$)", row=2, col=1)
fig.update_layout(height=700, showlegend=False, title_text="Daily Performance Trends")
fig.write_html('/mnt/user-data/outputs/visualizations/06_time_series.html')
print("   ✓ Saved: 06_time_series.html")

# ============================================================================
# 7. WEEKDAY ANALYSIS
# ============================================================================
print("7. Creating Weekday Analysis...")

day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
weekday_analysis = df.groupby('day_of_week').agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum'
}).reset_index()
weekday_analysis['avg_ticket'] = weekday_analysis['tpv'] / weekday_analysis['quantity_transactions']
weekday_analysis['day_of_week'] = pd.Categorical(weekday_analysis['day_of_week'], categories=day_order, ordered=True)
weekday_analysis = weekday_analysis.sort_values('day_of_week')

fig = make_subplots(
    rows=1, cols=2,
    subplot_titles=('TPV by Day of Week', 'Average Ticket by Day of Week'),
    specs=[[{'type': 'bar'}, {'type': 'bar'}]]
)

colors = ['#2E86AB', '#2E86AB', '#2E86AB', '#2E86AB', '#2E86AB', '#C73E1D', '#C73E1D']

fig.add_trace(
    go.Bar(x=weekday_analysis['day_of_week'], y=weekday_analysis['tpv']/1e9,
           marker_color=colors,
           text=[f'R$ {v/1e9:.2f}B' for v in weekday_analysis['tpv']],
           textposition='auto'),
    row=1, col=1
)

fig.add_trace(
    go.Bar(x=weekday_analysis['day_of_week'], y=weekday_analysis['avg_ticket'],
           marker_color=colors,
           text=[f'R$ {v:.2f}' for v in weekday_analysis['avg_ticket']],
           textposition='auto'),
    row=1, col=2
)

fig.update_xaxes(title_text="Day of Week", row=1, col=1)
fig.update_xaxes(title_text="Day of Week", row=1, col=2)
fig.update_yaxes(title_text="TPV (Billions R$)", row=1, col=1)
fig.update_yaxes(title_text="Avg Ticket (R$)", row=1, col=2)
fig.update_layout(height=500, showlegend=False, title_text="Weekday Performance Analysis")
fig.write_html('/mnt/user-data/outputs/visualizations/07_weekday_analysis.html')
print("   ✓ Saved: 07_weekday_analysis.html")

# ============================================================================
# 8. ANTICIPATION METHOD BY ENTITY
# ============================================================================
print("8. Creating Anticipation Method Analysis...")

anticipation_by_entity = df.groupby(['entity', 'anticipation_method']).agg({
    'tpv': 'sum'
}).reset_index()

fig = px.bar(anticipation_by_entity, x='entity', y='tpv', color='anticipation_method',
             title='Anticipation Method Usage by Entity',
             labels={'tpv': 'TPV (R$)', 'entity': 'Entity', 'anticipation_method': 'Anticipation Method'},
             barmode='group',
             color_discrete_sequence=['#2E86AB', '#F18F01', '#6A994E', '#C73E1D'])

fig.update_yaxes(title_text="TPV (R$)")
fig.update_layout(height=500)
fig.write_html('/mnt/user-data/outputs/visualizations/08_anticipation_by_entity.html')
print("   ✓ Saved: 08_anticipation_by_entity.html")

# ============================================================================
# 9. ENTITY x PRODUCT MATRIX
# ============================================================================
print("9. Creating Entity x Product Matrix...")

entity_product = df.groupby(['entity', 'product']).agg({
    'tpv': 'sum',
    'quantity_transactions': 'sum'
}).reset_index()
entity_product['avg_ticket'] = entity_product['tpv'] / entity_product['quantity_transactions']

fig = px.bar(entity_product, x='product', y='tpv', color='entity',
             title='TPV by Product and Entity',
             labels={'tpv': 'TPV (R$)', 'product': 'Product', 'entity': 'Entity'},
             barmode='group',
             color_discrete_sequence=['#2E86AB', '#A23B72'])

fig.update_yaxes(title_text="TPV (R$)")
fig.update_layout(height=500)
fig.write_html('/mnt/user-data/outputs/visualizations/09_entity_product_matrix.html')
print("   ✓ Saved: 09_entity_product_matrix.html")

# ============================================================================
# 10. COMPREHENSIVE DASHBOARD
# ============================================================================
print("10. Creating Comprehensive Dashboard...")

fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=('TPV by Entity', 'TPV by Product',
                    'TPV by Payment Method', 'Daily TPV Trend',
                    'Installments Distribution', 'Price Tier Analysis'),
    specs=[[{'type': 'bar'}, {'type': 'bar'}],
           [{'type': 'bar'}, {'type': 'scatter'}],
           [{'type': 'bar'}, {'type': 'bar'}]],
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

# Entity
entity_data = df.groupby('entity')['tpv'].sum().reset_index().sort_values('tpv', ascending=False)
fig.add_trace(go.Bar(x=entity_data['entity'], y=entity_data['tpv']/1e9, 
                     marker_color=['#2E86AB', '#A23B72'], showlegend=False), row=1, col=1)

# Product
product_data = df.groupby('product')['tpv'].sum().reset_index().sort_values('tpv', ascending=False)
fig.add_trace(go.Bar(x=product_data['product'], y=product_data['tpv']/1e9,
                     marker_color='#F18F01', showlegend=False), row=1, col=2)

# Payment Method
payment_data = df.groupby('payment_method')['tpv'].sum().reset_index().sort_values('tpv', ascending=False)
fig.add_trace(go.Bar(x=payment_data['payment_method'], y=payment_data['tpv']/1e9,
                     marker_color='#6A994E', showlegend=False), row=2, col=1)

# Daily Trend
fig.add_trace(go.Scatter(x=daily_tpv['day'], y=daily_tpv['tpv']/1e6,
                        mode='lines', line=dict(color='#C73E1D', width=2),
                        showlegend=False), row=2, col=2)

# Installments
inst_data = df.groupby('installments')['tpv'].sum().reset_index().sort_values('installments')
fig.add_trace(go.Bar(x=inst_data['installments'], y=inst_data['tpv']/1e9,
                     marker_color='#2E86AB', showlegend=False), row=3, col=1)

# Price Tier
tier_data = df.groupby('price_tier')['tpv'].sum().reset_index().sort_values('tpv', ascending=False)
fig.add_trace(go.Bar(x=tier_data['price_tier'], y=tier_data['tpv']/1e9,
                     marker_color='#A23B72', showlegend=False), row=3, col=2)

# Update axes
fig.update_yaxes(title_text="TPV (Billions R$)", row=1, col=1)
fig.update_yaxes(title_text="TPV (Billions R$)", row=1, col=2)
fig.update_yaxes(title_text="TPV (Billions R$)", row=2, col=1)
fig.update_yaxes(title_text="TPV (Millions R$)", row=2, col=2)
fig.update_yaxes(title_text="TPV (Billions R$)", row=3, col=1)
fig.update_yaxes(title_text="TPV (Billions R$)", row=3, col=2)

fig.update_layout(height=1200, title_text="CloudWalk Operations Intelligence Dashboard", showlegend=False)
fig.write_html('/mnt/user-data/outputs/visualizations/10_comprehensive_dashboard.html')
print("   ✓ Saved: 10_comprehensive_dashboard.html")

print("\n" + "="*80)
print("All visualizations created successfully!")
print("="*80)
print("\nFiles saved in: /mnt/user-data/outputs/visualizations/")
print("\nVisualization files:")
print("  01_tpv_by_entity.html")
print("  02_tpv_by_product.html")
print("  03_payment_method.html")
print("  04_installments_analysis.html")
print("  05_price_tier_analysis.html")
print("  06_time_series.html")
print("  07_weekday_analysis.html")
print("  08_anticipation_by_entity.html")
print("  09_entity_product_matrix.html")
print("  10_comprehensive_dashboard.html")
