
from typing import List, Dict
import pandas as pd

def detect_credit_stress(df: pd.DataFrame) -> List[Dict]:
    alerts = []
    for _, row in df.iterrows():
        overdue = float(row.get("overdue_days", 0) or 0)
        missed_emis = int(row.get("missed_emi_count", 0) or 0)
        utilization = float(row.get("utilization_ratio", 0) or 0)
        cust = row.get("customer_id")
        severity = "Low"
        msg = []
        if overdue > 60 or missed_emis >= 3 or utilization > 0.95:
            severity = "High"
        elif overdue > 30 or missed_emis >= 2 or utilization > 0.9:
            severity = "Medium"

        if overdue > 0:
            msg.append(f"Overdue: {int(overdue)} days")
        if missed_emis > 0:
            msg.append(f"Missed EMIs: {missed_emis}")
        if utilization > 0:
            msg.append(f"Utilization: {utilization:.2f}")

        if severity != "Low":
            alerts.append({
                "customer_id": cust,
                "alert_type": "Credit Stress",
                "severity": severity,
                "message": "; ".join(msg)
            })
    return alerts
