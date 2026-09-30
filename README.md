# Daily Spend & Subscription Intelligence (DSSI)

An end-to-end personal finance analytics project built with Python, Pandas, PostgreSQL, Streamlit, and Plotly.

## Project Overview

DSSI processes synthetic financial transaction data and converts it into useful spending insights.

The project includes data cleaning, PostgreSQL integration, recurring subscription detection, and an interactive analytics dashboard.

## Features

- 1,000 synthetic financial transactions
- Data cleaning and transformation using Pandas
- PostgreSQL data storage
- Recurring subscription detection
- Spending analysis by category and merchant
- Monthly spending trend analysis
- Interactive category and date filters
- KPI dashboard
- Recent transaction analysis

## Tech Stack

- Python
- Pandas
- PostgreSQL
- SQLAlchemy
- Streamlit
- Plotly
- Git & GitHub

## Project Structure

    dssi-daily-spend-intelligence/
    ├── data/
    │   ├── raw/
    │   └── processed/
    ├── src/
    │   ├── load_to_postgres.py
    │   └── detect_subscriptions.py
    ├── streamlit/
    │   └── app.py
    ├── requirements.txt
    ├── .gitignore
    └── README.md

## Data Pipeline

    Raw Transaction Data
            |
            v
      Python / Pandas
            |
            v
     Cleaned Dataset
       /     |     \
      v      v      v
 PostgreSQL  Subscription  Streamlit
             Detection     Dashboard

## PostgreSQL Integration

The cleaned transaction dataset is loaded into PostgreSQL using SQLAlchemy.

Successfully verified:

    1,000 rows loaded

## Subscription Detection

A recurring-payment heuristic analyzes transaction frequency and amount consistency to identify potential subscriptions.

The current synthetic dataset produced 0 qualifying subscriptions. The detector returns the actual result rather than generating artificial matches.

## Dashboard

The interactive Streamlit dashboard includes:

- Total spending
- Number of transactions
- Average transaction amount
- Top spending category
- Spending by category
- Monthly spending trends
- Top 10 merchants
- Recent transactions
- Category filters
- Date filters

## Run the Project

Install dependencies:

    pip install -r requirements.txt

Run subscription detection:

    python src/detect_subscriptions.py

Load data into PostgreSQL:

    python src/load_to_postgres.py

Launch the dashboard:

    python -m streamlit run streamlit/app.py

## Author

Sai Tarun Dantuluri
