import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sales Data Dashboard", layout="wide")

# --- LOAD DATA ---
@st.cache_data
def load_data():
    df = pd.read_csv("data-2 (1).csv", encoding="ISO-8859-1")
    
    # Clean dataset
    df = df.dropna(subset=['CustomerID', 'Description'])
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['CustomerID'] = df['CustomerID'].astype(int)
    df['Revenue'] = df['Quantity'] * df['UnitPrice']
    
    return df

df = load_data()

# --- TITLE ---
st.title("📊 Sales Data Analysis Dashboard")

# --- FILTER ---
country_filter = st.sidebar.multiselect("Select Country", options=df['Country'].unique(), default=df['Country'].unique())
df = df[df['Country'].isin(country_filter)]

# --- HOURLY SALES TREND ---
st.subheader("Hourly Sales Trend")
df['Hour'] = df['InvoiceDate'].dt.hour
hourly_sales = df.groupby('Hour', as_index=False)['Revenue'].sum()

fig, ax = plt.subplots(figsize=(8,4))
sns.lineplot(x='Hour', y='Revenue', data=hourly_sales, marker='o', ax=ax)
st.pyplot(fig)

# --- SALES HEATMAP ---
st.subheader("Sales Heatmap (Day vs Hour)")
df['Day'] = df['InvoiceDate'].dt.day_name()
heatmap_data = df.pivot_table(values='Revenue', index='Day', columns='Hour', aggfunc='sum')

fig, ax = plt.subplots(figsize=(10,5))
sns.heatmap(heatmap_data, cmap='YlGnBu', ax=ax)
st.pyplot(fig)

# --- TOP 10 COUNTRIES ---
st.subheader("Top 10 Countries by Revenue")
country_sales = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(x=country_sales.index, y=country_sales.values, ax=ax)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
st.pyplot(fig)

# --- TOP 10 PRODUCTS ---
st.subheader("Top 10 Products by Revenue")
top_products = df.groupby('Description')['Revenue'].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(x=top_products.values, y=top_products.index, ax=ax)
st.pyplot(fig)

# --- TOP 10 CUSTOMERS ---
st.subheader("Top 10 Customers by Revenue")
top_customers = df.groupby('CustomerID')['Revenue'].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(8,4))
sns.barplot(x=top_customers.index.astype(str), y=top_customers.values, ax=ax)
st.pyplot(fig)

# --- FOOTER ---
st.markdown("---")
st.markdown("✅ Built with Streamlit | Data Source: Online Retail Dataset")
