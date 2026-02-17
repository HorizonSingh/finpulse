import streamlit as st
import pandas as pd
from openai import OpenAI
import time
from datetime import datetime
import os

# --- CONFIGURATION ---
# It is best practice to use st.secrets["OPENAI_API_KEY"] for deployment
OPENAI_API_KEY = "sk-ZD8gB0MTEd2wpDdaQHVbO8HNArUI71W6nrxd0rstkWCaDLnp" 
client = OpenAI(api_key=OPENAI_API_KEY)

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
        path = "bank_transactions.csv" if not os.path.exists("FinPulse/bank_transactions.csv") else "FinPulse/bank_transactions.csv"
        df = pd.read_csv(path)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.sort_values(by='Date', ascending=False)
        df['Date'] = df['Date'].dt.strftime('%d-%m-%Y')
        return df
    except Exception:
        # Fallback dummy data
        data = {
            'Customer_Name': ['Aman Sharma', 'Priya Iyer'],
            'Amount': [60000, 4500],
            'Category': ['Salary', 'Shopping'],
            'Transaction_Description': ['Monthly Pay', 'Amazon India'],
            'Transaction_Type': ['Credit', 'Debit'],
            'Date': ['17-02-2026', '16-02-2026']
        }
        return pd.DataFrame(data)

def save_log(customer, amount, txn_type, status):
    log_file = "app_logs.csv"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_data = pd.DataFrame({"Timestamp": [timestamp], "Customer": [customer], "Amount": [amount], "Type": [txn_type], "Status": [status]})
    if not os.path.isfile(log_file):
        new_data.to_csv(log_file, index=False)
    else:
        new_data.to_csv(log_file, mode='a', header=False, index=False)

def generate_offer(customer, amount, category, description, txn_type):
    goal = "Invest in High-Yield FD" if txn_type == "Credit" else "Upgrade to Platinum Credit Card"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Cost-effective and fast
            messages=[
                {"role": "system", "content": "You are FinPulse, a premium AI banking assistant. Write short, punchy WhatsApp-style offers."},
                {"role": "user", "content": f"Customer {customer} made a {txn_type} of ₹{amount} for {description}. {goal}. Keep it under 20 words with 1 emoji."}
            ],
            max_tokens=50
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI Logic Offline: {str(e)}"

# --- UI LAYOUT ---
st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-bottom: 0px;'>💸 FinPulse <span style='color:#00E676'>Prime</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Autonomous Banking powered by OpenAI</p>", unsafe_allow_html=True)

tab_home, tab_analytics, tab_history = st.tabs(["🏠 Live Operations", "📈 Market Insights", "📜 Real-Time Audit Logs"])

with tab_home:
    df = load_data()
    if not df.empty:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("📉 Total Spends", f"₹{df[df['Transaction_Type']=='Debit']['Amount'].sum():,}")
        c2.metric("📈 Total Income", f"₹{df[df['Transaction_Type']=='Credit']['Amount'].sum():,}")
        c3.metric("👥 Active Users", f"{df['Customer_Name'].nunique()}")
        c4.metric("💎 High Value", f"{df[df['Amount'] > 5000].shape[0]}")
        
        st.markdown("---")
        col_table, col_action = st.columns([1.5, 1])
        
        with col_table:
            st.markdown("### 📡 Live Transaction Stream")
            st.dataframe(df, use_container_width=True, height=400)
        
        with col_action:
            st.markdown('<div style="background-color:rgba(255,255,255,0.05);padding:15px;border-radius:15px;"><h3>⚡ Command Center</h3></div>', unsafe_allow_html=True)
            idx = st.number_input("Select Row Index:", min_value=0, max_value=len(df)-1, step=1)
            
            if st.button("🚀 DEPLOY AGENT"):
                row = df.iloc[idx]
                with st.status("GPT-4o Analyzing Patterns...", expanded=True) as status:
                    msg = generate_offer(row['Customer_Name'], row['Amount'], row['Category'], row['Transaction_Description'], row['Transaction_Type'])
                    save_log(row['Customer_Name'], row['Amount'], row['Transaction_Type'], "✅ Deployed")
                    status.update(label="Campaign Strategy Generated!", state="complete")
                
                st.balloons()
                st.markdown(f"""
                    <div style="background:#0d1f14; border-left:5px solid #00E676; padding:15px; border-radius:5px;">
                        <p style="color:#00E676; font-weight:bold; font-size:12px;">SENT TO {row['Customer_Name']}</p>
                        <p>{msg}</p>
                    </div>
                """, unsafe_allow_html=True)

with tab_history:
    if os.path.exists("app_logs.csv"):
        st.dataframe(pd.read_csv("app_logs.csv").iloc[::-1], use_container_width=True)
    else:
        st.info("Log database empty. Run an agent deployment first.")

st.markdown('<div style="position:fixed;bottom:0;left:0;width:100%;background:#000;color:#888;text-align:center;padding:10px;border-top:1px solid #333;">🔒 FinPulse Prime | Powered by OpenAI GPT-4o</div>', unsafe_allow_html=True)


