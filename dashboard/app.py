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
st.set_page_config(import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

st.title("🧭 Credit and Deposit Early Warning System (CAD-EWS)")
st.markdown("Upload your **Credit** and **Transaction** datasets for automated analysis and visualization.")

# ---------------------------
# TEMPLATE CSV BUTTONS
# ---------------------------
st.sidebar.subheader("📄 Download Template CSV Files")

credit_template = """customer_id,overdue_days,missed_emi_count,utilization_ratio,monthly_income
CUST001,45,1,0.85,40000
"""

txn_template = """account_id,customer_id,txn_amount,txn_count_last_24h,avg_txn_amount,expected_income
ACC001,CUST001,200000,1,200000,40000
"""

st.sidebar.download_button(
    label="⬇️ Download Credit Template CSV",
    data=credit_template,
    file_name="credit_template.csv",
    mime="text/csv"
)

st.sidebar.download_button(
    label="⬇️ Download Transaction Template CSV",
    data=txn_template,
    file_name="transaction_template.csv",
    mime="text/csv"
)

# ---------------------------
# SIDEBAR SETTINGS
# ---------------------------
st.sidebar.header("⚙️ Settings")

mode_toggle = st.sidebar.toggle("Enable Production Mode", value=False)
mode = "Production" if mode_toggle else "Demo"

# Mode badge
badge_color = "🟢" if mode == "Demo" else "🔴"
st.markdown(
    f"<div style='text-align: right; font-size: 18px;'><b>Mode:</b> {badge_color} {mode}</div>",
    unsafe_allow_html=True
)

if mode == "Production":
    st.warning("🚧 Production backend not ready yet. Running in Demo Mode.")
    mode = "Demo"

# ---------------------------
# FILE UPLOADS
# ---------------------------
st.sidebar.subheader("📤 Upload Your Data")

credit_file = st.sidebar.file_uploader("Upload Credit Data (CSV)", type=["csv"])
txn_file = st.sidebar.file_uploader("Upload Transaction Data (CSV)", type=["csv"])

st.sidebar.markdown("---")
run_demo = st.sidebar.button("Run Sample Data (Demo Mode)")

# ---------------------------
# LOAD SAMPLE DATA
# ---------------------------
DATA_DIR = Path(__file__).resolve().parent.parent / "data"

@st.cache_data
def load_demo_data():
    credit_df = pd.read_csv(DATA_DIR / "credit_data.csv")
    txn_df = pd.read_csv(DATA_DIR / "transactions.csv")
    return credit_df, txn_df

# ---------------------------
# TABS
# ---------------------------
tab1, tab2 = st.tabs(["📊 Credit Monitoring", "💸 Transaction Monitoring"])

# =================================================
# CREDIT MONITORING
# =================================================
with tab1:
    st.subheader("Borrower Stress Detection")

    if credit_file is not None:
        credit_df = pd.read_csv(credit_file)
        st.success(f"Uploaded {len(credit_df)} credit records.")
    elif run_demo:
        credit_df, _ = load_demo_data()
        st.info("Running sample credit dataset.")
    else:
        st.info("Please upload a Credit CSV file or click 'Run Sample Data'.")
        st.stop()

    # Run detection
    credit_alerts = detect_credit_stress(credit_df)
    alert_df = pd.DataFrame(credit_alerts)

    # Show sample data
    st.write("### Sample Credit Data")
    st.dataframe(credit_df.head())

    # Visualizations
    st.write("### 📈 Credit Risk Visualizations")

    # Overdue distribution
    fig, ax = plt.subplots()
    ax.hist(credit_df["overdue_days"], bins=10)
    ax.set_title("Overdue Days Distribution")
    ax.set_xlabel("Days")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    # Utilization ratio distribution
    fig2, ax2 = plt.subplots()
    ax2.hist(credit_df["utilization_ratio"], bins=10)
    ax2.set_title("Utilization Ratio Distribution")
    ax2.set_xlabel("Utilization Ratio")
    ax2.set_ylabel("Frequency")
    st.pyplot(fig2)

    # EMI missed count plot
    fig3, ax3 = plt.subplots()
    ax3.hist(credit_df["missed_emi_count"], bins=10)
    ax3.set_title("Missed EMI Count Distribution")
    ax3.set_xlabel("Count")
    ax3.set_ylabel("Frequency")
    st.pyplot(fig3)

    # Alerts
    st.write("### 🚨 Detected Credit Alerts")
    st.dataframe(alert_df)

    st.download_button(
        label="⬇️ Download Credit Alerts",
        data=alert_df.to_csv(index=False).encode("utf-8"),
        file_name="credit_alerts.csv",
        mime="text/csv"
    )

    st.info(f"Running in {mode} Mode")

# =================================================
# TRANSACTION MONITORING
# =================================================
with tab2:
    st.subheader("Suspicious Transaction Detection")

    if txn_file is not None:
        txn_df = pd.read_csv(txn_file)
        st.success(f"Uploaded {len(txn_df)} transaction records.")
    elif run_demo:
        _, txn_df = load_demo_data()
        st.info("Running sample transaction dataset.")
    else:
        st.info("Please upload a Transaction CSV file or click 'Run Sample Data'.")
        st.stop()

    # Run detection
    txn_alerts = detect_suspicious_transactions(txn_df)
    alert_df = pd.DataFrame(txn_alerts)

    # Sample data
    st.write("### Sample Transaction Data")
    st.dataframe(txn_df.head())

    # Visualizations
    st.write("### 📈 Transaction Pattern Visualizations")

    # Transaction amounts
    fig4, ax4 = plt.subplots()
    ax4.hist(txn_df["txn_amount"], bins=15)
    ax4.set_title("Transaction Amount Distribution")
    ax4.set_xlabel("Amount")
    ax4.set_ylabel("Frequency")
    st.pyplot(fig4)

    # Frequency last 24 hours
    fig5, ax5 = plt.subplots()
    ax5.hist(txn_df["txn_count_last_24h"], bins=10)
    ax5.set_title("Transaction Count Last 24h")
    ax5.set_xlabel("Count")
    ax5.set_ylabel("Frequency")
    st.pyplot(fig5)

    # Average txn amount
    fig6, ax6 = plt.subplots()
    ax6.hist(txn_df["avg_txn_amount"], bins=10)
    ax6.set_title("Average Transaction Amount Distribution")
    ax6.set_xlabel("Average Amount")
    ax6.set_ylabel("Frequency")
    st.pyplot(fig6)

    # Alerts
    st.write("### 🚨 Detected Suspicious Transactions")
    st.dataframe(alert_df)

    st.download_button(
        label="⬇️ Download Transaction Alerts",
        data=alert_df.to_csv(index=False).encode("utf-8"),
        file_name="transaction_alerts.csv",
        mime="text/csv"
    )

    st.info(f"Running in {mode} Mode")

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("© 2025 CAD-EWS | Credit & Deposit Early Warning System | Built with ❤️ using Streamlit")

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
