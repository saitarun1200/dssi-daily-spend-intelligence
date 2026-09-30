import pandas as pd

INPUT_FILE = "data/processed/transactions_clean.csv"
OUTPUT_FILE = "data/processed/detected_subscriptions.csv"

df = pd.read_csv(INPUT_FILE)
df["transaction_date"] = pd.to_datetime(df["transaction_date"])

results = []

for merchant, group in df.groupby("merchant"):
    group = group.sort_values("transaction_date")

    if len(group) < 3:
        continue

    gaps = group["transaction_date"].diff().dt.days.dropna()

    avg_gap = gaps.mean()
    avg_amount = group["amount"].mean()
    amount_std = group["amount"].std()

    amount_variation = amount_std / avg_amount if avg_amount > 0 else 999

    if 20 <= avg_gap <= 40 and amount_variation <= 0.25:
        results.append({
            "merchant": merchant,
            "transactions": len(group),
            "average_amount": round(avg_amount, 2),
            "average_days_between_payments": round(avg_gap, 1),
            "estimated_monthly_cost": round(avg_amount, 2),
            "estimated_annual_cost": round(avg_amount * 12, 2)
        })

subscriptions = pd.DataFrame(results)
subscriptions.to_csv(OUTPUT_FILE, index=False)

print("Subscription detection complete!")
print(f"Subscriptions detected: {len(subscriptions)}")
print(f"Saved to: {OUTPUT_FILE}")

if not subscriptions.empty:
    print(subscriptions.to_string(index=False))