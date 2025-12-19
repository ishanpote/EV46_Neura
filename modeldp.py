import streamlit as st
import joblib
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="AIGuard | Grey Market Command Center",
    page_icon="🛡️",
    layout="wide"
)


st.markdown("""
    <style>
    /* Main App Background */
    .stApp { background-color: #0e1117; }
    
    /* Metric Card Container Styling */
    [data-testid="stMetric"] {
        background-color: #1e293b; 
        border: 1px solid #334155;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    /* Force high contrast for labels and values */
    [data-testid="stMetricLabel"] > div { 
        color: #94a3b8 !important; 
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricValue"] > div { 
        color: #ffffff !important; 
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    /* Style headers for the dark theme */
    h1, h2, h3 { color: #f8fafc !important; }
    p { color: #cbd5e1 !important; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_assets():
    return joblib.load('grey_market_detector_v1.joblib')

try:
    detector = load_assets()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

with st.sidebar:
    st.markdown("### 🛡️ AIGuard Control Panel")
    st.markdown("---")
    
    st.header("🛒 Live Feed Input")
    sku_name = st.text_input("Product Identifier", "VINTAGE PAISLEY DINNER TRAY")
    
    col_a, col_b = st.columns(2)
    with col_a:
        unit_price = st.number_input("Unit Price ($)", value=4.50, step=0.1)
        msrp = st.number_input("MSRP ($)", value=12.95, step=0.1)
    with col_b:
        quantity = st.number_input("Qty", value=1200, min_value=1)
    
    st.markdown("---")
    run_scan = st.button("🔍 Run Forensic Scan", use_container_width=True, type="primary")


st.title("⚖️ Grey Market Forensic Intelligence")
st.markdown(f"Analysis of trade diversion and price erosion for: **{sku_name}**")

if run_scan:
    pvi = (unit_price - msrp) / msrp
    pvi_pct = pvi * 100
    
    input_df = pd.DataFrame([[pvi, quantity, unit_price]], 
                             columns=['PVI', 'Quantity', 'UnitPrice'])
    
    is_anomaly = detector.predict(input_df)[0]
    raw_score = detector.decision_function(input_df)[0]

    stat1, stat2, stat3 = st.columns(3)
    stat1.metric("Price Variance", f"{pvi_pct:.1f}%", delta=f"{pvi_pct:.1f}%", delta_color="inverse")
    stat2.metric("Anomaly Score", f"{raw_score:.3f}")
    stat3.metric("Volume Scale", f"{quantity:,} Units")

    st.markdown("---")

    res_col, act_col = st.columns([2, 1])

    with res_col:
        if is_anomaly == -1:
            st.error("### 🚨 HIGH RISK: SUSPICIOUS TRADE DETECTED")
            st.warning(f"""
            **Forensic AI Insight:**
            This transaction deviates **{abs(pvi_pct):.1f}%** from MSRP with a bulk quantity of **{quantity:,}**.
            This represents a mathematical outlier at the **3-Sigma** threshold.
            """)
        else:
            st.success("### ✅ LOW RISK: AUTHORIZED TRANSACTION")
            st.info("Current behavior is consistent with established retail distribution patterns.")

    with act_col:
        st.subheader("Action Center")
        if is_anomaly == -1:
            st.button("📦 HOLD SHIPMENT", use_container_width=True)
            st.button("📧 ALERT DISTRIBUTOR", use_container_width=True)
            
            report_csv = input_df.to_csv().encode('utf-8')
            st.download_button("📂 DOWNLOAD AUDIT LOG", data=report_csv, 
                               file_name=f"alert_{sku_name}.csv", mime="text/csv", 
                               use_container_width=True)
        else:
            st.button("🚛 APPROVE LOGISTICS", use_container_width=True)

else:
    st.info("Adjust transaction parameters in the sidebar and click 'Run Forensic Scan' to evaluate risk.")