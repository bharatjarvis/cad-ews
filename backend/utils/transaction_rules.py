
from typing import List, Dict
import pandas as pd

def detect_suspicious_transactions(df: pd.DataFrame) -> List[Dict]:
    alerts = []
    for _, row in df.iterrows():
        account_id = row.get("account_id")
        customer_id = row.get("customer_id")
        txn_amount = float(row.get("txn_amount", 0) or 0)
        txn_count = int(row.get("txn_count_last_24h", 0) or 0)
        avg_txn = float(row.get("avg_txn_amount", 0) or 0)
        expected_income = float(row.get("expected_income", 0) or 0)

        # Rule: Many small transactions in 24h (possible smurfing)
        if txn_count >= 10 and avg_txn <= 5000:
            alerts.append({
                "account_id": account_id,
                "customer_id": customer_id,
                "alert_type": "Smurfing Pattern",
                "severity": "High",
                "message": f"{txn_count} transactions in 24h with avg ₹{avg_txn:.0f}"
            })
            continue

        # Rule: Single large transaction exceeding profile
        if expected_income > 0 and txn_amount > 5 * expected_income:
            alerts.append({
                "account_id": account_id,
                "customer_id": customer_id,
                "alert_type": "Profile Mismatch - Large Txn",
                "severity": "Medium",
                "message": f"Txn ₹{txn_amount:.0f} >> expected income ₹{expected_income:.0f}"
            })
            continue

        # Rule: Very large single txn independent of income
        if txn_amount >= 1_000_000:  # ₹10 lakh threshold
            alerts.append({
                "account_id": account_id,
                "customer_id": customer_id,
                "alert_type": "Very Large Transaction",
                "severity": "High",
                "message": f"Txn ₹{txn_amount:.0f} exceeds ₹1,000,000"
            })
            continue
    return alerts
