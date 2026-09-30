import pandas as pd
from sqlalchemy import create_engine, text

DATABASE_URL = "postgresql+psycopg2://saitarun@localhost:5432/dssi"

df = pd.read_csv("data/processed/transactions_clean.csv")
df["transaction_date"] = pd.to_datetime(df["transaction_date"])

engine = create_engine(DATABASE_URL)

df.to_sql(
    "raw_transactions",
    engine,
    if_exists="replace",
    index=False
)

with engine.connect() as connection:
    count = connection.execute(
        text("SELECT COUNT(*) FROM raw_transactions")
    ).scalar()

print("PostgreSQL load successful!")
print(f"Rows loaded: {count}")