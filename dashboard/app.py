import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
from pathlib import Path
from backend.utils.credit_rules import detect_credit_stress
from backend.utils.transaction_rules import detect_suspicious_transactions

# ---------------------------
# BASIC CONFIG
# ---------------------------
st.set_page_config(
    page_title="CAD-EWS Dashboard",
    page_icon="🧭",
    layout="wide"
)

# ---------------------------
# HEADER
# ---------------------------
st.title("🧭 Credit and Deposit Early Warning System (CAD-EWS)")
st.markdown("An AI-assisted early warning system for **credit stress** and **suspicious transactions**.")

# ---------------------------
# SIDEBAR: SETTINGS
# ---------------------------
st.sidebar.header("⚙️ Settings")

mode_toggle = st.sidebar.toggle("Enable Production Mode", value=False)
mode = "Production" if mode_toggle else "Demo"

# Mode badge on top-right
badge_color = "🟢" if mode == "Demo" else "🔴"
st.markdown(
    f"""
    <div style='text-align: right; font-size: 18px;'>
        <b>Mode:</b> {badge_color} {mode}
    </div>
    """,
    unsafe_allow_html=True
)

if mode == "Production":
    st.warning("🚧 Production backend not ready yet. Currently running in Demo Mode.")
    mode = "Demo"  # fallback for demo data usage

# ---------------------------
# DATA LOADING
# ---------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

@st.cache_data
def load_local_data():
    credit_df = pd.read_csv(DATA_DIR / "credit_data.csv")
    txn_df = pd.read_csv(DATA_DIR / "transactions.csv")
    return credit_df, txn_df

credit_df, txn_df = load_local_data()

# ---------------------------
# RUN DETECTION LOGIC
# ---------------------------
credit_alerts = detect_credit_stress(credit_df)
txn_alerts = detect_suspicious_transactions(txn_df)

# ---------------------------
# MAIN VIEW
# ---------------------------
tab1, tab2 = st.tabs(["📊 Credit Monitoring", "💸 Transaction Monitoring"])

with tab1:
    st.subheader("Borrower Stress Detection")
    st.dataframe(pd.DataFrame(credit_alerts))
    st.info(f"Running in {mode} Mode")

with tab2:
    st.subheader("Suspicious Transaction Detection")
    st.dataframe(pd.DataFrame(txn_alerts))
    st.info(f"Running in {mode} Mode")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("© 2025 CAD-EWS | Credit & Deposit Early Warning System | Built with ❤️ using Streamlit")
