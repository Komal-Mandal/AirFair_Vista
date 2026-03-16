import streamlit as st
import pickle
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# -------------------------
# 1. Page Configuration & Model Loading
# -------------------------
st.set_page_config(page_title="Flight Price Predictor", page_icon="✈️", layout="centered")

@st.cache_resource
def load_model():
    # Ensure xgboost_model.pkl is in the same folder as this script
    return pickle.load(open("xgboost_model.pkl", "rb"))

try:
    model = load_model()
except FileNotFoundError:
    st.error("🚨 Error: 'xgboost_model.pkl' not found. Please upload the model file.")
    st.stop()

# -------------------------
# 2. User Interface
# -------------------------
st.title("✈️ Flight Price Prediction")
st.markdown("Estimate your ticket price using machine learning.")
st.divider()

col1, col2 = st.columns(2)

with col1:
    dep_time = st.datetime_input("Departure Time", value=datetime.now())
    source = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
    total_stops = st.selectbox("Total Stops", [0, 1, 2, 3, 4])

with col2:
    # Default arrival is set to 2 hours after departure to avoid instant errors
    arr_time = st.datetime_input("Arrival Time", value=dep_time + timedelta(hours=2))
    destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'New_Delhi', 'Hyderabad', 'Kolkata'])
    airline = st.selectbox(
        "Airline",
        [
            'Jet Airways', 'IndiGo', 'Air India', 'Multiple carriers', 
            'SpiceJet', 'Vistara', 'GoAir', 'Multiple carriers Premium economy',
            'Jet Airways Business', 'Vistara Premium economy', 'Trujet'
        ]
    )

# -------------------------
# 3. Time Logic & Duration Validation
# -------------------------
duration = arr_time - dep_time
duration_seconds = duration.total_seconds()

if duration_seconds < 0:
    st.error("❌ **Error:** Arrival time cannot be earlier than Departure time. Please check the dates.")
    st.stop()

dur_hour = int(duration_seconds // 3600)
dur_min = int((duration_seconds % 3600) // 60)

st.info(f"⏱️ **Flight Duration:** {dur_hour} hours, {dur_min} minutes")

# -------------------------
# 4. Feature Engineering
# -------------------------
# Extracting Date/Time components
journey_day = dep_time.day
journey_month = dep_time.month
dep_hour = dep_time.hour
dep_min = dep_time.minute
arrival_hour = arr_time.hour
arrival_min = arr_time.minute

# Helper function for One-Hot Encoding
def get_encoded_list(selected_value, categories):
    return [1 if selected_value == cat else 0 for cat in categories]

# Define category lists (MUST MATCH THE ORDER YOUR MODEL WAS TRAINED ON)
airlines_list = [
    'Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
    'Multiple carriers', 'Multiple carriers Premium economy', 'SpiceJet',
    'Trujet', 'Vistara', 'Vistara Premium economy'
]
sources_list = ['Chennai', 'Delhi', 'Kolkata', 'Mumbai']
dest_list = ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New_Delhi']

# Encode the inputs
airline_encoded = get_encoded_list(airline, airlines_list)
source_encoded = get_encoded_list(source, sources_list)
dest_encoded = get_encoded_list(destination, dest_list)

# -------------------------
# 5. Prediction
# -------------------------
if st.button("Predict Ticket Price 💰", use_container_width=True):
    try:
        # Construct the feature vector in the exact order the model expects
        # 1. Numerical Features
        features_numeric = [
            total_stops, journey_day, journey_month, 
            dep_hour, dep_min, arrival_hour, arrival_min, 
            dur_hour, dur_min
        ]
        
        # 2. Concatenate all features (Numeric + Encoded Categoricals)
        final_features = np.array([features_numeric + airline_encoded + source_encoded + dest_encoded])

        # Predict
        prediction = model.predict(final_features)
        
        # Reversing Log Transformation (if applicable, which is common in flight price datasets)
        # If your model predicts actual price directly, remove np.exp()
        final_price = round(np.exp(prediction[0]))

        st.success(f"### 💸 Estimated Price: ₹ {final_price:,}")
        st.balloons()
        
    except Exception as e:
        st.error("An error occurred during prediction. Please verify feature shapes.")
        st.write(f"Error Details: {e}")

st.divider()
st.caption("Note: Prices are estimated based on historical data patterns.")