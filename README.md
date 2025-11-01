
# CAD-EWS MVP
Credit and Deposit Early Warning System (CAD-EWS) - Minimal Viable Product

## Overview
This prototype contains a simple backend (FastAPI) that applies rule-based detection for:
- Credit stress (borrowers)
- Suspicious transactions (deposit accounts)

and a Streamlit dashboard that fetches alerts from the backend and displays them.

## Structure
```
cad-ews/
├── backend/
│   ├── main.py
│   └── utils/
│       ├── credit_rules.py
│       └── transaction_rules.py
├── data/
│   ├── credit_data.csv
│   └── transactions.csv
├── dashboard/
│   └── app.py
├── requirements.txt
└── README.md
```

## Quick start (local)
1. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate      # on Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

2. Start the backend (from project root):
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Start the dashboard (in a separate terminal, from project root):
```bash
cd dashboard
streamlit run app.py
```

4. The Streamlit UI will open in your browser (usually at http://localhost:8501). The backend APIs are at http://localhost:8000/

## Notes
- Data is synthetic and stored in `data/` as CSV files. Replace with real data or connect to a database for production.
- This MVP uses simple rule-based detection. You can extend by adding ML models, persistence, alert history, and integration with bank systems.
