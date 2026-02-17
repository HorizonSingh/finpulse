import streamlit as st
import pandas as pd
from google import genai  # Correct import for the new 2026 SDK
from google.genai import types
import os
from datetime import datetime

# --- CONFIGURATION ---
# Using the key you provided
API_KEY = "AIzaSyD547fs3nuTNbj44SkM4Jyprk-DXylOxzQ"
client = genai.Client(api_key=API_KEY)

st.set_page_config(
    page_title="FinPulse Prime", 
    page_icon="💸", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- STYLING ---
st.markdown("""
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 10%, #1a4d2e 0%, #000000 70%);
        color: white;
    }
    div[data-baseweb="tab-list"] {
        justify-content: center;
        background-color: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 50px;
        width: 60%;
        margin: 0 auto;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    button[data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        color: #aaaaaa;
        font-weight: 500;
        border-radius: 30px;
        padding: 0px 25px;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #00E676 !important;
        color: black !important;
        font-weight: 800;
        box-shadow: 0px 0px 20px rgba(0, 230, 118, 0.6);
    }
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px;
        border-radius: 15px;
        text-align: center;
    }
    div[data-testid="stMetricValue"] {
        color: #00E676 !important;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #00C853 0%, #00E676 100%);
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 12px;
        height: 50px;
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC FUNCTIONS ---
def load_data():
    try:
        path = "bank_transactions.csv" if os.path.exists("bank_transactions.csv") else "FinPulse/bank_transactions.csv"
        df = pd.read_csv(path)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.sort_values(by='Date', ascending=False)
        df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')
        return df
    except Exception:
        # Fallback dummy data if file is missing
        data = {
            'Customer_Name': ['Aman Sharma', 'Priya Iyer'],
            'Amount': [60000, 4500],
            'Category': ['Salary', 'Shopping'],
            'Transaction_Description': ['Tech Corp Credit', 'Amazon India'],
            'Transaction_Type': ['Credit', 'Debit'],
            'Date': ['18-02-2026', '17-02-2026']
        }
        return pd.DataFrame(data)

def save_log(customer, amount, txn_type, status):
    log_file = "app_logs.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({
        "Timestamp": [timestamp],
        "Customer": [customer],
        "Amount": [amount],
        "Type": [txn_type],
        "Status": [status]
    })
    if not os.path.isfile(log_file):
        new_data.to_csv(log_file, index=False)
    else:
        new_data.to_csv(log_file, mode='a', header=False, index=False)

def generate_offer(customer, amount, description, txn_type):
    try:
        goal = "Suggest Investment" if txn_type == "Credit" else "Cross-sell Credit Card"
        # New SDK Syntax: client.models.generate_content
        response = client.models.generate_content(
            model='gemini-2.0-flash', 
            contents=f"You are FinPulse banking AI. {customer} did a {txn_type} of ₹{amount} for {description}. Task: {goal}. One short WhatsApp sentence + 1 emoji."
        )
        return response.text
    except Exception as e:
        return f"System Error: {str(e)}"

# --- UI LAYOUT ---
st.markdown("<h1 style='text-align: center;'>💸 FinPulse <span style='color:#00E676'>Prime</span></h1>", unsafe_allow_html=True)

tab_home, tab_logs = st.tabs(["🏠 Live Operations", "📜 Audit Logs"])

with tab_home:
    df = load_data()
    if not df.empty:
        # Show Metrics
        c1, c2, c3 = st.columns(3)
        c1.metric("📉 Spends", f"₹{df[df['Transaction_Type']=='Debit']['Amount'].sum():,}")
        c2.metric("📈 Income", f"₹{df[df['Transaction_Type']=='Credit']['Amount'].sum():,}")
        c3.metric("👥 Active Users", f"{df['Customer_Name'].nunique()}")
        
        st.markdown("---")
        col_table, col_action = st.columns([2, 1])
        
        with col_table:
            st.markdown("### 📡 Transaction Stream")
            st.dataframe(df, use_container_width=True)
        
        with col_action:
            st.markdown("### ⚡ Command Center")
            idx = st.number_input("Select Transaction ID:", min_value=0, max_value=len(df)-1, step=1)
            
            if st.button("🚀 DEPLOY AI AGENT"):
                row = df.iloc[idx]
                with st.status("Analyzing with Gemini 2.0..."):
                    msg = generate_offer(row['Customer_Name'], row['Amount'], row['Transaction_Description'], row['Transaction_Type'])
                    save_log(row['Customer_Name'], row['Amount'], row['Transaction_Type'], "✅ Deployed")
                
                st.balloons()
                st.info(f"**SENT TO {row['Customer_Name']}:**\n\n{msg}")

with tab_logs:
    if os.path.exists("app_logs.csv"):
        st.dataframe(pd.read_csv("app_logs.csv").iloc[::-1], use_container_width=True)
    else:
        st.info("No activity logs yet.")

st.markdown('<div style="text-align:center; color:#888; padding:20px;">🔒 FinPulse Prime © 2026 | Powered by Unified GenAI SDK</div>', unsafe_allow_html=True)


