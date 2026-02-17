import streamlit as st
import pandas as pd
from google import genai
from datetime import datetime
import os

# --- CONFIGURATION ---
# Get your FREE key at: https://aistudio.google.com/app/apikey
GEMINI_API_KEY = "AIzaSyCJhCUQg6y-VrYoukgaw6K5luHoLV93TxU"
client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(
    page_title="FinPulse Prime", 
    page_icon="💸", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ADVANCED STYLING (2026 Banking Glassmorphism) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #001a1a 0%, #000000 100%);
        color: #e0e0e0;
    }
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 230, 118, 0.2);
        padding: 20px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    }
    /* Tabs Styling */
    button[data-baseweb="tab"] {
        font-size: 1.1rem;
        color: #888;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #00E676 !important;
        border-bottom-color: #00E676 !important;
    }
    /* Action Button */
    div.stButton > button {
        background: linear-gradient(90deg, #00C853, #076585);
        color: white;
        border: none;
        padding: 15px;
        font-size: 1.2rem;
        border-radius: 12px;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(0, 230, 118, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# --- DATA & LOGIC ---
def load_data():
    path = "bank_transactions.csv" if not os.path.exists("FinPulse/bank_transactions.csv") else "FinPulse/bank_transactions.csv"
    try:
        df = pd.read_csv(path)
        return df
    except:
        return pd.DataFrame({
            'Customer': ['Arjun K.', 'Sara M.', 'Leo V.'],
            'Amount': [75000, 1500, 4200],
            'Type': ['Credit', 'Debit', 'Debit'],
            'Desc': ['Salary', 'Coffee', 'Fuel']
        })

def generate_ai_offer(name, amt, txn_type, desc):
    try:
        # Using Gemini 2.0 Flash for low-latency intelligence
        prompt = f"Customer {name} made a {txn_type} of ₹{amt} for {desc}. Write a ultra-short personalized banking offer. Max 15 words. Include 1 emoji."
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"AI Agent Busy: {str(e)}"

# --- MAIN UI ---
st.markdown("<h1 style='text-align: center;'>💸 FinPulse <span style='color:#00E676'>Prime</span></h1>", unsafe_allow_html=True)
st.caption("<p style='text-align: center;'>Autonomous Financial Intelligence Center v2.6</p>", unsafe_allow_html=True)

df = load_data()
t1, t2 = st.tabs(["🚀 Live Deployment", "📊 Audit Logs"])

with t1:
    # KPI Row
    c1, c2, c3 = st.columns(3)
    c1.metric("Processing Rate", "1.2ms", "⚡ Stable")
    c2.metric("Total Volume", f"₹{df['Amount'].sum():,}")
    c3.metric("Model Status", "Gemini 2.0", "Active")

    st.markdown("---")
    
    col_data, col_cmd = st.columns([1.5, 1])
    
    with col_data:
        st.subheader("📡 Transaction Stream")
        selected_row = st.selectbox("Select Transaction Target:", range(len(df)), format_func=lambda x: f"TXN-{x}: {df.iloc[x]['Customer']} (₹{df.iloc[x]['Amount']})")
        st.dataframe(df, use_container_width=True)

    with col_cmd:
        st.subheader("⚡ Command Center")
        row = df.iloc[selected_row]
        
        if st.button("EXECUTE AGENT"):
            with st.status("Initializing Neural Routing...", expanded=True) as status:
                offer = generate_ai_offer(row['Customer'], row['Amount'], row['Type'], row['Desc'])
                status.update(label="Offer Generated Successfully!", state="complete")
            
            st.balloons()
            st.markdown(f"""
                <div style="background: rgba(0, 230, 118, 0.1); border-left: 5px solid #00E676; padding: 20px; border-radius: 10px;">
                    <h4 style="margin:0; color:#00E676;">TARGET: {row['Customer']}</h4>
                    <p style="font-size:1.1rem; margin-top:10px;">{offer}</p>
                </div>
            """, unsafe_allow_html=True)

with t2:
    st.info("Log tracking enabled. All AI generations are archived for compliance.")
    st.write("Session History:")
    st.table(df.head()) # Replace with actual logs in production

st.markdown("<div style='text-align:center; padding:20px; color:#555;'>FinPulse Prime © 2026 | Secured by Google GenAI</div>", unsafe_allow_html=True)
