# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
# import io
# from datetime import datetime, timedelta

# # -------------------------
# # 1. PAGE CONFIG & STYLING
# # -------------------------
# st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# # Professional CSS for Dark Mode and Custom Cards
# st.markdown("""
#     <style>
#     .main { background-color: #0e1117; color: white; }
#     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
#     .stTabs [data-baseweb="tab"] {
#         height: 50px; white-space: pre-wrap; background-color: #1b263b;
#         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
#     }
#     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
#     div.stButton > button:first-child {
#         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
#         color: white; border: none; padding: 12px; border-radius: 8px; width: 100%;
#     }
#     .price-card {
#         background: #1b263b; padding: 30px; border-radius: 15px;
#         text-align: center; border: 1px solid #415a77; margin-bottom: 20px;
#     }
#     .price-value { font-size: 3rem; font-weight: 800; color: #00AEEF; }
#     </style>
#     """, unsafe_allow_html=True)

# # -------------------------
# # 2. LOAD AI ASSETS
# # -------------------------
# @st.cache_resource
# def load_assets():
#     model = joblib.load("xgboost_model.pkl")
#     scaler = joblib.load("scaler.pkl")
#     columns = joblib.load("columns.pkl")
#     ohe = joblib.load("airline_encoder.pkl")
#     return model, scaler, columns, ohe

# try:
#     model, scaler, columns, ohe = load_assets()
# except Exception as e:
#     st.error(f"🚨 Model files missing: {e}")
#     st.stop()

# # -------------------------
# # 3. HELPER FUNCTION: PREPROCESS
# # -------------------------
# def process_data(input_dict, airline_name):
#     df = pd.DataFrame([input_dict])
    
#     # One-hot encode airline
#     airline_encoded = ohe.transform([[airline_name]])
#     if hasattr(airline_encoded, "toarray"):
#         airline_encoded = airline_encoded.toarray()
    
#     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
#     df = pd.concat([df, airline_df], axis=1)

#     # Ensure all columns exist and are in the correct order
#     for col in columns:
#         if col not in df.columns:
#             df[col] = 0
#     df = df[columns]
    
#     # Scale and Predict
#     df_scaled = scaler.transform(df)
#     log_pred = model.predict(df_scaled)
#     return np.expm1(log_pred[0]) # Reverse Log transformation

# # -------------------------
# # 4. MAIN UI - TABS
# # -------------------------
# st.title("✈️ AirFair Vista")
# st.caption("Advanced AI Flight Fare Prediction System | Powered by XGBoost")

# tab1, tab2 = st.tabs(["🎯 Single Prediction", "📊 Bulk Scanner"])

# # --- TAB 1: SINGLE PREDICTION ---
# with tab1:
#     col1, col2 = st.columns(2, gap="large")
#     with col1:
#         st.subheader("📍 Journey Details")
#         src = st.selectbox("Source City", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
#         dest = st.selectbox("Destination City", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
#         air = st.selectbox("Select Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])

#     with col2:
#         st.subheader("🕒 Schedule")
#         dep = st.datetime_input("Departure Date & Time", value=datetime.now())
#         arr = st.datetime_input("Arrival Date & Time", value=dep + timedelta(hours=2))
#         stops = st.slider("Number of Stops", 0, 4, 0)

#     if st.button("Calculate Estimated Fare"):
#         if arr <= dep:
#             st.error("Arrival must be after Departure!")
#         else:
#             duration = arr - dep
#             dur_h = int(duration.total_seconds() // 3600)
#             dur_m = int((duration.total_seconds() % 3600) // 60)
            
#             input_features = {
#                 "Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month,
#                 "Dep_hour": dep.hour, "Dep_min": dep.minute, "Arrival_hour": arr.hour,
#                 "Arrival_min": arr.minute, "Duration_hours": dur_h, "Duration_mins": dur_m
#             }
            
#             final_price = process_data(input_features, air)
            
#             st.markdown(f"""
#                 <div class="price-card">
#                     <p style="color:#778da9; margin-bottom:0;">Estimated Ticket Price</p>
#                     <h1 class="price-value">₹ {final_price:,.2f}</h1>
#                     <p style="font-size:0.9rem;">{air} | {src} → {dest}</p>
#                 </div>
#             """, unsafe_allow_html=True)
#             st.balloons()

# # --- TAB 2: BULK SCANNER ---
# with tab2:
#     st.subheader("📂 Bulk Flight Price Analysis")
#     st.info("Upload a CSV with columns: Airline, Source, Destination, Dep_Time, Arrival_Time, Total_Stops")
    
#     upload_col, info_col = st.columns([2, 1])
    
#     with upload_col:
#         uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
#     with info_col:
#         # Template Download
#         sample = pd.DataFrame({
#             'Airline': ['IndiGo'], 'Source': ['Delhi'], 'Destination': ['Cochin'],
#             'Dep_Time': ['2026-05-10 10:00'], 'Arrival_Time': ['2026-05-10 13:00'], 'Total_Stops': [0]
#         })
#         st.download_button("📩 Download CSV Template", sample.to_csv(index=False), "template.csv")

#     if uploaded_file:
#         df_bulk = pd.read_csv(uploaded_file)
#         if st.button("🚀 Run Bulk Prediction"):
#             with st.spinner("Analyzing flights..."):
#                 prices = []
#                 # Simple loop for demo; for huge files, use a vectorized approach
#                 for _, row in df_bulk.iterrows():
#                     try:
#                         d_t = pd.to_datetime(row['Dep_Time'])
#                         a_t = pd.to_datetime(row['Arrival_Time'])
#                         diff = a_t - d_t
#                         feats = {
#                             "Total_Stops": row['Total_Stops'], "Journey_day": d_t.day, "Journey_month": d_t.month,
#                             "Dep_hour": d_t.hour, "Dep_min": d_t.minute, "Arrival_hour": a_t.hour,
#                             "Arrival_min": a_t.minute, "Duration_hours": int(diff.total_seconds()//3600),
#                             "Duration_mins": int((diff.total_seconds()%3600)//60)
#                         }
#                         prices.append(round(process_data(feats, row['Airline']), 2))
#                     except:
#                         prices.append(np.nan)
                
#                 df_bulk['Predicted_Price'] = prices
#                 st.write("### Preview of Results", df_bulk.head())
#                 st.download_button("📥 Download Results", df_bulk.to_csv(index=False), "predictions.csv")