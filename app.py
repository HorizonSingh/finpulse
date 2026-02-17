import streamlit as st
import pandas as pd
from openai import OpenAI
import time
from datetime import datetime
import os

# --- CONFIGURATION ---
# Get your key at https://openrouter.ai/keys
OPENROUTER_API_KEY = "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"

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

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
        background: radial-gradient(circle at 50% 10%, #001f3f 0%, #000000 70%);
        color: white;
    }
    div[data-testid="stMetricValue"] {
        color: #00E676 !important;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #0074D9 0%, #00E676 100%);
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIC FUNCTIONS ---
def generate_offer(customer, amount, description, txn_type):
    goal = "High-Yield Savings" if txn_type == "Credit" else "Travel Rewards Card"
    
    try:
        response = client.chat.completions.create(
            # Choose any model: "openai/gpt-4o", "anthropic/claude-3-haiku", etc.
            model="google/gemini-2.0-flash-001", 
            extra_headers={
                "HTTP-Referer": "https://finpulse.streamlit.app", # Optional
                "X-Title": "FinPulse Prime", # Optional
            },
            messages=[
                {"role": "system", "content": "You are FinPulse AI. Write a 15-word banking offer with 1 emoji."},
                {"role": "user", "content": f"{customer} spent ₹{amount} on {description}. {goal}."}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenRouter Error: {str(e)}"

# --- UI (Simplified for brevity) ---
st.title("💸 FinPulse Prime")
st.caption("Universal AI Gateway via OpenRouter")

# Sample Data Loader
df = pd.DataFrame({
    'Customer': ['Rohan Das', 'Ananya S.'],
    'Amount': [52000, 1200],
    'Type': ['Credit', 'Debit'],
    'Desc': ['Salary', 'Uber']
})

st.dataframe(df, use_container_width=True)

if st.button("🚀 RUN AI AGENT"):
    with st.status("Routing through OpenRouter...", expanded=True):
        row = df.iloc[0]
        offer = generate_offer(row['Customer'], row['Amount'], row['Desc'], row['Type'])
        st.success(f"**Offer for {row['Customer']}:** {offer}")
