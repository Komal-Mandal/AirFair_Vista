# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
# import plotly.graph_objects as go
# from datetime import datetime, timedelta

# # -------------------------
# # 1. PAGE CONFIG & STYLING
# # -------------------------
# st.set_page_config(page_title="Flight Price Intelligence", page_icon="✈️", layout="wide")

# st.markdown("""
# <style>
# .main { background-color: #0e1117; color: white; }
# div.stButton > button:first-child {
#     background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
#     color: white; border: none; padding: 15px;
#     font-size: 1.2rem; font-weight: bold; border-radius: 12px;
#     width: 100%; margin-top: 20px;
# }
# .price-card {
#     background: linear-gradient(180deg, rgba(99, 102, 241, 0.1) 0%, rgba(11, 14, 20, 0) 100%);
#     padding: 40px; border-radius: 20px;
#     text-align: center; border: 1px solid rgba(99, 102, 241, 0.2);
# }
# .price-value { font-size: 4rem; font-weight: 800; color: #ffffff; }
# </style>
# """, unsafe_allow_html=True)

# # -------------------------
# # 2. LOAD MODEL & COLUMNS
# # -------------------------
# @st.cache_resource
# def load_model():
#     return joblib.load("xgboost_model.pkl")  # This file must contain {"model": xgb, "columns": X.columns.tolist()}

# try:
#     model_data = load_model()
#     model = model_data["model"]
#     model_columns = model_data["columns"]
# except Exception as e:
#     st.error(f"🚨 Model loading failed: {e}")
#     st.stop()

# # -------------------------
# # 3. STREAMLIT UI
# # -------------------------
# st.title("✈️ Flight Price Intelligence")
# st.caption("Smart AI-based flight fare prediction system")
# st.divider()

# col1, col2 = st.columns(2, gap="large")

# with col1:
#     st.markdown("#### 📍 Route")
#     source = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
#     destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
#     airline = st.selectbox("Airline", [
#         'Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
#         'Multiple carriers', 'Multiple carriers Premium economy', 'SpiceJet',
#         'Trujet', 'Vistara', 'Vistara Premium economy'
#     ])

# with col2:
#     st.markdown("#### 🕒 Schedule")
#     dep_time = st.datetime_input("Departure Time", value=datetime.now())
#     arr_time = st.datetime_input("Arrival Time", value=dep_time + timedelta(hours=2))
#     total_stops = st.select_slider("Total Stops", options=[0,1,2,3,4])

# # Calculate Duration
# duration = arr_time - dep_time
# duration_seconds = duration.total_seconds()
# if duration_seconds < 0:
#     st.error("❌ Arrival cannot be before Departure.")
#     st.stop()
# dur_hour = int(duration_seconds // 3600)
# dur_min = int((duration_seconds % 3600) // 60)
# st.info(f"⏱️ Flight Duration: {dur_hour}h {dur_min}m")

# # -------------------------
# # 4. PREDICTION
# # -------------------------
# if st.button("Calculate Best Fare"):
#     # Base numeric features
#     input_dict = {
#         "Total_Stops": total_stops,
#         "Journey_day": dep_time.day,
#         "Journey_month": dep_time.month,
#         "Dep_hour": dep_time.hour,
#         "Dep_min": dep_time.minute,
#         "Arrival_hour": arr_time.hour,
#         "Arrival_min": arr_time.minute,
#         "Duration_hours": dur_hour,
#         "Duration_mins": dur_min
#     }

#     # Create DataFrame with all zeros
#     input_df = pd.DataFrame(0, index=[0], columns=model_columns)

#     # Fill numeric features
#     for col in input_dict:
#         if col in input_df.columns:
#             input_df[col] = input_dict[col]

#     # Fill one-hot categorical features
#     airline_col = f"Airline_{airline}"
#     source_col = f"Source_{source}"
#     dest_col = f"Destination_{destination}"
#     for col in [airline_col, source_col, dest_col]:
#         if col in input_df.columns:
#             input_df[col] = 1

#     # Predict
#     try:
#         pred = model.predict(input_df)
#         final_price = np.expm1(pred[0])  # Reverse log1p

#         st.divider()
#         colA, colB = st.columns([1.2,1])

#         with colA:
#             st.markdown(f"""
#             <div class="price-card">
#                 <p style="color:#6366f1;">Estimated Fare</p>
#                 <h1 class="price-value">₹ {final_price:,.2f}</h1>
#                 <p>{airline} • {source} → {destination}</p>
#             </div>
#             """, unsafe_allow_html=True)
#             st.balloons()

#         with colB:
#             fig = go.Figure(go.Indicator(
#                 mode="gauge+number",
#                 value=final_price,
#                 gauge={
#                     'axis': {'range':[None,30000]},
#                     'bar': {'color':"#6366f1"},
#                     'steps':[{'range':[0,8000],'color':'rgba(0,255,0,0.1)'},
#                              {'range':[8000,18000],'color':'rgba(255,255,0,0.1)'},
#                              {'range':[18000,30000],'color':'rgba(255,0,0,0.1)'}]
#                 }
#             ))
#             fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
#             st.plotly_chart(fig, use_container_width=True)

#     except Exception as e:
#         st.error(f"Prediction Error: {e}")
#         st.write("⚠️ Make sure your input features exactly match the training features.")


import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.graph_objects as go
from datetime import datetime, timedelta

# -------------------------
# 1. PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Flight Price Intelligence", page_icon="✈️", layout="wide")

# -------------------------
# 2. LOAD MODEL + SCALER + COLUMNS
# -------------------------
@st.cache_resource
def load_all():
    model = joblib.load("xgboost_model.pkl")
    scaler = joblib.load("scaler.pkl")
    columns = joblib.load("columns.pkl")
    return model, scaler, columns

model, scaler, model_columns = load_all()

# -------------------------
# 3. UI
# -------------------------
st.title("✈️ Flight Price Intelligence")
st.caption("AI-based Flight Fare Prediction System")

col1, col2 = st.columns(2)

with col1:
    source = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
    destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
    airline = st.selectbox("Airline", [
        'Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
        'Multiple carriers', 'Multiple carriers Premium economy', 'SpiceJet',
        'Trujet', 'Vistara', 'Vistara Premium economy'
    ])

with col2:
    dep_time = st.datetime_input("Departure Time", value=datetime.now())
    arr_time = st.datetime_input("Arrival Time", value=dep_time + timedelta(hours=2))
    total_stops = st.select_slider("Total Stops", options=[0,1,2,3,4])

# -------------------------
# 4. FEATURE ENGINEERING
# -------------------------
duration = arr_time - dep_time
if duration.total_seconds() < 0:
    st.error("Arrival cannot be before Departure")
    st.stop()

dur_hour = int(duration.total_seconds() // 3600)
dur_min = int((duration.total_seconds() % 3600) // 60)

# -------------------------
# 5. PREDICTION
# -------------------------
if st.button("Predict Price"):

    # Create empty dataframe with all columns
    input_df = pd.DataFrame(0, index=[0], columns=model_columns)

    # Fill numeric features
    input_df["Total_Stops"] = total_stops
    input_df["Journey_day"] = dep_time.day
    input_df["Journey_month"] = dep_time.month
    input_df["Dep_hour"] = dep_time.hour
    input_df["Dep_min"] = dep_time.minute
    input_df["Arrival_hour"] = arr_time.hour
    input_df["Arrival_min"] = arr_time.minute
    input_df["Duration_hours"] = dur_hour
    input_df["Duration_mins"] = dur_min

    # Reset all categorical columns
    for col in model_columns:
        if "Airline_" in col or "Source_" in col or "Destination_" in col:
            input_df[col] = 0

    # Set selected categorical values
    if f"Airline_{airline}" in input_df.columns:
        input_df[f"Airline_{airline}"] = 1

    if f"Source_{source}" in input_df.columns:
        input_df[f"Source_{source}"] = 1

    if f"Destination_{destination}" in input_df.columns:
        input_df[f"Destination_{destination}"] = 1

    # ✅ APPLY SCALING (CRITICAL FIX)
    input_scaled = scaler.transform(input_df)

    # Predict
    prediction = model.predict(input_scaled)

    # Reverse log transform
    final_price = np.expm1(prediction[0])

    # -------------------------
    # 6. OUTPUT
    # -------------------------
    st.success(f"💰 Estimated Price: ₹ {final_price:,.2f}")

    # Optional chart
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=final_price,
        gauge={'axis': {'range': [None, 30000]}}
    ))
    st.plotly_chart(fig)

    # Debug (remove later)
    st.write("DEBUG INPUT:", input_df)