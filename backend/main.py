
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
from utils.credit_rules import detect_credit_stress
from utils.transaction_rules import detect_suspicious_transactions

app = FastAPI(title="CAD-EWS API (MVP)")

# Allow CORS for local testing with Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'

@app.get("/health")
def health():
    return {"status":"ok"}

@app.get("/credit-alerts")
def credit_alerts():
    csv = DATA_DIR / "credit_data.csv"
    df = pd.read_csv(csv)
    alerts = detect_credit_stress(df)
    return {"count": len(alerts), "alerts": alerts}

@app.get("/transaction-alerts")
def transaction_alerts():
    csv = DATA_DIR / "transactions.csv"
    df = pd.read_csv(csv)
    alerts = detect_suspicious_transactions(df)
    return {"count": len(alerts), "alerts": alerts}
