
import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title='CAD-EWS Dashboard', layout='wide')
st.title("🧭 CAD‑EWS — Credit & Deposit Early Warning System (MVP)")

st.sidebar.header("Modules")
module = st.sidebar.selectbox("Module", ["Overview", "Credit Alerts", "Transaction Alerts"])

API_BASE = st.sidebar.text_input("Backend API base URL", "http://localhost:8000")

if module == "Overview":
    st.markdown("""
    **Overview**
    - This dashboard displays alerts detected by the CAD‑EWS backend.
    - Use **Credit Alerts** for borrower stress signals.
    - Use **Transaction Alerts** for suspicious transaction patterns.
    """)
    if st.button("Health check API"):
        try:
            r = requests.get(f"{API_BASE}/health", timeout=5)
            st.success(f"Backend status: {r.json()}")
        except Exception as e:
            st.error(f"Could not reach backend: {e}")
elif module == "Credit Alerts":
    st.subheader("Borrower Stress Alerts")
    try:
        r = requests.get(f"{API_BASE}/credit-alerts", timeout=8)
        data = r.json().get("alerts", [])
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.write(f"Total alerts: {len(data)}")
        else:
            st.info("No credit alerts found.")
    except Exception as e:
        st.error(f"Error fetching credit alerts: {e}")
else:
    st.subheader("Suspicious Transaction Alerts")
    try:
        r = requests.get(f"{API_BASE}/transaction-alerts", timeout=8)
        data = r.json().get("alerts", [])
        if data:
            df = pd.DataFrame(data)
            st.dataframe(df)
            st.write(f"Total alerts: {len(data)}")
        else:
            st.info("No transaction alerts found.")
    except Exception as e:
        st.error(f"Error fetching transaction alerts: {e}")
