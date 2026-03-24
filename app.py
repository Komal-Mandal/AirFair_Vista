
import streamlit as st
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# -------------------------
# 1. UI & Styling
# -------------------------
st.set_page_config(page_title="Flight Price Intelligence", page_icon="✈️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stVerticalBlock"] > div:has(div.stSelectbox) {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px; border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        color: white; border: none; padding: 15px;
        font-size: 1.2rem; font-weight: bold; border-radius: 12px;
        transition: 0.3s; width: 100%; margin-top: 20px;
    }
    .price-card {
        background: linear-gradient(180deg, rgba(99, 102, 241, 0.1) 0%, rgba(11, 14, 20, 0) 100%);
        padding: 40px; border-radius: 20px;
        text-align: center; border: 1px solid rgba(99, 102, 241, 0.2);
    }
    .price-value { font-size: 4rem; font-weight: 800; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return pickle.load(open("xgboost_model.pkl", "rb"))

try:
    model = load_model()
except Exception as e:
    st.error(f"🚨 Model loading failed: {e}")
    st.stop()

# -------------------------
# 2. Input Section & Time Logic
# -------------------------
st.title("✈️ Flight Price Intelligence")
st.divider()

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("#### 📍 Route")
    source = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
    destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'New_Delhi', 'Hyderabad', 'Kolkata'])
    airline = st.selectbox("Airline", [
        'Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
        'Multiple carriers', 'Multiple carriers Premium economy', 'SpiceJet',
        'Trujet', 'Vistara', 'Vistara Premium economy'
    ])

with col2:
    st.markdown("#### 🕒 Schedule")
    dep_time = st.datetime_input("Departure Time", value=datetime.now())
    # Arrival defaults to 2 hours later
    arr_time = st.datetime_input("Arrival Time", value=dep_time + timedelta(hours=2))
    total_stops = st.select_slider("Total Stops", options=[0, 1, 2, 3, 4])

# --- Duration Calculation ---
duration = arr_time - dep_time
duration_seconds = duration.total_seconds()

if duration_seconds < 0:
    st.error("❌ **Error:** Arrival cannot be before Departure.")
    st.stop()

dur_hour = int(duration_seconds // 3600)
dur_min = int((duration_seconds % 3600) // 60)

st.info(f"⏱️ **Flight Duration:** {dur_hour} hours, {dur_min} minutes")

# -------------------------
# 3. Prediction Execution
# -------------------------
if st.button("Calculate Best Fare"):
    # Fix for the NameError: Define time components explicitly
    dep_hour = dep_time.hour
    dep_min = dep_time.minute
    arrival_hour = arr_time.hour
    arrival_min = arr_time.minute
    journey_day = dep_time.day
    journey_month = dep_time.month

    # Encoding Logic
    def get_enc(val, cats): return [1 if val == cat else 0 for cat in cats]
    
    airlines_list = [
        'Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
        'Multiple carriers', 'Multiple carriers Premium economy', 'SpiceJet',
        'Trujet', 'Vistara', 'Vistara Premium economy'
    ]
    sources_list = ['Chennai', 'Delhi', 'Kolkata', 'Mumbai']
    dest_list = ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New_Delhi']

    airline_enc = get_enc(airline, airlines_list)
    source_enc = get_enc(source, sources_list)
    dest_enc = get_enc(destination, dest_list)
    
    # Corrected Feature Vector (Must match model training order)
    features_numeric = [
        total_stops, journey_day, journey_month, 
        dep_hour, dep_min, arrival_hour, arrival_min, 
        dur_hour, dur_min
    ]
    
    final_features = np.array([features_numeric + airline_enc + source_enc + dest_enc])

    try:
        prediction = model.predict(final_features)
        # Reverse Log Transformation
        final_price = round(np.exp(prediction[0]))

        st.divider()
        res_col1, res_col2 = st.columns([1.2, 1])

        with res_col1:
            st.markdown(f"""
                <div class="price-card">
                    <p style="color: #6366f1; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Estimated Fare</p>
                    <h1 class="price-value">₹ {final_price:,}</h1>
                    <p style="color: #94a3b8;">{airline} • {source} to {destination}</p>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()

        with res_col2:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = final_price,
                gauge = {
                    'axis': {'range': [None, 30000]},
                    'bar': {'color': "#6366f1"},
                    'steps': [
                        {'range': [0, 8000], 'color': "rgba(0, 255, 0, 0.1)"},
                        {'range': [8000, 18000], 'color': "rgba(255, 255, 0, 0.1)"},
                        {'range': [18000, 30000], 'color': "rgba(255, 0, 0, 0.1)"}
                    ],
                }
            ))
            fig.update_layout(height=280, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(t=50, b=0))
            st.plotly_chart(fig, use_container_width=True)
            
    except Exception as e:
        st.error(f"Prediction Error: {e}")
        st.write("Ensure your model expects 29 features in this specific order.")