import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
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
    st.warning("🚧 Production backend not ready yet. Running in Demo Mode.")
    mode = "Demo"

# ---------------------------
# FILE UPLOAD SECTION
# ---------------------------
st.sidebar.subheader("📤 Upload Data Files")

credit_file = st.sidebar.file_uploader("Upload Credit Data (CSV)", type=["csv"])
txn_file = st.sidebar.file_uploader("Upload Transaction Data (CSV)", type=["csv"])

# ---------------------------
# DATA LOADING
# ---------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

@st.cache_data
def load_demo_data():
    credit_df = pd.read_csv(DATA_DIR / "credit_data.csv")
    txn_df = pd.read_csv(DATA_DIR / "transactions.csv")
    return credit_df, txn_df

# ---------------------------
# MAIN VIEW
# ---------------------------
tab1, tab2 = st.tabs(["📊 Credit Monitoring", "💸 Transaction Monitoring"])

# ==========================================================
# CREDIT MONITORING TAB
# ==========================================================
with tab1:
    st.subheader("Borrower Stress Detection")

    # Decide which data to use
    if credit_file is not None:
        try:
            credit_df = pd.read_csv(credit_file)
            st.success(f"Uploaded {len(credit_df)} credit records.")
        except Exception as e:
            st.error(f"❌ Error reading uploaded credit file: {e}")
            st.stop()
    else:
        st.info("Using demo credit dataset (upload your own CSV to override).")
        credit_df, _ = load_demo_data()

    # Run detection
    credit_alerts = detect_credit_stress(credit_df)

    # Display data + alerts
    st.write("### Sample Credit Data", credit_df.head())
    alert_df = pd.DataFrame(credit_alerts)

    if not alert_df.empty:
        st.write("### 🚨 Detected Credit Alerts", alert_df)
        st.download_button(
            label="⬇️ Download Credit Alerts",
            data=alert_df.to_csv(index=False).encode("utf-8"),
            file_name="credit_alerts.csv",
            mime="text/csv"
        )
    else:
        st.info("No borrower stress detected.")

    st.info(f"Running in {mode} Mode")

# ==========================================================
# TRANSACTION MONITORING TAB
# ==========================================================
with tab2:
    st.subheader("Suspicious Transaction Detection")

    # Decide data source
    if txn_file is not None:
        try:
            txn_df = pd.read_csv(txn_file)
            st.success(f"Uploaded {len(txn_df)} transaction records.")
        except Exception as e:
            st.error(f"❌ Error reading uploaded transaction file: {e}")
            st.stop()
    else:
        st.info("Using demo transaction dataset (upload your own CSV to override).")
        _, txn_df = load_demo_data()

    # Run detection
    txn_alerts = detect_suspicious_transactions(txn_df)

    # Display data + alerts
    st.write("### Sample Transaction Data", txn_df.head())
    alert_df = pd.DataFrame(txn_alerts)

    if not alert_df.empty:
        st.write("### 🚨 Detected Suspicious Transactions", alert_df)
        st.download_button(
            label="⬇️ Download Transaction Alerts",
            data=alert_df.to_csv(index=False).encode("utf-8"),
            file_name="transaction_alerts.csv",
            mime="text/csv"
        )
    else:
        st.info("No suspicious transactions detected.")

    st.info(f"Running in {mode} Mode")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("© 2025 CAD-EWS | Credit & Deposit Early Warning System | Built with ❤️ using Streamlit")
