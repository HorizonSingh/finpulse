import streamlit as st
import pandas as pd
import google.generativeai as genai
import time
from datetime import datetime
import os

GENAI_API_KEY = "AIzaSyCJhCUQg6y-VrYoukgaw6K5luHoLV93TxU"
genai.configure(api_key=GENAI_API_KEY)

st.set_page_config(
    page_title="FinPulse Prime", 
    page_icon="💸", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-bottom: 0px;'>💸 FinPulse <span style='color:#00E676'>Prime</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Next-Gen Autonomous Banking Interface</p>", unsafe_allow_html=True)
st.write("")

tab_home, tab_analytics, tab_history = st.tabs([
    "🏠 Live Operations", 
    "📈 Market Insights", 
    "📜 Real-Time Audit Logs"
])

def load_data():
    try:
        df = pd.read_csv("FinPulse/bank_transactions.csv")
        
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.sort_values(by='Date', ascending=False)
        df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')
        
        return df
    except FileNotFoundError:
        st.error("⚠️ Data file missing.")
        return pd.DataFrame()

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

def generate_offer(customer, amount, category, description, txn_type):
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    if txn_type == "Credit":
        goal = "Suggest Investment (FD/Mutual Fund) since money just came in."
    else:
        goal = "Cross-sell a relevant product (Credit Card/Loan) based on spending."

    prompt = f"""
    You are 'FinPulse', an elite banking AI.
    Context: Customer {customer} just did a '{txn_type}' of ₹{amount} for {description} ({category}).
    Goal: {goal}
    Tone: Short, punchy WhatsApp notification. Use emojis. No robotic intros.
    """
    response = model.generate_content(prompt)
    return response.text

with tab_home:
    st.write("")
    df = load_data()
    
    if not df.empty:
        total_spend = df[df['Transaction_Type'] == 'Debit']['Amount'].sum()
        total_income = df[df['Transaction_Type'] == 'Credit']['Amount'].sum()
        active_users = df['Customer_Name'].nunique()
        high_value_count = df[(df['Amount'] > 5000) & (df['Transaction_Type'] == 'Debit')].shape[0]
    else:
        total_spend, total_income, active_users, high_value_count = 0, 0, 0, 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📉 Total Spends", f"₹{total_spend:,}", "Debit")
    c2.metric("📈 Total Income", f"₹{total_income:,}", "Credit")
    c3.metric("👥 Active Users", f"{active_users}", "+New")
    c4.metric("💎 High Value Targets", f"{high_value_count}", "Priority Leads")
    
    st.markdown("---")
    
    if not df.empty:
        col_table, col_action = st.columns([1.5, 1])
        
        with col_table:
            st.markdown("### 📡 Live Transaction Stream")
            st.dataframe(df, use_container_width=True, height=400)
        
        with col_action:
            with st.container():
                st.markdown("""
                <div style="background-color: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid #333;">
                    <h3 style="color: white; margin-top:0;">⚡ Command Center</h3>
                    <p style="color: #888;">Select a target to deploy AI Agent.</p>
                </div>
                """, unsafe_allow_html=True)
                
                max_val = len(df)-1 if len(df) > 0 else 0
                idx = st.number_input("Select Transaction ID:", min_value=0, max_value=max_val, step=1)
                
                if st.button("🚀 DEPLOY AGENT"):
                    if not df.empty:
                        row = df.iloc[idx]
                        
                        progress_text = "Initializing Neural Engine..."
                        my_bar = st.progress(0, text=progress_text)
                        for percent_complete in range(100):
                            time.sleep(0.01)
                            my_bar.progress(percent_complete + 1, text="Analyzing Spending Patterns...")
                        
                        msg = generate_offer(
                            row['Customer_Name'], row['Amount'], row['Category'], 
                            row['Transaction_Description'], row['Transaction_Type']
                        )
                        my_bar.empty()
                        
                        save_log(row['Customer_Name'], row['Amount'], row['Transaction_Type'], "✅ Offer Sent")
                        
                        st.balloons()
                        st.toast(f"Offer Deployed to {row['Customer_Name']}", icon="✅")
                        
                        st.markdown(f"""
                        <div style="background-color: #0d1f14; border-left: 5px solid #00E676; padding: 15px; margin-top: 10px; border-radius: 5px;">
                            <p style="color: #00E676; font-size: 12px; font-weight: bold;">GENERATED OUTPUT</p>
                            <p style="font-size: 16px;">{msg}</p>
                            <p style="color: #555; font-size: 12px; margin-bottom: 0;">Target: {row['Customer_Name']}</p>
                        </div>
                        """, unsafe_allow_html=True)


with tab_history:
    st.write("")
    st.markdown("### 🔐 Encrypted System Logs")
    
    if os.path.isfile("app_logs.csv"):
        try:
            logs_df = pd.read_csv("app_logs.csv")
            
            if not logs_df.empty:
                logs_df = logs_df.iloc[::-1]
                st.dataframe(logs_df, use_container_width=True)
            else:
                st.info("ℹ️ Log file created but empty. Deploy an agent to record data.")
                
        except pd.errors.EmptyDataError:
            st.warning("⚠️ Log file is empty. Please delete 'app_logs.csv' and restart.")
            
    else:
        st.info("ℹ️ System initialized. Waiting for first deployment...")
        st.code("[System] Logs database created... Ready for operations.", language="bash")


st.write("")
st.write("")
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #000000;
        color: #888;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #333;
        z-index: 100;
    }
    </style>
    
    <div class="footer">
        <p style="margin: 0;">
            🔒 <b>FinPulse Prime</b> &copy; 2024 | 
            <span style="color: #00E676;">● System Status: Stable</span> | 
            Built for <b>InnovGenius Hackathon</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

