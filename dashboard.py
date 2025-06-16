
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

col1, col2 = st.columns(2)
with col1:
    st.subheader("Top 5 Metric Increases")
    st.plotly_chart(px.bar(df.sort_values('% Change', ascending=False).head(5),
                           x='% Change', y='Metric', orientation='h', color_discrete_sequence=['green']))
with col2:
    st.subheader("Top 5 Metric Decreases")
    st.plotly_chart(px.bar(df.sort_values('% Change').head(5),
                           x='% Change', y='Metric', orientation='h', color_discrete_sequence=['red']))

st.markdown("### 📋 Full Metric Table")
st.dataframe(df.style.format({
    'Avg_2024': '{:.2f}',
    'Avg_2025': '{:.2f}',
    '% Change': '{:.2f}'
}))
