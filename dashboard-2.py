
import streamlit as st
import pandas as pd
import plotly.express as px

# Load or define the data
data = {
    'Metric': [
        'Retail Fill Up', 'Consumer Volume', 'Retail Volume', 'Net Margin',
        'Total Volume', 'Gross Margin', 'Fuel Card Volume', 'Net Profit',
        'Retail Transactions', 'Business Profit', 'Gross Profit',
        'Bunkered Volume', 'Gross Sales', 'Replacement Costs',
        'Blended Costs', 'Bunkering Commission', 'Total Fees'
    ],
    'Avg_2024': [
        23.64, 1943.28, 2221.58, 17.32, 2435.09, 18.40, 491.77, 300.20,
        92.93, 301.72, 330.09, 206.80, 2830.48, 113.76, 2500.33, 1.48, 29.92
    ],
    'Avg_2025': [
        25.13, 1955.96, 2228.19, 17.28, 2422.00, 18.21, 466.07, 283.06,
        87.61, 284.41, 307.23, 188.35, 2546.71, 102.12, 2239.40, 1.32, 24.19
    ]
}
df = pd.DataFrame(data)
df['% Change'] = ((df['Avg_2025'] - df['Avg_2024']) / df['Avg_2024']) * 100

# Streamlit UI
st.set_page_config(page_title="May 2024 vs 2025 Dashboard", layout="wide")
st.title("📊 May 2025 vs May 2024 Metrics Dashboard")

# Metric Selector
selected_metric = st.selectbox("Select a metric to compare:", df['Metric'])
row = df[df['Metric'] == selected_metric].iloc[0]
comparison_df = pd.DataFrame({
    'Year': ['2024', '2025'],
    'Value': [row['Avg_2024'], row['Avg_2025']]
})
st.plotly_chart(px.bar(comparison_df, x='Year', y='Value', title=f"{selected_metric} Comparison"))

# Highlight requested metrics
highlight_metrics = ['Gross Margin', 'Gross Profit', 'Retail Volume', 'Retail Fill Up', 'Replacement Costs', 'Retail Transactions']
highlight_df = df[df['Metric'].isin(highlight_metrics)].copy()

st.subheader("🔍 Focus Metrics Overview")
st.dataframe(highlight_df[['Metric', 'Avg_2024', 'Avg_2025', '% Change']].style.format({
    'Avg_2024': '{:.2f}',
    'Avg_2025': '{:.2f}',
    '% Change': '{:.2f}'
}))

# Columns for change visualisations
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Metric Increases")
    top_increases = df.sort_values('% Change', ascending=False).head(10)
    st.plotly_chart(px.bar(top_increases, x='% Change', y='Metric', orientation='h', color_discrete_sequence=['green']))

with col2:
    st.subheader("Top 10 Metric Decreases")
    top_decreases = df.sort_values('% Change').head(10)
    st.plotly_chart(px.bar(top_decreases, x='% Change', y='Metric', orientation='h', color_discrete_sequence=['red']))

# Table summary
st.markdown("### 📋 Full Metric Table")
st.dataframe(df.style.format({
    'Avg_2024': '{:.2f}',
    'Avg_2025': '{:.2f}',
    '% Change': '{:.2f}'
}))

# Additional Investigations
st.markdown("## 🧠 Strategic Investigations")
st.markdown("### 1. 📣 Promotion & Loyalty Scheme Trends")
st.markdown("Use this space to correlate promotions with transaction dips or volume lifts. Upload your promo calendar below:")
promo_file = st.file_uploader("Upload Promotion Schedule (CSV with Date, Description)", type=["csv"])
if promo_file:
    promo_df = pd.read_csv(promo_file)
    st.dataframe(promo_df)

st.markdown("### 2. 🛑 Site-level Fill-Up Patterns")
st.markdown("Upload site-level fill-up volumes to spot outliers across May 24 vs 25.")
sites_file = st.file_uploader("Upload Site Fill-Up Data (CSV with Site, Date, Litres)", type=["csv"], key="site")
if sites_file:
    site_df = pd.read_csv(sites_file)
    st.dataframe(site_df.head())
    st.markdown("#### Site-Level Average Fill-Ups")
    site_avg = site_df.groupby("Site")["Litres"].mean().reset_index()
    st.plotly_chart(px.bar(site_avg, x="Site", y="Litres", title="Avg Fill-Up by Site"))

st.markdown("### 3. 💰 Price Sensitivity vs Competitors")
st.markdown("Upload pole price comparison (daily) between you and competitors (Shell, Circle K, OK) for E95/Diesel")
price_file = st.file_uploader("Upload Pricing Data (Date, Brand, E95_Price, Diesel_Price)", type=["csv"], key="price")
if price_file:
    price_df = pd.read_csv(price_file)
    st.dataframe(price_df.head())
    st.plotly_chart(px.line(price_df, x="Date", y="E95_Price", color="Brand", title="E95 Daily Price Comparison"))
