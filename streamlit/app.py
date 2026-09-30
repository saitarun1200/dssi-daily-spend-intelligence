import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------
# Page configuration
# -----------------------------
st.set_page_config(
    page_title="DSSI Dashboard",
    page_icon="💳",
    layout="wide"
)

# -----------------------------
# Load cleaned transaction data
# -----------------------------
DATA_FILE = "data/processed/transactions_clean.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE)
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    return df


df = load_data()

# -----------------------------
# Dashboard title
# -----------------------------
st.title("💳 Daily Spend & Subscription Intelligence")
st.caption("Personal finance analytics dashboard built with Python, Pandas, Plotly, and Streamlit.")

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("🔎 Filters")

categories = sorted(df["category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=categories,
    default=categories
)

min_date = df["transaction_date"].min().date()
max_date = df["transaction_date"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

filtered_df = df[df["category"].isin(selected_categories)].copy()

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["transaction_date"].dt.date >= start_date)
        & (filtered_df["transaction_date"].dt.date <= end_date)
    ]

if filtered_df.empty:
    st.warning("No transactions match the selected filters.")
    st.stop()

# -----------------------------
# KPI calculations
# -----------------------------
total_spending = filtered_df["amount"].sum()
transaction_count = len(filtered_df)
average_transaction = filtered_df["amount"].mean()

category_totals = (
    filtered_df
    .groupby("category")["amount"]
    .sum()
    .sort_values(ascending=False)
)

top_category = category_totals.index[0]

# -----------------------------
# KPI cards
# -----------------------------
st.subheader("📌 Spending Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Spending",
    f"${total_spending:,.2f}"
)

col2.metric(
    "Transactions",
    f"{transaction_count:,}"
)

col3.metric(
    "Average Transaction",
    f"${average_transaction:,.2f}"
)

col4.metric(
    "Top Category",
    top_category
)

st.divider()

# -----------------------------
# Spending by category
# -----------------------------
st.subheader("📊 Spending by Category")

category_spending = (
    filtered_df
    .groupby("category", as_index=False)["amount"]
    .sum()
    .sort_values("amount", ascending=False)
)

fig_category = px.bar(
    category_spending,
    x="category",
    y="amount",
    labels={
        "category": "Category",
        "amount": "Spending ($)"
    },
    title="Total Spending by Category"
)

st.plotly_chart(
    fig_category,
    width="stretch"
)

# -----------------------------
# Monthly spending trend
# -----------------------------
st.subheader("📈 Monthly Spending Trend")

monthly_spending = (
    filtered_df
    .set_index("transaction_date")
    .resample("ME")["amount"]
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_spending,
    x="transaction_date",
    y="amount",
    markers=True,
    labels={
        "transaction_date": "Month",
        "amount": "Spending ($)"
    },
    title="Monthly Spending"
)

st.plotly_chart(
    fig_monthly,
    width="stretch"
)

# -----------------------------
# Top merchants
# -----------------------------
st.subheader("🏪 Top 10 Merchants")

merchant_spending = (
    filtered_df
    .groupby("merchant", as_index=False)["amount"]
    .sum()
    .sort_values("amount", ascending=False)
    .head(10)
)

fig_merchants = px.bar(
    merchant_spending,
    x="merchant",
    y="amount",
    labels={
        "merchant": "Merchant",
        "amount": "Spending ($)"
    },
    title="Top 10 Merchants by Spending"
)

st.plotly_chart(
    fig_merchants,
    width="stretch"
)

# -----------------------------
# Recent transactions
# -----------------------------
st.subheader("🧾 Recent Transactions")

recent_transactions = (
    filtered_df
    .sort_values("transaction_date", ascending=False)
    .head(20)
    .copy()
)

recent_transactions["transaction_date"] = (
    recent_transactions["transaction_date"]
    .dt.strftime("%Y-%m-%d")
)

st.dataframe(
    recent_transactions[
        [
            "transaction_date",
            "merchant",
            "category",
            "amount",
            "transaction_type"
        ]
    ],
    width="stretch",
    hide_index=True
)

st.caption(
    f"Showing analytics for {len(filtered_df):,} transactions."
)
