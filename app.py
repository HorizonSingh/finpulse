import streamlit as st
import pandas as pd
from google import genai  # Unified SDK import
import os

# --- NEW CONFIGURATION (Unified SDK Style) ---
GEMINI_API_KEY = "AIzaSyCJhCUQg6y-VrYoukgaw6K5luHoLV93TxU"
# All configuration now happens inside the Client
client = genai.Client(api_key=GEMINI_API_KEY)

st.set_page_config(page_title="FinPulse Prime", page_icon="💸", layout="wide")

# (Styling remains the same...)

def generate_offer(customer, amount, category, description, txn_type):
    try:
        # In the new SDK, GenerativeModel is replaced by client.models.generate_content
        response = client.models.generate_content(
            model='gemini-2.0-flash', # Optimized for speed
            contents=f"Customer {customer} made a {txn_type} of ₹{amount} for {description}. Write a 1-sentence bank offer with 1 emoji."
        )
        return response.text
    except Exception as e:
        return f"System Error: {str(e)}"

# --- MAIN UI ---
st.title("💸 FinPulse Prime")
# Sample data for demo
df = pd.DataFrame({'Customer': ['Aman'], 'Amount': [5000], 'Type': ['Credit'], 'Desc': ['Salary']})

st.dataframe(df)

if st.button("🚀 DEPLOY AGENT"):
    row = df.iloc[0]
    with st.status("Neural Routing Active..."):
        offer = generate_offer(row['Customer'], row['Amount'], 'Salary', row['Desc'], row['Type'])
        st.success(offer)
