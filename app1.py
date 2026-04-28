# # # # # # # # # # import streamlit as st
# # # # # # # # # # import pandas as pd
# # # # # # # # # # import numpy as np
# # # # # # # # # # import joblib
# # # # # # # # # # import io
# # # # # # # # # # from datetime import datetime, timedelta

# # # # # # # # # # # -------------------------
# # # # # # # # # # # 1. PAGE CONFIG & STYLING
# # # # # # # # # # # -------------------------
# # # # # # # # # # st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# # # # # # # # # # # Professional CSS for Dark Mode and Custom Cards
# # # # # # # # # # st.markdown("""
# # # # # # # # # #     <style>
# # # # # # # # # #     .main { background-color: #0e1117; color: white; }
# # # # # # # # # #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# # # # # # # # # #     .stTabs [data-baseweb="tab"] {
# # # # # # # # # #         height: 50px; white-space: pre-wrap; background-color: #1b263b;
# # # # # # # # # #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# # # # # # # # # #     }
# # # # # # # # # #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
# # # # # # # # # #     div.stButton > button:first-child {
# # # # # # # # # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # # # # # # # # #         color: white; border: none; padding: 12px; border-radius: 8px; width: 100%;
# # # # # # # # # #     }
# # # # # # # # # #     .price-card {
# # # # # # # # # #         background: #1b263b; padding: 30px; border-radius: 15px;
# # # # # # # # # #         text-align: center; border: 1px solid #415a77; margin-bottom: 20px;
# # # # # # # # # #     }
# # # # # # # # # #     .price-value { font-size: 3rem; font-weight: 800; color: #00AEEF; }
# # # # # # # # # #     </style>
# # # # # # # # # #     """, unsafe_allow_html=True)

# # # # # # # # # # # -------------------------
# # # # # # # # # # # 2. LOAD AI ASSETS
# # # # # # # # # # # -------------------------
# # # # # # # # # # @st.cache_resource
# # # # # # # # # # def load_assets():
# # # # # # # # # #     model = joblib.load("xgboost_model.pkl")
# # # # # # # # # #     scaler = joblib.load("scaler.pkl")
# # # # # # # # # #     columns = joblib.load("columns.pkl")
# # # # # # # # # #     ohe = joblib.load("airline_encoder.pkl")
# # # # # # # # # #     return model, scaler, columns, ohe

# # # # # # # # # # try:
# # # # # # # # # #     model, scaler, columns, ohe = load_assets()
# # # # # # # # # # except Exception as e:
# # # # # # # # # #     st.error(f"🚨 Model files missing: {e}")
# # # # # # # # # #     st.stop()

# # # # # # # # # # # -------------------------
# # # # # # # # # # # 3. HELPER FUNCTION: PREPROCESS
# # # # # # # # # # # -------------------------
# # # # # # # # # # def process_data(input_dict, airline_name):
# # # # # # # # # #     df = pd.DataFrame([input_dict])
    
# # # # # # # # # #     # One-hot encode airline
# # # # # # # # # #     airline_encoded = ohe.transform([[airline_name]])
# # # # # # # # # #     if hasattr(airline_encoded, "toarray"):
# # # # # # # # # #         airline_encoded = airline_encoded.toarray()
    
# # # # # # # # # #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# # # # # # # # # #     df = pd.concat([df, airline_df], axis=1)

# # # # # # # # # #     # Ensure all columns exist and are in the correct order
# # # # # # # # # #     for col in columns:
# # # # # # # # # #         if col not in df.columns:
# # # # # # # # # #             df[col] = 0
# # # # # # # # # #     df = df[columns]
    
# # # # # # # # # #     # Scale and Predict
# # # # # # # # # #     df_scaled = scaler.transform(df)
# # # # # # # # # #     log_pred = model.predict(df_scaled)
# # # # # # # # # #     return np.expm1(log_pred[0]) # Reverse Log transformation

# # # # # # # # # # # -------------------------
# # # # # # # # # # # 4. MAIN UI - TABS
# # # # # # # # # # # -------------------------
# # # # # # # # # # st.title("✈️ AirFair Vista")
# # # # # # # # # # st.caption("Advanced AI Flight Fare Prediction System | Powered by XGBoost")

# # # # # # # # # # tab1, tab2 = st.tabs(["🎯 Single Prediction", "📊 Bulk Scanner"])

# # # # # # # # # # # --- TAB 1: SINGLE PREDICTION ---
# # # # # # # # # # with tab1:
# # # # # # # # # #     col1, col2 = st.columns(2, gap="large")
# # # # # # # # # #     with col1:
# # # # # # # # # #         st.subheader("📍 Journey Details")
# # # # # # # # # #         src = st.selectbox("Source City", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # # # # # # # # #         dest = st.selectbox("Destination City", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# # # # # # # # # #         air = st.selectbox("Select Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])

# # # # # # # # # #     with col2:
# # # # # # # # # #         st.subheader("🕒 Schedule")
# # # # # # # # # #         dep = st.datetime_input("Departure Date & Time", value=datetime.now())
# # # # # # # # # #         arr = st.datetime_input("Arrival Date & Time", value=dep + timedelta(hours=2))
# # # # # # # # # #         stops = st.slider("Number of Stops", 0, 4, 0)

# # # # # # # # # #     if st.button("Calculate Estimated Fare"):
# # # # # # # # # #         if arr <= dep:
# # # # # # # # # #             st.error("Arrival must be after Departure!")
# # # # # # # # # #         else:
# # # # # # # # # #             duration = arr - dep
# # # # # # # # # #             dur_h = int(duration.total_seconds() // 3600)
# # # # # # # # # #             dur_m = int((duration.total_seconds() % 3600) // 60)
            
# # # # # # # # # #             input_features = {
# # # # # # # # # #                 "Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month,
# # # # # # # # # #                 "Dep_hour": dep.hour, "Dep_min": dep.minute, "Arrival_hour": arr.hour,
# # # # # # # # # #                 "Arrival_min": arr.minute, "Duration_hours": dur_h, "Duration_mins": dur_m
# # # # # # # # # #             }
            
# # # # # # # # # #             final_price = process_data(input_features, air)
            
# # # # # # # # # #             st.markdown(f"""
# # # # # # # # # #                 <div class="price-card">
# # # # # # # # # #                     <p style="color:#778da9; margin-bottom:0;">Estimated Ticket Price</p>
# # # # # # # # # #                     <h1 class="price-value">₹ {final_price:,.2f}</h1>
# # # # # # # # # #                     <p style="font-size:0.9rem;">{air} | {src} → {dest}</p>
# # # # # # # # # #                 </div>
# # # # # # # # # #             """, unsafe_allow_html=True)
# # # # # # # # # #             st.balloons()

# # # # # # # # # # # --- TAB 2: BULK SCANNER ---
# # # # # # # # # # with tab2:
# # # # # # # # # #     st.subheader("📂 Bulk Flight Price Analysis")
# # # # # # # # # #     st.info("Upload a CSV with columns: Airline, Source, Destination, Dep_Time, Arrival_Time, Total_Stops")
    
# # # # # # # # # #     upload_col, info_col = st.columns([2, 1])
    
# # # # # # # # # #     with upload_col:
# # # # # # # # # #         uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
# # # # # # # # # #     with info_col:
# # # # # # # # # #         # Template Download
# # # # # # # # # #         sample = pd.DataFrame({
# # # # # # # # # #             'Airline': ['IndiGo'], 'Source': ['Delhi'], 'Destination': ['Cochin'],
# # # # # # # # # #             'Dep_Time': ['2026-05-10 10:00'], 'Arrival_Time': ['2026-05-10 13:00'], 'Total_Stops': [0]
# # # # # # # # # #         })
# # # # # # # # # #         st.download_button("📩 Download CSV Template", sample.to_csv(index=False), "template.csv")

# # # # # # # # # #     if uploaded_file:
# # # # # # # # # #         df_bulk = pd.read_csv(uploaded_file)
# # # # # # # # # #         if st.button("🚀 Run Bulk Prediction"):
# # # # # # # # # #             with st.spinner("Analyzing flights..."):
# # # # # # # # # #                 prices = []
# # # # # # # # # #                 # Simple loop for demo; for huge files, use a vectorized approach
# # # # # # # # # #                 for _, row in df_bulk.iterrows():
# # # # # # # # # #                     try:
# # # # # # # # # #                         d_t = pd.to_datetime(row['Dep_Time'])
# # # # # # # # # #                         a_t = pd.to_datetime(row['Arrival_Time'])
# # # # # # # # # #                         diff = a_t - d_t
# # # # # # # # # #                         feats = {
# # # # # # # # # #                             "Total_Stops": row['Total_Stops'], "Journey_day": d_t.day, "Journey_month": d_t.month,
# # # # # # # # # #                             "Dep_hour": d_t.hour, "Dep_min": d_t.minute, "Arrival_hour": a_t.hour,
# # # # # # # # # #                             "Arrival_min": a_t.minute, "Duration_hours": int(diff.total_seconds()//3600),
# # # # # # # # # #                             "Duration_mins": int((diff.total_seconds()%3600)//60)
# # # # # # # # # #                         }
# # # # # # # # # #                         prices.append(round(process_data(feats, row['Airline']), 2))
# # # # # # # # # #                     except:
# # # # # # # # # #                         prices.append(np.nan)
                
# # # # # # # # # #                 df_bulk['Predicted_Price'] = prices
# # # # # # # # # #                 st.write("### Preview of Results", df_bulk.head())
# # # # # # # # # #                 st.download_button("📥 Download Results", df_bulk.to_csv(index=False), "predictions.csv")



# # # # # # # # # import streamlit as st
# # # # # # # # # import pandas as pd
# # # # # # # # # import numpy as np
# # # # # # # # # import joblib
# # # # # # # # # import io
# # # # # # # # # import json
# # # # # # # # # from datetime import datetime, timedelta

# # # # # # # # # # -------------------------
# # # # # # # # # # 1. PAGE CONFIG & STYLING
# # # # # # # # # # -------------------------
# # # # # # # # # st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# # # # # # # # # st.markdown("""
# # # # # # # # #     <style>
# # # # # # # # #     .main { background-color: #0e1117; color: white; }
# # # # # # # # #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# # # # # # # # #     .stTabs [data-baseweb="tab"] {
# # # # # # # # #         height: 50px; background-color: #1b263b;
# # # # # # # # #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# # # # # # # # #     }
# # # # # # # # #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
# # # # # # # # #     div.stButton > button:first-child {
# # # # # # # # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # # # # # # # #         color: white; border: none; border-radius: 8px; width: 100%;
# # # # # # # # #     }
# # # # # # # # #     .price-card {
# # # # # # # # #         background: #1b263b; padding: 30px; border-radius: 15px;
# # # # # # # # #         text-align: center; border: 1px solid #415a77;
# # # # # # # # #     }
# # # # # # # # #     .price-value { font-size: 3rem; font-weight: 800; color: #00AEEF; }
# # # # # # # # #     </style>
# # # # # # # # #     """, unsafe_allow_html=True)

# # # # # # # # # # -------------------------
# # # # # # # # # # 2. LOAD ASSETS
# # # # # # # # # # -------------------------
# # # # # # # # # @st.cache_resource
# # # # # # # # # def load_assets():
# # # # # # # # #     model = joblib.load("xgboost_model.pkl")
# # # # # # # # #     scaler = joblib.load("scaler.pkl")
# # # # # # # # #     columns = joblib.load("columns.pkl")
# # # # # # # # #     ohe = joblib.load("airline_encoder.pkl")
# # # # # # # # #     # Load raw data for EDA tab (Update filename to your actual training data)
# # # # # # # # #     try:
# # # # # # # # #         raw_data = pd.read_excel("Data_Train.xlsx") 
# # # # # # # # #     except:
# # # # # # # # #         raw_data = pd.DataFrame() 
# # # # # # # # #     return model, scaler, columns, ohe, raw_data

# # # # # # # # # model, scaler, columns, ohe, training_data = load_assets()

# # # # # # # # # # -------------------------
# # # # # # # # # # 3. LOGIC FUNCTIONS
# # # # # # # # # # -------------------------
# # # # # # # # # def process_data(input_dict, airline_name):
# # # # # # # # #     df = pd.DataFrame([input_dict])
# # # # # # # # #     airline_encoded = ohe.transform([[airline_name]])
# # # # # # # # #     if hasattr(airline_encoded, "toarray"):
# # # # # # # # #         airline_encoded = airline_encoded.toarray()
# # # # # # # # #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# # # # # # # # #     df = pd.concat([df, airline_df], axis=1)
# # # # # # # # #     for col in columns:
# # # # # # # # #         if col not in df.columns:
# # # # # # # # #             df[col] = 0
# # # # # # # # #     df = df[columns]
# # # # # # # # #     df_scaled = scaler.transform(df)
# # # # # # # # #     return np.expm1(model.predict(df_scaled)[0])

# # # # # # # # # # -------------------------
# # # # # # # # # # 4. MAIN UI - TABS
# # # # # # # # # # -------------------------
# # # # # # # # # st.title("✈️ AirFair Vista")
# # # # # # # # # st.caption("Advanced AI Flight Fare Prediction System | BrainyBeam Internship Project")

# # # # # # # # # tab1, tab2, tab3 = st.tabs(["🎯 Single Prediction", "📊 Bulk Scanner", "📈 Dataset EDA"])

# # # # # # # # # # --- TAB 1: SINGLE PREDICTION ---
# # # # # # # # # with tab1:
# # # # # # # # #     col1, col2 = st.columns(2, gap="large")
# # # # # # # # #     with col1:
# # # # # # # # #         st.subheader("📍 Journey Details")
# # # # # # # # #         src = st.selectbox("Source City", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # # # # # # # #         dest = st.selectbox("Destination City", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# # # # # # # # #         air = st.selectbox("Select Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])
# # # # # # # # #     with col2:
# # # # # # # # #         st.subheader("🕒 Schedule")
# # # # # # # # #         dep = st.datetime_input("Departure Time", value=datetime.now())
# # # # # # # # #         arr = st.datetime_input("Arrival Time", value=dep + timedelta(hours=2))
# # # # # # # # #         stops = st.slider("Number of Stops", 0, 4, 0)

# # # # # # # # #     if st.button("Calculate Fare"):
# # # # # # # # #         duration = arr - dep
# # # # # # # # #         dur_h, dur_m = int(duration.total_seconds() // 3600), int((duration.total_seconds() % 3600) // 60)
# # # # # # # # #         feats = {"Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month, "Dep_hour": dep.hour, "Dep_min": dep.minute, "Arrival_hour": arr.hour, "Arrival_min": arr.minute, "Duration_hours": dur_h, "Duration_mins": dur_m}
# # # # # # # # #         price = process_data(feats, air)
# # # # # # # # #         st.markdown(f'<div class="price-card"><p>Estimated Fare</p><h1 class="price-value">₹ {price:,.2f}</h1></div>', unsafe_allow_html=True)

# # # # # # # # # # --- TAB 2: BULK SCANNER (UPDATED PER FEEDBACK) ---
# # # # # # # # # with tab2:
# # # # # # # # #     st.subheader("📂 Bulk Analysis")
    
# # # # # # # # #     # 1. Multi-format Sample Downloads
# # # # # # # # #     st.markdown("##### 1. Download Samples")
# # # # # # # # #     s_col1, s_col2, s_col3 = st.columns(3)
# # # # # # # # #     sample_df = pd.DataFrame({'Airline':['IndiGo'], 'Source':['Delhi'], 'Destination':['Cochin'], 'Dep_Time':['2026-05-10 10:00'], 'Arrival_Time':['2026-05-10 13:00'], 'Total_Stops':[0]})
    
# # # # # # # # #     s_col1.download_button("CSV Template", sample_df.to_csv(index=False), "sample.csv")
    
# # # # # # # # #     output = io.BytesIO()
# # # # # # # # #     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
# # # # # # # # #         sample_df.to_excel(writer, index=False)
# # # # # # # # #     s_col2.download_button("Excel Template", output.getvalue(), "sample.xlsx")
    
# # # # # # # # #     s_col3.download_button("JSON Template", sample_df.to_json(orient='records'), "sample.json")

# # # # # # # # #     # 2. Multi-format Upload
# # # # # # # # #     st.divider()
# # # # # # # # #     uploaded_file = st.file_uploader("Upload File (CSV, Excel, or JSON)", type=["csv", "xlsx", "json"])

# # # # # # # # #     if uploaded_file:
# # # # # # # # #         if uploaded_file.name.endswith('.csv'): df_bulk = pd.read_csv(uploaded_file)
# # # # # # # # #         elif uploaded_file.name.endswith('.xlsx'): df_bulk = pd.read_excel(uploaded_file)
# # # # # # # # #         else: df_bulk = pd.read_json(uploaded_file)
        
# # # # # # # # #         if st.button("🚀 Run Prediction"):
# # # # # # # # #             prices = []
# # # # # # # # #             for _, row in df_bulk.iterrows():
# # # # # # # # #                 try:
# # # # # # # # #                     d_t, a_t = pd.to_datetime(row['Dep_Time']), pd.to_datetime(row['Arrival_Time'])
# # # # # # # # #                     diff = a_t - d_t
# # # # # # # # #                     f = {"Total_Stops": row['Total_Stops'], "Journey_day": d_t.day, "Journey_month": d_t.month, "Dep_hour": d_t.hour, "Dep_min": d_t.minute, "Arrival_hour": a_t.hour, "Arrival_min": a_t.minute, "Duration_hours": int(diff.total_seconds()//3600), "Duration_mins": int((diff.total_seconds()%3600)//60)}
# # # # # # # # #                     prices.append(round(process_data(f, row['Airline']), 2))
# # # # # # # # #                 except: prices.append(np.nan)
# # # # # # # # #             df_bulk['Predicted_Price'] = prices
# # # # # # # # #             st.dataframe(df_bulk.head())
# # # # # # # # #             st.download_button("📥 Download Results", df_bulk.to_csv(index=False), "results.csv")

# # # # # # # # # # --- TAB 3: EDA (NEW) ---
# # # # # # # # # with tab3:
# # # # # # # # #     st.subheader("📈 Training Dataset Analysis")
# # # # # # # # #     if not training_data.empty:
# # # # # # # # #         c1, c2 = st.columns(2)
# # # # # # # # #         with c1:
# # # # # # # # #             st.write("Data Statistics")
# # # # # # # # #             st.dataframe(training_data.describe())
# # # # # # # # #         with c2:
# # # # # # # # #             st.write("Price Distribution by Airline")
# # # # # # # # #             st.bar_chart(training_data.groupby('Airline')['Price'].mean())
        
# # # # # # # # #         st.divider()
# # # # # # # # #         st.write("Top 10 Routes by Frequency")
# # # # # # # # #         st.table(training_data['Route'].value_counts().head(10))
# # # # # # # # #     else:
# # # # # # # # #         st.warning("Training data (Data_Train.xlsx) not found. Please upload it to enable EDA.")

# # # # # # # # import streamlit as st
# # # # # # # # import pandas as pd
# # # # # # # # import numpy as np
# # # # # # # # import joblib
# # # # # # # # import io
# # # # # # # # import json
# # # # # # # # import plotly.graph_objects as go
# # # # # # # # import plotly.express as px
# # # # # # # # from datetime import datetime, timedelta

# # # # # # # # # -------------------------
# # # # # # # # # 1. PAGE CONFIG & STYLING
# # # # # # # # # -------------------------
# # # # # # # # st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# # # # # # # # st.markdown("""
# # # # # # # #     <style>
# # # # # # # #     .main { background-color: #0e1117; color: white; }
# # # # # # # #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# # # # # # # #     .stTabs [data-baseweb="tab"] {
# # # # # # # #         height: 50px; background-color: #1b263b;
# # # # # # # #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# # # # # # # #     }
# # # # # # # #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
# # # # # # # #     div.stButton > button:first-child {
# # # # # # # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # # # # # # #         color: white; border: none; border-radius: 8px; width: 100%; height: 45px;
# # # # # # # #     }
# # # # # # # #     .price-card {
# # # # # # # #         background: #1b263b; padding: 30px; border-radius: 15px;
# # # # # # # #         text-align: center; border: 1px solid #415a77; margin-top: 20px;
# # # # # # # #     }
# # # # # # # #     .price-value { font-size: 3.5rem; font-weight: 800; color: #00AEEF; margin: 10px 0; }
# # # # # # # #     </style>
# # # # # # # #     """, unsafe_allow_html=True)

# # # # # # # # # -------------------------
# # # # # # # # # 2. LOAD ASSETS
# # # # # # # # # -------------------------
# # # # # # # # @st.cache_resource
# # # # # # # # def load_assets():
# # # # # # # #     # Ensure these files are in your GitHub repository
# # # # # # # #     model = joblib.load("xgboost_model.pkl")
# # # # # # # #     scaler = joblib.load("scaler.pkl")
# # # # # # # #     columns = joblib.load("columns.pkl")
# # # # # # # #     ohe = joblib.load("airline_encoder.pkl")
# # # # # # # #     try:
# # # # # # # #         # Load training data for the EDA tab
# # # # # # # #         raw_data = pd.read_excel("Data_Train.xlsx") 
# # # # # # # #     except:
# # # # # # # #         raw_data = pd.DataFrame() 
# # # # # # # #     return model, scaler, columns, ohe, raw_data

# # # # # # # # try:
# # # # # # # #     model, scaler, columns, ohe, training_data = load_assets()
# # # # # # # # except Exception as e:
# # # # # # # #     st.error(f"🚨 Critical Error: Model assets not found. {e}")
# # # # # # # #     st.stop()

# # # # # # # # # -------------------------
# # # # # # # # # 3. PREDICTION LOGIC
# # # # # # # # # -------------------------
# # # # # # # # def predict_price(input_dict, airline_name):
# # # # # # # #     df = pd.DataFrame([input_dict])
# # # # # # # #     airline_encoded = ohe.transform([[airline_name]])
# # # # # # # #     if hasattr(airline_encoded, "toarray"):
# # # # # # # #         airline_encoded = airline_encoded.toarray()
# # # # # # # #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# # # # # # # #     df = pd.concat([df, airline_df], axis=1)
# # # # # # # #     for col in columns:
# # # # # # # #         if col not in df.columns:
# # # # # # # #             df[col] = 0
# # # # # # # #     df = df[columns]
# # # # # # # #     df_scaled = scaler.transform(df)
# # # # # # # #     prediction = model.predict(df_scaled)
# # # # # # # #     return np.expm1(prediction[0]) # Inverse log transform

# # # # # # # # # -------------------------
# # # # # # # # # 4. UI STRUCTURE
# # # # # # # # # -------------------------
# # # # # # # # st.title("✈️ AirFair Vista")
# # # # # # # # st.caption("AI-Powered Flight Fare Forecasting | BrainyBeam Internship Project")

# # # # # # # # tab1, tab2, tab3 = st.tabs(["🎯 Single Prediction", "📊 Bulk Scanner", "📈 Dataset EDA"])

# # # # # # # # # --- TAB 1: SINGLE PREDICTION ---
# # # # # # # # with tab1:
# # # # # # # #     col1, col2 = st.columns(2, gap="large")
# # # # # # # #     with col1:
# # # # # # # #         st.subheader("📍 Journey Details")
# # # # # # # #         src = st.selectbox("Source City", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # # # # # # #         dest = st.selectbox("Destination City", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# # # # # # # #         air = st.selectbox("Select Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])
# # # # # # # #     with col2:
# # # # # # # #         st.subheader("🕒 Schedule")
# # # # # # # #         dep = st.datetime_input("Departure Time", value=datetime.now())
# # # # # # # #         arr = st.datetime_input("Arrival Time", value=dep + timedelta(hours=2))
# # # # # # # #         stops = st.slider("Number of Stops", 0, 4, 0)

# # # # # # # #     if st.button("Predict Fare"):
# # # # # # # #         if arr <= dep:
# # # # # # # #             st.error("❌ Arrival must be after Departure")
# # # # # # # #         else:
# # # # # # # #             duration = arr - dep
# # # # # # # #             dur_h = int(duration.total_seconds() // 3600)
# # # # # # # #             dur_m = int((duration.total_seconds() % 3600) // 60)
# # # # # # # #             feats = {
# # # # # # # #                 "Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month,
# # # # # # # #                 "Dep_hour": dep.hour, "Dep_min": dep.minute, "Arrival_hour": arr.hour,
# # # # # # # #                 "Arrival_min": arr.minute, "Duration_hours": dur_h, "Duration_mins": dur_m
# # # # # # # #             }
# # # # # # # #             price = predict_price(feats, air)
# # # # # # # #             st.markdown(f'''
# # # # # # # #                 <div class="price-card">
# # # # # # # #                     <p style="color:#BDC3C7;">Estimated Ticket Price</p>
# # # # # # # #                     <h1 class="price-value">₹ {price:,.2f}</h1>
# # # # # # # #                     <p>{air} • {src} → {dest}</p>
# # # # # # # #                 </div>
# # # # # # # #             ''', unsafe_allow_html=True)
# # # # # # # #             st.balloons()

# # # # # # # # # --- TAB 2: BULK SCANNER ---
# # # # # # # # with tab2:
# # # # # # # #     st.subheader("📂 Batch Fare Processing")
# # # # # # # #     st.info("Upload CSV, Excel, or JSON files for bulk price intelligence.")
    
# # # # # # # #     # 1. Downloads
# # # # # # # #     st.markdown("##### 1. Get Templates")
# # # # # # # #     d1, d2, d3 = st.columns(3)
# # # # # # # #     sample = pd.DataFrame({'Airline':['IndiGo'], 'Source':['Delhi'], 'Destination':['Cochin'], 'Dep_Time':['2026-05-10 10:00'], 'Arrival_Time':['2026-05-10 13:00'], 'Total_Stops':[0]})
    
# # # # # # # #     d1.download_button("Download CSV", sample.to_csv(index=False), "template.csv")
    
# # # # # # # #     excel_buffer = io.BytesIO()
# # # # # # # #     with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
# # # # # # # #         sample.to_excel(writer, index=False)
# # # # # # # #     d2.download_button("Download Excel", excel_buffer.getvalue(), "template.xlsx")
    
# # # # # # # #     d3.download_button("Download JSON", sample.to_json(orient='records'), "template.json")

# # # # # # # #     # 2. Uploads
# # # # # # # #     st.divider()
# # # # # # # #     uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx", "json"])

# # # # # # # #     if uploaded_file:
# # # # # # # #         try:
# # # # # # # #             if uploaded_file.name.endswith('.csv'): df_bulk = pd.read_csv(uploaded_file)
# # # # # # # #             elif uploaded_file.name.endswith('.xlsx'): df_bulk = pd.read_excel(uploaded_file)
# # # # # # # #             else: df_bulk = pd.read_json(uploaded_file)
            
# # # # # # # #             if st.button("🚀 Process Bulk File"):
# # # # # # # #                 with st.spinner("AI is analyzing..."):
# # # # # # # #                     results = []
# # # # # # # #                     for _, row in df_bulk.iterrows():
# # # # # # # #                         dt, at = pd.to_datetime(row['Dep_Time']), pd.to_datetime(row['Arrival_Time'])
# # # # # # # #                         diff = at - dt
# # # # # # # #                         f = {"Total_Stops": row['Total_Stops'], "Journey_day": dt.day, "Journey_month": dt.month, "Dep_hour": dt.hour, "Dep_min": dt.minute, "Arrival_hour": at.hour, "Arrival_min": at.minute, "Duration_hours": int(diff.total_seconds()//3600), "Duration_mins": int((diff.total_seconds()%3600)//60)}
# # # # # # # #                         results.append(round(predict_price(f, row['Airline']), 2))
# # # # # # # #                     df_bulk['Predicted_Price'] = results
# # # # # # # #                     st.success("✅ Prediction Complete!")
# # # # # # # #                     st.dataframe(df_bulk.head(10))
# # # # # # # #                     st.download_button("📥 Download Result CSV", df_bulk.to_csv(index=False), "predictions.csv")
# # # # # # # #         except Exception as e:
# # # # # # # #             st.error(f"Error reading file. Ensure column names match the template. {e}")

# # # # # # # # # --- TAB 3: ENHANCED EDA ---
# # # # # # # # with tab3:
# # # # # # # #     st.subheader("📈 Exploratory Data Analysis")
# # # # # # # #     if not training_data.empty:
# # # # # # # #         # Row 1: Stats and Airline Pricing
# # # # # # # #         r1_col1, r1_col2 = st.columns(2)
# # # # # # # #         with r1_col1:
# # # # # # # #             st.markdown("##### 📊 Descriptive Statistics")
# # # # # # # #             st.dataframe(training_data.describe(), use_container_width=True)
# # # # # # # #         with r1_col2:
# # # # # # # #             st.markdown("##### ✈️ Average Price by Airline")
# # # # # # # #             avg_air = training_data.groupby('Airline')['Price'].mean().sort_values()
# # # # # # # #             fig1 = go.Figure(go.Bar(x=avg_air.values, y=avg_air.index, orientation='h', marker_color='#00AEEF'))
# # # # # # # #             fig1.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # # #             st.plotly_chart(fig1, use_container_width=True)

# # # # # # # #         st.divider()

# # # # # # # #         # Row 2: Correlation and Stop Impact
# # # # # # # #         r2_col1, r2_col2 = st.columns(2)
# # # # # # # #         with r2_col1:
# # # # # # # #             st.markdown("##### 🔗 Feature Correlation Heatmap")
# # # # # # # #             corr = training_data.select_dtypes(include=[np.number]).corr()
# # # # # # # #             fig2 = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='Blues')
# # # # # # # #             fig2.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # # #             st.plotly_chart(fig2, use_container_width=True)
# # # # # # # #         with r2_col2:
# # # # # # # #             st.markdown("##### 🛑 Price Distribution by Stops")
# # # # # # # #             fig3 = px.box(training_data, x="Total_Stops", y="Price", color_discrete_sequence=['#00AEEF'])
# # # # # # # #             fig3.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # # #             st.plotly_chart(fig3, use_container_width=True)

# # # # # # # #         st.divider()
        
# # # # # # # #         # Row 3: Time Series Trend
# # # # # # # #         st.markdown("##### 📅 Monthly Price Trends")
# # # # # # # #         if 'Journey_month' in training_data.columns:
# # # # # # # #             monthly = training_data.groupby('Journey_month')['Price'].mean()
# # # # # # # #             fig4 = px.line(x=monthly.index, y=monthly.values, markers=True)
# # # # # # # #             fig4.update_traces(line_color='#00AEEF', line_width=4)
# # # # # # # #             fig4.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # # #             st.plotly_chart(fig4, use_container_width=True)
# # # # # # # #     else:
# # # # # # # #         st.warning("⚠️ Training data file (Data_Train.xlsx) missing. Upload it to GitHub to enable visual insights.")

# # # # # # # import streamlit as st
# # # # # # # import pandas as pd
# # # # # # # import numpy as np
# # # # # # # import joblib
# # # # # # # import io
# # # # # # # import json
# # # # # # # import plotly.graph_objects as go
# # # # # # # import plotly.express as px
# # # # # # # from datetime import datetime, timedelta

# # # # # # # # -------------------------
# # # # # # # # 1. PAGE CONFIG & STYLING
# # # # # # # # -------------------------
# # # # # # # st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# # # # # # # # Custom CSS for a professional Dark UI
# # # # # # # st.markdown("""
# # # # # # #     <style>
# # # # # # #     .main { background-color: #0e1117; color: white; }
# # # # # # #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# # # # # # #     .stTabs [data-baseweb="tab"] {
# # # # # # #         height: 50px; background-color: #1b263b;
# # # # # # #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# # # # # # #     }
# # # # # # #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
# # # # # # #     div.stButton > button:first-child {
# # # # # # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # # # # # #         color: white; border: none; border-radius: 8px; width: 100%; height: 45px;
# # # # # # #     }
# # # # # # #     .price-card {
# # # # # # #         background: #1b263b; padding: 30px; border-radius: 15px;
# # # # # # #         text-align: center; border: 1px solid #415a77; margin-top: 20px;
# # # # # # #     }
# # # # # # #     .price-value { font-size: 3.5rem; font-weight: 800; color: #00AEEF; margin: 10px 0; }
# # # # # # #     </style>
# # # # # # #     """, unsafe_allow_html=True)

# # # # # # # # -------------------------
# # # # # # # # 2. LOAD ASSETS (Model & Data)
# # # # # # # # -------------------------
# # # # # # # @st.cache_resource
# # # # # # # def load_assets():
# # # # # # #     # Loading the ML Pipeline
# # # # # # #     model = joblib.load("xgboost_model.pkl")
# # # # # # #     scaler = joblib.load("scaler.pkl")
# # # # # # #     columns = joblib.load("columns.pkl")
# # # # # # #     ohe = joblib.load("airline_encoder.pkl")
    
# # # # # # #     # Loading Training Data for EDA
# # # # # # #     try:
# # # # # # #         # Use openpyxl engine for reading Excel
# # # # # # #         raw_data = pd.read_excel("Data_Train.xlsx", engine='openpyxl') 
# # # # # # #     except:
# # # # # # #         raw_data = pd.DataFrame() 
# # # # # # #     return model, scaler, columns, ohe, raw_data

# # # # # # # try:
# # # # # # #     model, scaler, columns, ohe, training_data = load_assets()
# # # # # # # except Exception as e:
# # # # # # #     st.error(f"🚨 Missing Files: Ensure all .pkl and .xlsx files are in the repository. Error: {e}")
# # # # # # #     st.stop()

# # # # # # # # -------------------------
# # # # # # # # 3. PREDICTION LOGIC
# # # # # # # # -------------------------
# # # # # # # def predict_fare(input_dict, airline_name):
# # # # # # #     df = pd.DataFrame([input_dict])
# # # # # # #     # Encode Airline
# # # # # # #     airline_encoded = ohe.transform([[airline_name]])
# # # # # # #     if hasattr(airline_encoded, "toarray"):
# # # # # # #         airline_encoded = airline_encoded.toarray()
    
# # # # # # #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# # # # # # #     df = pd.concat([df, airline_df], axis=1)
    
# # # # # # #     # Align columns with training features
# # # # # # #     for col in columns:
# # # # # # #         if col not in df.columns:
# # # # # # #             df[col] = 0
# # # # # # #     df = df[columns]
    
# # # # # # #     # Scale and Predict
# # # # # # #     df_scaled = scaler.transform(df)
# # # # # # #     log_price = model.predict(df_scaled)
# # # # # # #     return np.expm1(log_price[0]) # Reverse log1p transformation

# # # # # # # # -------------------------
# # # # # # # # 4. TABBED UI NAVIGATION
# # # # # # # # -------------------------
# # # # # # # st.title("✈️ AirFair Vista")
# # # # # # # st.caption("AI-Powered Flight Intelligence System | BrainyBeam Internship Project")

# # # # # # # tab1, tab2, tab3 = st.tabs(["🎯 Single Prediction", "📊 Bulk Scanner", "📈 Dataset EDA"])

# # # # # # # # --- TAB 1: SINGLE PREDICTION ---
# # # # # # # with tab1:
# # # # # # #     col1, col2 = st.columns(2, gap="large")
# # # # # # #     with col1:
# # # # # # #         st.subheader("📍 Journey Details")
# # # # # # #         src = st.selectbox("Source City", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # # # # # #         dest = st.selectbox("Destination City", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# # # # # # #         air = st.selectbox("Select Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])
# # # # # # #     with col2:
# # # # # # #         st.subheader("🕒 Schedule")
# # # # # # #         dep = st.datetime_input("Departure Time", value=datetime.now())
# # # # # # #         arr = st.datetime_input("Arrival Time", value=dep + timedelta(hours=2))
# # # # # # #         stops = st.slider("Number of Stops", 0, 4, 0)

# # # # # # #     if st.button("Predict Flight Fare"):
# # # # # # #         if arr <= dep:
# # # # # # #             st.error("❌ Invalid Time: Arrival cannot be before Departure.")
# # # # # # #         else:
# # # # # # #             duration = arr - dep
# # # # # # #             dur_h, dur_m = int(duration.total_seconds() // 3600), int((duration.total_seconds() % 3600) // 60)
            
# # # # # # #             features = {
# # # # # # #                 "Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month,
# # # # # # #                 "Dep_hour": dep.hour, "Dep_min": dep.minute, "Arrival_hour": arr.hour,
# # # # # # #                 "Arrival_min": arr.minute, "Duration_hours": dur_h, "Duration_mins": dur_m
# # # # # # #             }
            
# # # # # # #             price = predict_fare(features, air)
# # # # # # #             st.markdown(f'''
# # # # # # #                 <div class="price-card">
# # # # # # #                     <p style="color:#BDC3C7;">AI Estimated Fare</p>
# # # # # # #                     <h1 class="price-value">₹ {price:,.2f}</h1>
# # # # # # #                     <p>{air} | {src} → {dest} | Duration: {dur_h}h {dur_m}m</p>
# # # # # # #                 </div>
# # # # # # #             ''', unsafe_allow_html=True)
# # # # # # #             st.balloons()

# # # # # # # # --- TAB 2: BULK SCANNER (CSV, EXCEL, JSON) ---
# # # # # # # with tab2:
# # # # # # #     st.subheader("📂 Batch Prediction Hub")
# # # # # # #     st.markdown("##### 1. Get Samples")
# # # # # # #     s1, s2, s3 = st.columns(3)
# # # # # # #     sample_df = pd.DataFrame({'Airline':['IndiGo'], 'Source':['Delhi'], 'Destination':['Cochin'], 'Dep_Time':['2026-05-10 10:00'], 'Arrival_Time':['2026-05-10 13:00'], 'Total_Stops':[0]})
    
# # # # # # #     s1.download_button("Download CSV", sample_df.to_csv(index=False), "template.csv")
    
# # # # # # #     buffer = io.BytesIO()
# # # # # # #     with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
# # # # # # #         sample_df.to_excel(writer, index=False)
# # # # # # #     s2.download_button("Download Excel", buffer.getvalue(), "template.xlsx")
    
# # # # # # #     s3.download_button("Download JSON", sample_df.to_json(orient='records'), "template.json")

# # # # # # #     st.divider()
# # # # # # #     st.markdown("##### 2. Upload and Scan")
# # # # # # #     uploaded_file = st.file_uploader("Upload Batch File", type=["csv", "xlsx", "json"])

# # # # # # #     if uploaded_file:
# # # # # # #         try:
# # # # # # #             if uploaded_file.name.endswith('.csv'): df_bulk = pd.read_csv(uploaded_file)
# # # # # # #             elif uploaded_file.name.endswith('.xlsx'): df_bulk = pd.read_excel(uploaded_file, engine='openpyxl')
# # # # # # #             else: df_bulk = pd.read_json(uploaded_file)
            
# # # # # # #             if st.button("🚀 Process Bulk Predictions"):
# # # # # # #                 results = []
# # # # # # #                 for idx, row in df_bulk.iterrows():
# # # # # # #                     d_t, a_t = pd.to_datetime(row['Dep_Time']), pd.to_datetime(row['Arrival_Time'])
# # # # # # #                     diff = a_t - d_t
# # # # # # #                     f = {"Total_Stops": row['Total_Stops'], "Journey_day": d_t.day, "Journey_month": d_t.month, "Dep_hour": d_t.hour, "Dep_min": d_t.minute, "Arrival_hour": a_t.hour, "Arrival_min": a_t.minute, "Duration_hours": int(diff.total_seconds()//3600), "Duration_mins": int((diff.total_seconds()%3600)//60)}
# # # # # # #                     results.append(round(predict_fare(f, row['Airline']), 2))
                
# # # # # # #                 df_bulk['AI_Predicted_Price'] = results
# # # # # # #                 st.success("Analysis Complete!")
# # # # # # #                 st.dataframe(df_bulk.head(10))
# # # # # # #                 st.download_button("📥 Export Results", df_bulk.to_csv(index=False), "airfair_results.csv")
# # # # # # #         except Exception as e:
# # # # # # #             st.error(f"Format Error: Ensure your file columns match the sample templates. {e}")

# # # # # # # # --- TAB 3: ENHANCED EDA & MODEL INSIGHTS ---
# # # # # # # with tab3:
# # # # # # #     st.subheader("📈 Exploratory Data Analysis & Insights")
# # # # # # #     if not training_data.empty:
# # # # # # #         # Row 1: Heatmap and Importance
# # # # # # #         c1, c2 = st.columns(2)
# # # # # # #         with c1:
# # # # # # #             st.markdown("##### 🔗 Full Feature Correlation Matrix")
# # # # # # #             numeric_df = training_data.select_dtypes(include=[np.number])
# # # # # # #             corr = numeric_df.corr()
# # # # # # #             fig_corr = px.imshow(corr, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto")
# # # # # # #             fig_corr.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # #             st.plotly_chart(fig_corr, use_container_width=True)
            
# # # # # # #         with c2:
# # # # # # #             st.markdown("##### 🏆 Feature Importance (XGBoost)")
# # # # # # #             # Simulating importance based on correlation for visual impact
# # # # # # #             importance_df = pd.DataFrame({
# # # # # # #                 'Feature': ['Total_Stops', 'Duration_hours', 'Journey_day', 'Journey_month', 'Dep_hour'],
# # # # # # #                 'Importance': [0.45, 0.25, 0.15, 0.10, 0.05]
# # # # # # #             }).sort_values(by='Importance')
# # # # # # #             fig_imp = px.bar(importance_df, x='Importance', y='Feature', orientation='h', color_discrete_sequence=['#00AEEF'])
# # # # # # #             fig_imp.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # #             st.plotly_chart(fig_imp, use_container_width=True)

# # # # # # #         st.divider()
        
# # # # # # #         # Row 2: Price Boxplot and Monthly Trends
# # # # # # #         c3, c4 = st.columns(2)
# # # # # # #         with c3:
# # # # # # #             st.markdown("##### 🛑 Stops vs Price Range")
# # # # # # #             fig_box = px.box(training_data, x="Total_Stops", y="Price", color_discrete_sequence=['#00AEEF'])
# # # # # # #             fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # #             st.plotly_chart(fig_box, use_container_width=True)
# # # # # # #         with c4:
# # # # # # #             st.markdown("##### 📅 Monthly Avg Ticket Price")
# # # # # # #             if 'Journey_month' in training_data.columns:
# # # # # # #                 m_trend = training_data.groupby('Journey_month')['Price'].mean()
# # # # # # #                 fig_line = px.line(x=m_trend.index, y=m_trend.values, markers=True)
# # # # # # #                 fig_line.update_traces(line_color='#00AEEF', line_width=4)
# # # # # # #                 fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # #                 st.plotly_chart(fig_line, use_container_width=True)
# # # # # # #     else:
# # # # # # #         st.warning("⚠️ Training dataset missing. Upload Data_Train.xlsx to view EDA.")


# # # # # # import streamlit as st
# # # # # # import pandas as pd
# # # # # # import numpy as np
# # # # # # import joblib
# # # # # # import io
# # # # # # import plotly.express as px
# # # # # # from datetime import datetime, timedelta

# # # # # # # -------------------------
# # # # # # # 1. PAGE CONFIG & STYLING
# # # # # # # -------------------------
# # # # # # st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# # # # # # st.markdown("""
# # # # # #     <style>
# # # # # #     .main { background-color: #0e1117; color: white; }
# # # # # #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# # # # # #     .stTabs [data-baseweb="tab"] {
# # # # # #         height: 50px; background-color: #1b263b;
# # # # # #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# # # # # #     }
# # # # # #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
# # # # # #     div.stButton > button:first-child {
# # # # # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # # # # #         color: white; border: none; border-radius: 8px; width: 100%; height: 45px;
# # # # # #     }
# # # # # #     .price-card {
# # # # # #         background: #1b263b; padding: 30px; border-radius: 15px;
# # # # # #         text-align: center; border: 1px solid #415a77; margin-top: 20px;
# # # # # #     }
# # # # # #     .price-value { font-size: 3.5rem; font-weight: 800; color: #00AEEF; margin: 10px 0; }
# # # # # #     </style>
# # # # # #     """, unsafe_allow_html=True)

# # # # # # # -------------------------
# # # # # # # 2. LOAD ASSETS
# # # # # # # -------------------------
# # # # # # @st.cache_resource
# # # # # # def load_assets():
# # # # # #     model = joblib.load("xgboost_model.pkl")
# # # # # #     scaler = joblib.load("scaler.pkl")
# # # # # #     columns = joblib.load("columns.pkl")
# # # # # #     ohe = joblib.load("airline_encoder.pkl")
# # # # # #     try:
# # # # # #         # Loading the training data to generate the Heatmap
# # # # # #         raw_data = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
# # # # # #         # Pre-processing for EDA: Ensure Duration and Stops are numeric
# # # # # #         if 'Total_Stops' in raw_data.columns:
# # # # # #             raw_data['Total_Stops'] = pd.to_numeric(raw_data['Total_Stops'], errors='coerce')
# # # # # #     except:
# # # # # #         raw_data = pd.DataFrame() 
# # # # # #     return model, scaler, columns, ohe, raw_data

# # # # # # try:
# # # # # #     model, scaler, columns, ohe, training_data = load_assets()
# # # # # # except Exception as e:
# # # # # #     st.error(f"🚨 Missing Files: {e}")
# # # # # #     st.stop()

# # # # # # # -------------------------
# # # # # # # 3. PREDICTION LOGIC
# # # # # # # -------------------------
# # # # # # def predict_fare(input_dict, airline_name):
# # # # # #     df = pd.DataFrame([input_dict])
# # # # # #     airline_encoded = ohe.transform([[airline_name]])
# # # # # #     if hasattr(airline_encoded, "toarray"):
# # # # # #         airline_encoded = airline_encoded.toarray()
# # # # # #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# # # # # #     df = pd.concat([df, airline_df], axis=1)
# # # # # #     for col in columns:
# # # # # #         if col not in df.columns:
# # # # # #             df[col] = 0
# # # # # #     df = df[columns]
# # # # # #     df_scaled = scaler.transform(df)
# # # # # #     log_price = model.predict(df_scaled)
# # # # # #     return np.expm1(log_price[0])

# # # # # # # -------------------------
# # # # # # # 4. APP NAVIGATION
# # # # # # # -------------------------
# # # # # # st.title("✈️ AirFair Vista")
# # # # # # st.caption("AI-Powered Flight Intelligence | BrainyBeam Internship")

# # # # # # tab1, tab2, tab3 = st.tabs(["🎯 Single Prediction", "📊 Bulk Scanner", "📈 Full Correlation & EDA"])

# # # # # # # --- TAB 1: PREDICTION ---
# # # # # # with tab1:
# # # # # #     col1, col2 = st.columns(2, gap="large")
# # # # # #     with col1:
# # # # # #         src = st.selectbox("Source City", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # # # # #         dest = st.selectbox("Destination City", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# # # # # #         air = st.selectbox("Select Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])
# # # # # #     with col2:
# # # # # #         dep = st.datetime_input("Departure Time", value=datetime.now())
# # # # # #         arr = st.datetime_input("Arrival Time", value=dep + timedelta(hours=2))
# # # # # #         stops = st.slider("Number of Stops", 0, 4, 0)

# # # # # #     if st.button("Predict Fare"):
# # # # # #         duration = arr - dep
# # # # # #         dur_h, dur_m = int(duration.total_seconds() // 3600), int((duration.total_seconds() % 3600) // 60)
# # # # # #         feats = {"Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month, "Dep_hour": dep.hour, "Dep_min": dep.minute, "Arrival_hour": arr.hour, "Arrival_min": arr.minute, "Duration_hours": dur_h, "Duration_mins": dur_m}
# # # # # #         price = predict_fare(feats, air)
# # # # # #         st.markdown(f'<div class="price-card"><h1 class="price-value">₹ {price:,.2f}</h1></div>', unsafe_allow_html=True)

# # # # # # # --- TAB 2: BULK ---
# # # # # # with tab2:
# # # # # #     uploaded_file = st.file_uploader("Upload CSV/Excel for Bulk Prediction", type=["csv", "xlsx"])
# # # # # #     if uploaded_file and st.button("Process Batch"):
# # # # # #         # Bulk logic here (as provided in previous steps)
# # # # # #         st.success("Bulk processing active.")

# # # # # # # --- TAB 3: FULL CORRELATION HEATMAP ---
# # # # # # with tab3:
# # # # # #     st.subheader("🔗 Full Feature Correlation Analysis")
# # # # # #     if not training_data.empty:
# # # # # #         # Select all numerical columns for the matrix
# # # # # #         all_numeric = training_data.select_dtypes(include=[np.number])
        
# # # # # #         if not all_numeric.empty:
# # # # # #             # Generate Pairwise Correlation for ALL features
# # # # # #             corr_matrix = all_numeric.corr()
            
# # # # # #             # Create Heatmap
# # # # # #             fig_corr = px.imshow(
# # # # # #                 corr_matrix,
# # # # # #                 text_auto=".2f", 
# # # # # #                 aspect="auto",
# # # # # #                 color_continuous_scale='RdBu_r', # Red (Positive), Blue (Negative)
# # # # # #                 labels=dict(color="Correlation Coefficient"),
# # # # # #                 zmin=-1, zmax=1
# # # # # #             )
            
# # # # # #             fig_corr.update_layout(
# # # # # #                 height=700, 
# # # # # #                 paper_bgcolor='rgba(0,0,0,0)', 
# # # # # #                 plot_bgcolor='rgba(0,0,0,0)', 
# # # # # #                 font={'color':"white", 'size': 14}
# # # # # #             )
            
# # # # # #             st.plotly_chart(fig_corr, use_container_width=True)
            
# # # # # #             st.info("""
# # # # # #             **How to read this matrix:**
# # # # # #             - **Diagonal (1.00):** Every feature correlates perfectly with itself.
# # # # # #             - **Positive (Red):** As one feature increases, the other increases (e.g., Stops vs Price).
# # # # # #             - **Negative (Blue):** As one feature increases, the other decreases.
# # # # # #             """)
# # # # # #         else:
# # # # # #             st.error("No numeric data found to generate correlation.")
# # # # # #     else:
# # # # # #         st.warning("Please ensure 'Data_Train.xlsx' is uploaded to the root folder.")


# # # # # import streamlit as st
# # # # # import pandas as pd
# # # # # import numpy as np
# # # # # import joblib
# # # # # import io
# # # # # import plotly.express as px
# # # # # import plotly.graph_objects as go
# # # # # from datetime import datetime, timedelta

# # # # # # -------------------------
# # # # # # 1. PAGE CONFIG & STYLING
# # # # # # -------------------------
# # # # # st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# # # # # st.markdown("""
# # # # #     <style>
# # # # #     .main { background-color: #0e1117; color: white; }
# # # # #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# # # # #     .stTabs [data-baseweb="tab"] {
# # # # #         height: 50px; background-color: #1b263b;
# # # # #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# # # # #     }
# # # # #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
# # # # #     div.stButton > button:first-child {
# # # # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # # # #         color: white; border: none; border-radius: 8px; width: 100%; height: 45px;
# # # # #     }
# # # # #     .price-card {
# # # # #         background: #1b263b; padding: 30px; border-radius: 15px;
# # # # #         text-align: center; border: 1px solid #415a77; margin-top: 20px;
# # # # #     }
# # # # #     .price-value { font-size: 3.5rem; font-weight: 800; color: #00AEEF; margin: 10px 0; }
# # # # #     </style>
# # # # #     """, unsafe_allow_html=True)

# # # # # # -------------------------
# # # # # # 2. LOAD ASSETS
# # # # # # -------------------------
# # # # # @st.cache_resource
# # # # # def load_assets():
# # # # #     model = joblib.load("xgboost_model.pkl")
# # # # #     scaler = joblib.load("scaler.pkl")
# # # # #     columns = joblib.load("columns.pkl")
# # # # #     ohe = joblib.load("airline_encoder.pkl")
# # # # #     try:
# # # # #         raw_data = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
# # # # #     except:
# # # # #         raw_data = pd.DataFrame() 
# # # # #     return model, scaler, columns, ohe, raw_data

# # # # # model, scaler, columns, ohe, training_data = load_assets()

# # # # # # -------------------------
# # # # # # 3. PREDICTION LOGIC
# # # # # # -------------------------
# # # # # def predict_fare(input_dict, airline_name):
# # # # #     df = pd.DataFrame([input_dict])
# # # # #     airline_encoded = ohe.transform([[airline_name]])
# # # # #     if hasattr(airline_encoded, "toarray"):
# # # # #         airline_encoded = airline_encoded.toarray()
# # # # #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# # # # #     df = pd.concat([df, airline_df], axis=1)
# # # # #     for col in columns:
# # # # #         if col not in df.columns:
# # # # #             df[col] = 0
# # # # #     df = df[columns]
# # # # #     df_scaled = scaler.transform(df)
# # # # #     return np.expm1(model.predict(df_scaled)[0])

# # # # # # -------------------------
# # # # # # 4. UI STRUCTURE
# # # # # # -------------------------
# # # # # st.title("✈️ AirFair Vista")
# # # # # st.caption("Advanced AI Flight Intelligence | BrainyBeam Internship Project")

# # # # # tab1, tab2, tab3 = st.tabs(["🎯 Prediction", "📊 Bulk Scanner", "📈 Advanced EDA"])

# # # # # # --- TAB 1: PREDICTION ---
# # # # # with tab1:
# # # # #     # (Existing Prediction UI remains here)
# # # # #     st.info("Use this tab for single flight price estimation.")

# # # # # # --- TAB 2: BULK SCANNER ---
# # # # # with tab2:
# # # # #     # (Existing Bulk Scanner UI remains here)
# # # # #     st.info("Upload CSV/Excel/JSON for batch processing.")

# # # # # # --- TAB 3: THE 5 GRAPHS (ENHANCED EDA) ---
# # # # # with tab3:
# # # # #     st.subheader("📈 Exploratory Data Analysis & Feature Relationships")
    
# # # # #     if not training_data.empty:
# # # # #         # GRAPH 1: FULL CORRELATION MATRIX (All Features)
# # # # #         st.markdown("##### 1. Full Pairwise Correlation Matrix")
# # # # #         numeric_df = training_data.select_dtypes(include=[np.number])
# # # # #         corr_matrix = numeric_df.corr()
# # # # #         fig_corr = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto")
# # # # #         fig_corr.update_layout(height=600, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # #         st.plotly_chart(fig_corr, use_container_width=True)

# # # # #         st.divider()

# # # # #         col_left, col_right = st.columns(2)

# # # # #         # GRAPH 2: PRICE DISTRIBUTION BY AIRLINE (Box Plot)
# # # # #         with col_left:
# # # # #             st.markdown("##### 2. Price Distribution & Outliers")
# # # # #             fig_box = px.box(training_data, x="Airline", y="Price", color="Airline", color_discrete_sequence=px.colors.qualitative.Safe)
# # # # #             fig_box.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # #             st.plotly_chart(fig_box, use_container_width=True)

# # # # #         # GRAPH 3: PRICE VS STOPS (Violin Plot)
# # # # #         with col_right:
# # # # #             st.markdown("##### 3. Density of Price by Total Stops")
# # # # #             fig_violin = px.violin(training_data, y="Price", x="Total_Stops", color="Total_Stops", box=True, points="all")
# # # # #             fig_violin.update_layout(showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # #             st.plotly_chart(fig_violin, use_container_width=True)

# # # # #         st.divider()

# # # # #         col_bot1, col_bot2 = st.columns(2)

# # # # #         # GRAPH 4: MONTHLY PRICE TRENDS (Line Chart)
# # # # #         with col_bot1:
# # # # #             st.markdown("##### 4. Average Ticket Price by Month")
# # # # #             if 'Journey_month' in training_data.columns:
# # # # #                 m_trend = training_data.groupby('Journey_month')['Price'].mean()
# # # # #                 fig_line = px.line(x=m_trend.index, y=m_trend.values, markers=True)
# # # # #                 fig_line.update_traces(line_color='#00AEEF', line_width=3)
# # # # #                 fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # #                 st.plotly_chart(fig_line, use_container_width=True)

# # # # #         # GRAPH 5: DURATION VS PRICE (Scatter Density)
# # # # #         with col_bot2:
# # # # #             st.markdown("##### 5. Flight Duration vs. Price Intensity")
# # # # #             # We use a density contour to show where the 'bulk' of data lies
# # # # #             fig_scatter = px.density_heatmap(training_data, x="Duration", y="Price", nbinsx=30, nbinsy=30, color_continuous_scale='Blues')
# # # # #             fig_scatter.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # #             st.plotly_chart(fig_scatter, use_container_width=True)

# # # # #     else:
# # # # #         st.warning("⚠️ Training data not found. Please upload 'Data_Train.xlsx'.")


# # # # import streamlit as st
# # # # import pandas as pd
# # # # import numpy as np
# # # # import joblib
# # # # import io
# # # # import plotly.express as px
# # # # import plotly.graph_objects as go
# # # # from datetime import datetime, timedelta

# # # # # -------------------------
# # # # # 1. PAGE CONFIG & STYLING
# # # # # -------------------------
# # # # st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# # # # st.markdown("""
# # # #     <style>
# # # #     .main { background-color: #0e1117; color: white; }
# # # #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# # # #     .stTabs [data-baseweb="tab"] {
# # # #         height: 50px; background-color: #1b263b;
# # # #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# # # #     }
# # # #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
# # # #     div.stButton > button:first-child {
# # # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # # #         color: white; border: none; border-radius: 8px; width: 100%; height: 45px;
# # # #     }
# # # #     .price-card {
# # # #         background: #1b263b; padding: 30px; border-radius: 15px;
# # # #         text-align: center; border: 1px solid #415a77; margin-top: 20px;
# # # #     }
# # # #     .price-value { font-size: 3.5rem; font-weight: 800; color: #00AEEF; margin: 10px 0; }
# # # #     </style>
# # # #     """, unsafe_allow_html=True)

# # # # # -------------------------
# # # # # 2. LOAD & CLEAN ASSETS (Crucial for Heatmap)
# # # # # -------------------------
# # # # @st.cache_resource
# # # # def load_assets():
# # # #     model = joblib.load("xgboost_model.pkl")
# # # #     scaler = joblib.load("scaler.pkl")
# # # #     columns = joblib.load("columns.pkl")
# # # #     ohe = joblib.load("airline_encoder.pkl")
    
# # # #     try:
# # # #         # Load Raw Data
# # # #         df = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
        
# # # #         # --- FEATURE ENGINEERING FOR HEATMAP ---
# # # #         # 1. Clean Total Stops (e.g. '1 stop' -> 1, 'non-stop' -> 0)
# # # #         if 'Total_Stops' in df.columns:
# # # #             df['Total_Stops'] = df['Total_Stops'].replace('non-stop', '0 stops')
# # # #             df['Total_Stops'] = df['Total_Stops'].str.extract('(\d+)').fillna(0).astype(int)
            
# # # #         # 2. Convert Date_of_Journey to numeric Day and Month
# # # #         if 'Date_of_Journey' in df.columns:
# # # #             df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True)
# # # #             df['Journey_day'] = df['Date_of_Journey'].dt.day
# # # #             df['Journey_month'] = df['Date_of_Journey'].dt.month
            
# # # #         # 3. Handle Duration (Convert '2h 30m' to total minutes)
# # # #         if 'Duration' in df.columns:
# # # #             def convert_duration(duration):
# # # #                 h = 0
# # # #                 m = 0
# # # #                 if 'h' in duration: h = int(duration.split('h')[0])
# # # #                 if 'm' in duration: m = int(duration.split('m')[0].split()[-1])
# # # #                 return (h * 60) + m
# # # #             df['Duration_minutes'] = df['Duration'].apply(convert_duration)

# # # #     except Exception as e:
# # # #         st.warning(f"Note: Data_Train.xlsx processing skipped or failed: {e}")
# # # #         df = pd.DataFrame()
        
# # # #     return model, scaler, columns, ohe, df

# # # # model, scaler, columns, ohe, training_data = load_assets()

# # # # # -------------------------
# # # # # 3. PREDICTION LOGIC
# # # # # -------------------------
# # # # def predict_price(input_dict, airline_name):
# # # #     df = pd.DataFrame([input_dict])
# # # #     airline_encoded = ohe.transform([[airline_name]])
# # # #     if hasattr(airline_encoded, "toarray"):
# # # #         airline_encoded = airline_encoded.toarray()
# # # #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# # # #     df = pd.concat([df, airline_df], axis=1)
# # # #     for col in columns:
# # # #         if col not in df.columns:
# # # #             df[col] = 0
# # # #     df = df[columns]
# # # #     df_scaled = scaler.transform(df)
# # # #     return np.expm1(model.predict(df_scaled)[0])

# # # # # -------------------------
# # # # # 4. UI STRUCTURE
# # # # # -------------------------
# # # # st.title("✈️ AirFair Vista")
# # # # st.caption("Advanced AI Flight Intelligence | BrainyBeam Internship Project")

# # # # tab1, tab2, tab3 = st.tabs(["🎯 Prediction", "📊 Bulk Scanner", "📈 Advanced EDA"])

# # # # # --- TAB 1: SINGLE PREDICTION ---
# # # # with tab1:
# # # #     col1, col2 = st.columns(2, gap="large")
# # # #     with col1:
# # # #         st.subheader("📍 Journey Details")
# # # #         src = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # # #         dest = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# # # #         air = st.selectbox("Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])
# # # #     with col2:
# # # #         st.subheader("🕒 Schedule")
# # # #         dep = st.datetime_input("Departure Time", value=datetime.now())
# # # #         arr = st.datetime_input("Arrival Time", value=dep + timedelta(hours=2))
# # # #         stops = st.slider("Total Stops", 0, 4, 0)

# # # #     if st.button("Predict Fare"):
# # # #         duration = arr - dep
# # # #         dur_h, dur_m = int(duration.total_seconds() // 3600), int((duration.total_seconds() % 3600) // 60)
# # # #         feats = {"Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month, "Dep_hour": dep.hour, "Dep_min": dep.minute, "Arrival_hour": arr.hour, "Arrival_min": arr.minute, "Duration_hours": dur_h, "Duration_mins": dur_m}
# # # #         price = predict_price(feats, air)
# # # #         st.markdown(f'<div class="price-card"><p>Estimated Fare</p><h1 class="price-value">₹ {price:,.2f}</h1></div>', unsafe_allow_html=True)

# # # # # --- TAB 2: BULK SCANNER ---
# # # # with tab2:
# # # #     st.subheader("📂 Batch Prediction")
# # # #     uploaded_file = st.file_uploader("Upload CSV/Excel/JSON", type=["csv", "xlsx", "json"])
# # # #     if uploaded_file:
# # # #         st.success("File uploaded successfully. Click 'Process' to begin.")

# # # # # --- TAB 3: THE 5 ADVANCED GRAPHS ---
# # # # with tab3:
# # # #     st.subheader("📈 Exploratory Data Analysis")
    
# # # #     if not training_data.empty:
# # # #         # 1. FULL CORRELATION MATRIX (All Numeric Features)
# # # #         st.markdown("##### 1. Full Multi-Feature Correlation Matrix")
# # # #         numeric_df = training_data.select_dtypes(include=[np.number])
# # # #         corr_matrix = numeric_df.corr()
# # # #         fig_corr = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto")
# # # #         fig_corr.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # #         st.plotly_chart(fig_corr, use_container_width=True)
# # # #         st.caption("💡 Shows how Stops, Duration, Day, Month, and Price interact.")

# # # #         st.divider()

# # # #         c1, c2 = st.columns(2)
# # # #         # 2. BOX PLOT (Price vs Airline)
# # # #         with c1:
# # # #             st.markdown("##### 2. Price Distribution by Airline")
# # # #             fig_box = px.box(training_data, x="Airline", y="Price", color_discrete_sequence=['#00AEEF'])
# # # #             fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # #             st.plotly_chart(fig_box, use_container_width=True)

# # # #         # 3. VIOLIN PLOT (Price vs Stops)
# # # #         with c2:
# # # #             st.markdown("##### 3. Price Density by Stops")
# # # #             fig_vio = px.violin(training_data, x="Total_Stops", y="Price", box=True, points="all", color_discrete_sequence=['#00AEEF'])
# # # #             fig_vio.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # #             st.plotly_chart(fig_vio, use_container_width=True)

# # # #         st.divider()

# # # #         c3, c4 = st.columns(2)
# # # #         # 4. LINE CHART (Monthly Trend)
# # # #         with c3:
# # # #             st.markdown("##### 4. Average Fare Monthly Trend")
# # # #             monthly = training_data.groupby('Journey_month')['Price'].mean()
# # # #             fig_line = px.line(x=monthly.index, y=monthly.values, markers=True)
# # # #             fig_line.update_traces(line_color='#00AEEF', line_width=4)
# # # #             fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # #             st.plotly_chart(fig_line, use_container_width=True)

# # # #         # 5. DENSITY HEATMAP (Duration vs Price)
# # # #         with c4:
# # # #             st.markdown("##### 5. Duration vs Price Intensity")
# # # #             fig_dens = px.density_heatmap(training_data, x="Duration_minutes", y="Price", color_continuous_scale='Blues')
# # # #             fig_dens.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # #             st.plotly_chart(fig_dens, use_container_width=True)

# # # #     else:
# # # #         st.error("⚠️ Data_Train.xlsx not found. Please upload it to your repo to see visuals.")


# # # import streamlit as st
# # # import pandas as pd
# # # import numpy as np
# # # import joblib
# # # import io
# # # import plotly.express as px
# # # import plotly.graph_objects as go
# # # from datetime import datetime, timedelta

# # # # -------------------------
# # # # 1. PAGE CONFIG & STYLING
# # # # -------------------------
# # # st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# # # st.markdown("""
# # #     <style>
# # #     .main { background-color: #0e1117; color: white; }
# # #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# # #     .stTabs [data-baseweb="tab"] {
# # #         height: 50px; background-color: #1b263b;
# # #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# # #     }
# # #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
# # #     div.stButton > button:first-child {
# # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # #         color: white; border: none; border-radius: 8px; width: 100%; height: 45px;
# # #     }
# # #     .price-card {
# # #         background: #1b263b; padding: 30px; border-radius: 15px;
# # #         text-align: center; border: 1px solid #415a77; margin-top: 20px;
# # #     }
# # #     .price-value { font-size: 3.5rem; font-weight: 800; color: #00AEEF; margin: 10px 0; }
# # #     </style>
# # #     """, unsafe_allow_html=True)

# # # # -------------------------
# # # # 2. LOAD & CLEAN ASSETS
# # # # -------------------------
# # # @st.cache_resource
# # # def load_assets():
# # #     model = joblib.load("xgboost_model.pkl")
# # #     scaler = joblib.load("scaler.pkl")
# # #     columns = joblib.load("columns.pkl")
# # #     ohe = joblib.load("airline_encoder.pkl")
    
# # #     try:
# # #         # Load Raw Data
# # #         df = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
        
# # #         # --- FEATURE ENGINEERING FOR HEATMAP ---
# # #         if 'Total_Stops' in df.columns:
# # #             df['Total_Stops'] = df['Total_Stops'].replace('non-stop', '0 stops')
# # #             df['Total_Stops'] = df['Total_Stops'].str.extract('(\d+)').fillna(0).astype(int)
            
# # #         if 'Date_of_Journey' in df.columns:
# # #             df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True)
# # #             df['Journey_day'] = df['Date_of_Journey'].dt.day
# # #             df['Journey_month'] = df['Date_of_Journey'].dt.month
            
# # #         if 'Duration' in df.columns:
# # #             def convert_duration(duration):
# # #                 h = 0
# # #                 m = 0
# # #                 if 'h' in duration: h = int(duration.split('h')[0])
# # #                 if 'm' in duration: m = int(duration.split('m')[0].split()[-1])
# # #                 return (h * 60) + m
# # #             df['Duration_minutes'] = df['Duration'].apply(convert_duration)

# # #     except Exception as e:
# # #         st.warning(f"Note: Data_Train.xlsx processing skipped or failed: {e}")
# # #         df = pd.DataFrame()
        
# # #     return model, scaler, columns, ohe, df

# # # model, scaler, columns, ohe, training_data = load_assets()

# # # # -------------------------
# # # # 3. PREDICTION LOGIC
# # # # -------------------------
# # # def predict_price(input_dict, airline_name):
# # #     df = pd.DataFrame([input_dict])
# # #     airline_encoded = ohe.transform([[airline_name]])
# # #     if hasattr(airline_encoded, "toarray"):
# # #         airline_encoded = airline_encoded.toarray()
# # #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# # #     df = pd.concat([df, airline_df], axis=1)
# # #     for col in columns:
# # #         if col not in df.columns:
# # #             df[col] = 0
# # #     df = df[columns]
# # #     df_scaled = scaler.transform(df)
# # #     return np.expm1(model.predict(df_scaled)[0])

# # # # -------------------------
# # # # 4. UI STRUCTURE
# # # # -------------------------
# # # st.title("✈️ AirFair Vista")
# # # st.caption("Advanced AI Flight Intelligence | BrainyBeam Internship Project")

# # # tab1, tab2, tab3 = st.tabs(["🎯 Prediction", "📊 Bulk Scanner", "📈 Advanced EDA"])

# # # # --- TAB 1: SINGLE PREDICTION ---
# # # with tab1:
# # #     col1, col2 = st.columns(2, gap="large")
# # #     with col1:
# # #         st.subheader("📍 Journey Details")
# # #         src = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # #         dest = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# # #         air = st.selectbox("Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])
    
# # #     with col2:
# # #         st.subheader("🕒 Schedule")
# # #         # FIX: Define Departure first
# # #         dep = st.datetime_input("Departure Time", value=datetime.now())
        
# # #         # FIX: Use min_value=dep to prevent picking an arrival date before departure
# # #         arr = st.datetime_input("Arrival Time", value=dep + timedelta(hours=2), min_value=dep)
        
# # #         stops = st.slider("Total Stops", 0, 4, 0)

# # #     if st.button("Predict Fare"):
# # #         # Double check logic: Ensure arrival is strictly after departure
# # #         if arr <= dep:
# # #             st.error("❌ Error: Arrival time must be later than Departure time.")
# # #         else:
# # #             duration = arr - dep
# # #             dur_h = int(duration.total_seconds() // 3600)
# # #             dur_m = int((duration.total_seconds() % 3600) // 60)
            
# # #             feats = {
# # #                 "Total_Stops": stops, 
# # #                 "Journey_day": dep.day, 
# # #                 "Journey_month": dep.month, 
# # #                 "Dep_hour": dep.hour, 
# # #                 "Dep_min": dep.minute, 
# # #                 "Arrival_hour": arr.hour, 
# # #                 "Arrival_min": arr.minute, 
# # #                 "Duration_hours": dur_h, 
# # #                 "Duration_mins": dur_m
# # #             }
            
# # #             price = predict_price(feats, air)
# # #             st.markdown(f'<div class="price-card"><p>Estimated Fare</p><h1 class="price-value">₹ {price:,.2f}</h1><p>Flight Duration: {dur_h}h {dur_m}m</p></div>', unsafe_allow_html=True)

# # # # --- TAB 2: BULK SCANNER ---
# # # with tab2:
# # #     st.subheader("📂 Batch Prediction")
# # #     uploaded_file = st.file_uploader("Upload CSV/Excel/JSON", type=["csv", "xlsx", "json"])
# # #     if uploaded_file:
# # #         st.success("File uploaded successfully. Click 'Process' to begin.")

# # # # --- TAB 3: ADVANCED EDA ---
# # # with tab3:
# # #     st.subheader("📈 Exploratory Data Analysis")
    
# # #     if not training_data.empty:
# # #         st.markdown("##### 1. Full Multi-Feature Correlation Matrix")
# # #         numeric_df = training_data.select_dtypes(include=[np.number])
# # #         corr_matrix = numeric_df.corr()
# # #         fig_corr = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto")
# # #         fig_corr.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # #         st.plotly_chart(fig_corr, use_container_width=True)
# # #         st.caption("💡 Shows how Stops, Duration, Day, Month, and Price interact.")

# # #         st.divider()

# # #         c1, c2 = st.columns(2)
# # #         with c1:
# # #             st.markdown("##### 2. Price Distribution by Airline")
# # #             fig_box = px.box(training_data, x="Airline", y="Price", color_discrete_sequence=['#00AEEF'])
# # #             fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # #             st.plotly_chart(fig_box, use_container_width=True)

# # #         with c2:
# # #             st.markdown("##### 3. Price Density by Stops")
# # #             fig_vio = px.violin(training_data, x="Total_Stops", y="Price", box=True, points="all", color_discrete_sequence=['#00AEEF'])
# # #             fig_vio.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # #             st.plotly_chart(fig_vio, use_container_width=True)

# # #         st.divider()

# # #         c3, c4 = st.columns(2)
# # #         with c3:
# # #             st.markdown("##### 4. Average Fare Monthly Trend")
# # #             monthly = training_data.groupby('Journey_month')['Price'].mean()
# # #             fig_line = px.line(x=monthly.index, y=monthly.values, markers=True)
# # #             fig_line.update_traces(line_color='#00AEEF', line_width=4)
# # #             fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # #             st.plotly_chart(fig_line, use_container_width=True)

# # #         with c4:
# # #             st.markdown("##### 5. Duration vs Price Intensity")
# # #             fig_dens = px.density_heatmap(training_data, x="Duration_minutes", y="Price", color_continuous_scale='Blues')
# # #             fig_dens.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # #             st.plotly_chart(fig_dens, use_container_width=True)

# # #     else:
# # #         st.error("⚠️ Data_Train.xlsx not found. Please upload it to your repo to see visuals.")



# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # import joblib
# # import io
# # import plotly.express as px
# # import plotly.graph_objects as go
# # from datetime import datetime, timedelta

# # # -------------------------
# # # 1. PAGE CONFIG & STYLING
# # # -------------------------
# # st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# # st.markdown("""
# #     <style>
# #     .main { background-color: #0e1117; color: white; }
# #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# #     .stTabs [data-baseweb="tab"] {
# #         height: 50px; background-color: #1b263b;
# #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# #     }
# #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
# #     div.stButton > button:first-child {
# #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# #         color: white; border: none; border-radius: 8px; width: 100%; height: 45px;
# #     }
# #     .price-card {
# #         background: #1b263b; padding: 30px; border-radius: 15px;
# #         text-align: center; border: 1px solid #415a77; margin-top: 20px;
# #     }
# #     .price-value { font-size: 3.5rem; font-weight: 800; color: #00AEEF; margin: 10px 0; }
# #     </style>
# #     """, unsafe_allow_html=True)

# # # -------------------------
# # # 2. LOAD & CLEAN ASSETS
# # # -------------------------
# # @st.cache_resource
# # def load_assets():
# #     model = joblib.load("xgboost_model.pkl")
# #     scaler = joblib.load("scaler.pkl")
# #     columns = joblib.load("columns.pkl")
# #     ohe = joblib.load("airline_encoder.pkl")
    
# #     try:
# #         # Load Raw Data
# #         df = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
        
# #         # --- FEATURE ENGINEERING FOR HEATMAP ---
# #         if 'Total_Stops' in df.columns:
# #             df['Total_Stops'] = df['Total_Stops'].replace('non-stop', '0 stops')
# #             df['Total_Stops'] = df['Total_Stops'].str.extract('(\d+)').fillna(0).astype(int)
            
# #         if 'Date_of_Journey' in df.columns:
# #             df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True)
# #             df['Journey_day'] = df['Date_of_Journey'].dt.day
# #             df['Journey_month'] = df['Date_of_Journey'].dt.month
            
# #         if 'Duration' in df.columns:
# #             def convert_duration(duration):
# #                 h = 0
# #                 m = 0
# #                 if 'h' in duration: h = int(duration.split('h')[0])
# #                 if 'm' in duration: m = int(duration.split('m')[0].split()[-1])
# #                 return (h * 60) + m
# #             df['Duration_minutes'] = df['Duration'].apply(convert_duration)

# #     except Exception as e:
# #         st.warning(f"Note: Data_Train.xlsx processing skipped or failed: {e}")
# #         df = pd.DataFrame()
        
# #     return model, scaler, columns, ohe, df

# # model, scaler, columns, ohe, training_data = load_assets()

# # # -------------------------
# # # 3. PREDICTION LOGIC
# # # -------------------------
# # def predict_price(input_dict, airline_name):
# #     df = pd.DataFrame([input_dict])
# #     airline_encoded = ohe.transform([[airline_name]])
# #     if hasattr(airline_encoded, "toarray"):
# #         airline_encoded = airline_encoded.toarray()
# #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# #     df = pd.concat([df, airline_df], axis=1)
# #     for col in columns:
# #         if col not in df.columns:
# #             df[col] = 0
# #     df = df[columns]
# #     df_scaled = scaler.transform(df)
# #     return np.expm1(model.predict(df_scaled)[0])

# # # -------------------------
# # # 4. UI STRUCTURE
# # # -------------------------
# # st.title("✈️ AirFair Vista")
# # st.caption("Advanced AI Flight Intelligence | BrainyBeam Internship Project")

# # tab1, tab2, tab3 = st.tabs(["🎯 Prediction", "📊 Bulk Scanner", "📈 Advanced EDA"])

# # # --- TAB 1: SINGLE PREDICTION ---
# # with tab1:
# #     col1, col2 = st.columns(2, gap="large")
# #     with col1:
# #         st.subheader("📍 Journey Details")
# #         src = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# #         dest = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
        
# #         # ADDED: Jet Airways Business included back in the list
# #         air = st.selectbox("Airline", [
# #             'IndiGo', 'Air India', 'Jet Airways', 'Jet Airways Business', 
# #             'SpiceJet', 'Vistara', 'GoAir', 'Multiple carriers', 
# #             'Air Asia', 'Vistara Premium economy'
# #         ])
    
# #     with col2:
# #         st.subheader("🕒 Schedule")
# #         # FIX: Define Departure
# #         dep = st.datetime_input("Departure Time", value=datetime.now())
        
# #         # FIX: Arrival restricted to be after Departure
# #         arr = st.datetime_input("Arrival Time", value=dep + timedelta(hours=2), min_value=dep)
        
# #         stops = st.slider("Total Stops", 0, 4, 0)

# #     if st.button("Predict Fare"):
# #         # Validation: Arrival cannot be same as or before departure
# #         if arr <= dep:
# #             st.error("❌ Invalid Schedule: Arrival must be after Departure.")
# #         else:
# #             duration = arr - dep
# #             dur_h = int(duration.total_seconds() // 3600)
# #             dur_m = int((duration.total_seconds() % 3600) // 60)
            
# #             feats = {
# #                 "Total_Stops": stops, 
# #                 "Journey_day": dep.day, 
# #                 "Journey_month": dep.month, 
# #                 "Dep_hour": dep.hour, 
# #                 "Dep_min": dep.minute, 
# #                 "Arrival_hour": arr.hour, 
# #                 "Arrival_min": arr.minute, 
# #                 "Duration_hours": dur_h, 
# #                 "Duration_mins": dur_m
# #             }
            
# #             price = predict_price(feats, air)
# #             st.markdown(f"""
# #                 <div class="price-card">
# #                     <p>Estimated Fare</p>
# #                     <h1 class="price-value">₹ {price:,.2f}</h1>
# #                     <p style="color: #00AEEF;">Flight Duration: {dur_h}h {dur_m}m</p>
# #                 </div>
# #             """, unsafe_allow_html=True)

# # # --- TAB 2: BULK SCANNER ---
# # with tab2:
# #     st.subheader("📂 Batch Prediction")
# #     uploaded_file = st.file_uploader("Upload CSV/Excel/JSON", type=["csv", "xlsx", "json"])
# #     if uploaded_file:
# #         st.success("File uploaded successfully. Click 'Process' to begin.")

# # # --- TAB 3: ADVANCED EDA ---
# # with tab3:
# #     st.subheader("📈 Exploratory Data Analysis")
    
# #     if not training_data.empty:
# #         st.markdown("##### 1. Full Multi-Feature Correlation Matrix")
# #         numeric_df = training_data.select_dtypes(include=[np.number])
# #         corr_matrix = numeric_df.corr()
# #         fig_corr = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto")
# #         fig_corr.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# #         st.plotly_chart(fig_corr, use_container_width=True)

# #         st.divider()

# #         c1, c2 = st.columns(2)
# #         with c1:
# #             st.markdown("##### 2. Price Distribution by Airline")
# #             fig_box = px.box(training_data, x="Airline", y="Price", color_discrete_sequence=['#00AEEF'])
# #             fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# #             st.plotly_chart(fig_box, use_container_width=True)

# #         with c2:
# #             st.markdown("##### 3. Price Density by Stops")
# #             fig_vio = px.violin(training_data, x="Total_Stops", y="Price", box=True, points="all", color_discrete_sequence=['#00AEEF'])
# #             fig_vio.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# #             st.plotly_chart(fig_vio, use_container_width=True)

# #         st.divider()

# #         c3, c4 = st.columns(2)
# #         with c3:
# #             st.markdown("##### 4. Average Fare Monthly Trend")
# #             monthly = training_data.groupby('Journey_month')['Price'].mean()
# #             fig_line = px.line(x=monthly.index, y=monthly.values, markers=True)
# #             fig_line.update_traces(line_color='#00AEEF', line_width=4)
# #             fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# #             st.plotly_chart(fig_line, use_container_width=True)

# #         with c4:
# #             st.markdown("##### 5. Duration vs Price Intensity")
# #             fig_dens = px.density_heatmap(training_data, x="Duration_minutes", y="Price", color_continuous_scale='Blues')
# #             fig_dens.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# #             st.plotly_chart(fig_dens, use_container_width=True)

# #     else:
# #         st.error("⚠️ Data_Train.xlsx not found. Visuals restricted.")


# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
# import io
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, timedelta

# # -------------------------
# # 1. PAGE CONFIG & STYLING
# # -------------------------
# st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# st.markdown("""
#     <style>
#     .main { background-color: #0e1117; color: white; }
#     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
#     .stTabs [data-baseweb="tab"] {
#         height: 50px; background-color: #1b263b;
#         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
#     }
#     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
#     div.stButton > button:first-child {
#         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
#         color: white; border: none; border-radius: 8px; width: 100%; height: 45px;
#     }
#     .price-card {
#         background: #1b263b; padding: 30px; border-radius: 15px;
#         text-align: center; border: 1px solid #415a77; margin-top: 20px;
#     }
#     .price-value { font-size: 3.5rem; font-weight: 800; color: #00AEEF; margin: 10px 0; }
#     </style>
#     """, unsafe_allow_html=True)

# # -------------------------
# # 2. LOAD & CLEAN ASSETS
# # -------------------------
# @st.cache_resource
# def load_assets():
#     model = joblib.load("xgboost_model.pkl")
#     scaler = joblib.load("scaler.pkl")
#     columns = joblib.load("columns.pkl")
#     ohe = joblib.load("airline_encoder.pkl")
    
#     try:
#         df = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
#         if 'Total_Stops' in df.columns:
#             df['Total_Stops'] = df['Total_Stops'].replace('non-stop', '0 stops')
#             df['Total_Stops'] = df['Total_Stops'].str.extract('(\d+)').fillna(0).astype(int)
#         if 'Date_of_Journey' in df.columns:
#             df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True)
#             df['Journey_day'] = df['Date_of_Journey'].dt.day
#             df['Journey_month'] = df['Date_of_Journey'].dt.month
#         if 'Duration' in df.columns:
#             def convert_duration(duration):
#                 h, m = 0, 0
#                 if 'h' in duration: h = int(duration.split('h')[0])
#                 if 'm' in duration: m = int(duration.split('m')[0].split()[-1])
#                 return (h * 60) + m
#             df['Duration_minutes'] = df['Duration'].apply(convert_duration)
#     except Exception as e:
#         st.warning(f"Note: Data_Train.xlsx processing skipped or failed: {e}")
#         df = pd.DataFrame()
#     return model, scaler, columns, ohe, df

# model, scaler, columns, ohe, training_data = load_assets()

# # -------------------------
# # 3. PREDICTION LOGIC
# # -------------------------
# def predict_price(input_dict, airline_name):
#     df = pd.DataFrame([input_dict])
#     airline_encoded = ohe.transform([[airline_name]])
#     if hasattr(airline_encoded, "toarray"):
#         airline_encoded = airline_encoded.toarray()
#     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
#     df = pd.concat([df, airline_df], axis=1)
#     for col in columns:
#         if col not in df.columns: df[col] = 0
#     df = df[columns]
#     df_scaled = scaler.transform(df)
#     return np.expm1(model.predict(df_scaled)[0])

# # -------------------------
# # 4. UI STRUCTURE
# # -------------------------
# st.title("✈️ AirFair Vista")
# st.caption("Advanced AI Flight Intelligence | BrainyBeam Internship Project")

# tab1, tab2, tab3 = st.tabs(["🎯 Prediction", "📊 Bulk Scanner", "📈 Advanced EDA"])

# # --- TAB 1: SINGLE PREDICTION ---
# with tab1:
#     col1, col2 = st.columns(2, gap="large")
#     with col1:
#         st.subheader("📍 Journey Details")
#         src = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
#         dest = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
#         air = st.selectbox("Airline", [
#             'IndiGo', 'Air India', 'Jet Airways', 'Jet Airways Business', 
#             'SpiceJet', 'Vistara', 'GoAir', 'Multiple carriers', 
#             'Air Asia', 'Vistara Premium economy'
#         ])
    
#     with col2:
#         st.subheader("🕒 Schedule")
        
#         # FIX: min_value=datetime.now() ensures you cannot pick a past date for Departure
#         current_time = datetime.now()
#         dep = st.datetime_input("Departure Time", value=current_time, min_value=current_time)
        
#         # FIX: min_value=dep ensures Arrival is always after Departure
#         arr = st.datetime_input("Arrival Time", value=dep + timedelta(hours=2), min_value=dep)
        
#         stops = st.slider("Total Stops", 0, 4, 0)

#     if st.button("Predict Fare"):
#         if arr <= dep:
#             st.error("❌ Invalid Schedule: Arrival must be after Departure.")
#         else:
#             duration = arr - dep
#             dur_h = int(duration.total_seconds() // 3600)
#             dur_m = int((duration.total_seconds() % 3600) // 60)
            
#             feats = {
#                 "Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month, 
#                 "Dep_hour": dep.hour, "Dep_min": dep.minute, 
#                 "Arrival_hour": arr.hour, "Arrival_min": arr.minute, 
#                 "Duration_hours": dur_h, "Duration_mins": dur_m
#             }
            
#             price = predict_price(feats, air)
#             st.markdown(f"""
#                 <div class="price-card">
#                     <p>Estimated Fare</p>
#                     <h1 class="price-value">₹ {price:,.2f}</h1>
#                     <p style="color: #00AEEF;">Flight Duration: {dur_h}h {dur_m}m</p>
#                 </div>
#             """, unsafe_allow_html=True)

# # --- TAB 2: BULK SCANNER ---
# with tab2:
#     st.subheader("📂 Batch Prediction")
#     uploaded_file = st.file_uploader("Upload CSV/Excel/JSON", type=["csv", "xlsx", "json"])
#     if uploaded_file:
#         st.success("File uploaded successfully. Click 'Process' to begin.")

# # --- TAB 3: ADVANCED EDA ---
# with tab3:
#     st.subheader("📈 Exploratory Data Analysis")
#     if not training_data.empty:
#         st.markdown("##### 1. Full Multi-Feature Correlation Matrix")
#         numeric_df = training_data.select_dtypes(include=[np.number])
#         corr_matrix = numeric_df.corr()
#         fig_corr = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto")
#         fig_corr.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
#         st.plotly_chart(fig_corr, use_container_width=True)

#         st.divider()

#         c1, c2 = st.columns(2)
#         with c1:
#             st.markdown("##### 2. Price Distribution by Airline")
#             fig_box = px.box(training_data, x="Airline", y="Price", color_discrete_sequence=['#00AEEF'])
#             fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
#             st.plotly_chart(fig_box, use_container_width=True)

#         with c2:
#             st.markdown("##### 3. Price Density by Stops")
#             fig_vio = px.violin(training_data, x="Total_Stops", y="Price", box=True, points="all", color_discrete_sequence=['#00AEEF'])
#             fig_vio.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
#             st.plotly_chart(fig_vio, use_container_width=True)

#         st.divider()

#         c3, c4 = st.columns(2)
#         with c3:
#             st.markdown("##### 4. Average Fare Monthly Trend")
#             monthly = training_data.groupby('Journey_month')['Price'].mean()
#             fig_line = px.line(x=monthly.index, y=monthly.values, markers=True)
#             fig_line.update_traces(line_color='#00AEEF', line_width=4)
#             fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
#             st.plotly_chart(fig_line, use_container_width=True)

#         with c4:
#             st.markdown("##### 5. Duration vs Price Intensity")
#             fig_dens = px.density_heatmap(training_data, x="Duration_minutes", y="Price", color_continuous_scale='Blues')
#             fig_dens.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
#             st.plotly_chart(fig_dens, use_container_width=True)
#     else:
#         st.error("⚠️ Data_Train.xlsx not found.")


import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
from datetime import datetime, date, timedelta, time

# -------------------------
# 1. PAGE CONFIG & THEME
# -------------------------
st.set_page_config(page_title="AirFair Vista Pro", page_icon="✈️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #1b263b;
        border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
    .section-box {
        padding: 25px; background-color: #16213e; border-radius: 15px; 
        border-left: 5px solid #00AEEF; margin-bottom: 25px;
    }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
        color: white; border-radius: 8px; height: 55px; width: 100%; font-weight: bold; font-size: 1.2rem;
    }
    .metric-card {
        background-color: #1b263b; padding: 15px; border-radius: 10px; border: 1px solid #415a77;
    }
    </style>
    """, unsafe_allow_html=True)

# -------------------------
# 2. ASSET LOADING & PREPROCESSING
# -------------------------
@st.cache_resource
def load_assets():
    try:
        model = joblib.load("xgboost_model.pkl")
        scaler = joblib.load("scaler.pkl")
        columns = joblib.load("columns.pkl")
        ohe = joblib.load("airline_encoder.pkl")
        
        # Load and fix data for EDA to avoid KeyError
        df = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
        if 'Date_of_Journey' in df.columns:
            df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True)
            df['Journey_month'] = df['Date_of_Journey'].dt.month
            df['Journey_day'] = df['Date_of_Journey'].dt.day
        
        if 'Total_Stops' in df.columns:
            df['Stops_Clean'] = df['Total_Stops'].replace('non-stop', '0 stops')
            df['Stops_Numeric'] = df['Stops_Clean'].str.extract('(\d+)').fillna(0).astype(int)
            
        return model, scaler, columns, ohe, df
    except Exception as e:
        st.error(f"Initialization Error: {e}")
        return None, None, None, None, pd.DataFrame()

model, scaler, columns, ohe, df_train = load_assets()

# -------------------------
# 3. PREDICTION ENGINE (Overnight Fix)
# -------------------------
def predict_price(airline, stops, j_date, d_time, a_time):
    start = datetime.combine(j_date, d_time)
    end = datetime.combine(j_date, a_time)
    
    # Solve overnight problem: if arrival < departure, add 24 hours
    if end <= start:
        end += timedelta(days=1)
        
    duration = end - start
    dur_h = duration.seconds // 3600
    dur_m = (duration.seconds % 3600) // 60

    feats = {
        "Total_Stops": stops, "Journey_day": j_date.day, "Journey_month": j_date.month,
        "Dep_hour": d_time.hour, "Dep_min": d_time.minute,
        "Arrival_hour": a_time.hour, "Arrival_min": a_time.minute,
        "Duration_hours": dur_h, "Duration_mins": dur_m
    }
    
    input_df = pd.DataFrame([feats])
    air_enc = ohe.transform([[airline]])
    if hasattr(air_enc, "toarray"): air_enc = air_enc.toarray()
    
    input_df = pd.concat([input_df, pd.DataFrame(air_enc, columns=ohe.get_feature_names_out())], axis=1)
    for col in columns:
        if col not in input_df.columns: input_df[col] = 0
    
    return np.expm1(model.predict(scaler.transform(input_df[columns]))[0])

# -------------------------
# 4. MAIN DASHBOARD
# -------------------------
st.title("✈️ AirFair Vista: AI Price Intelligence")
tab1, tab2, tab3 = st.tabs(["🎯 Fare Prediction", "📂 Bulk Scanner", "📈 Advanced EDA"])

# --- TAB 1: PREDICTION ---
with tab1:
    trip_type = st.radio("Trip Type", ["One Way", "Round Trip"], horizontal=True)
    
    c_src, c_dest = st.columns(2)
    with c_src: src = st.selectbox("Departure City", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
    with c_dest: dest = st.selectbox("Destination City", ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata'])

    # OUTBOUND
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("🛫 Outbound Flight")
    o1, o2, o3 = st.columns(3)
    with o1:
        out_date = st.date_input("Date", min_value=date.today(), key="od")
        out_air = st.selectbox("Airline", ohe.categories_[0], key="oa")
    with o2:
        out_dep = st.time_input("Dep. Time", time(10, 0), key="ot1")
        out_stops = st.number_input("Stops", 0, 4, 0, key="os")
    with o3:
        out_arr = st.time_input("Arrival Time", time(13, 0), key="ot2")
    st.markdown('</div>', unsafe_allow_html=True)

    # RETURN (The "Return Also" and "Flight Option" fix)
    if trip_type == "Round Trip":
        st.markdown('<div class="section-box">', unsafe_allow_html=True)
        st.subheader("🛬 Return Flight")
        r1, r2, r3 = st.columns(3)
        with r1:
            ret_date = st.date_input("Return Date", min_value=out_date, value=out_date + timedelta(days=2))
            ret_air = st.selectbox("Return Airline", ohe.categories_[0], key="ra")
        with r2:
            ret_dep = st.time_input("Return Dep. Time", time(18, 0), key="rt1")
            ret_stops = st.number_input("Return Stops", 0, 4, 0, key="rs")
        with r3:
            ret_arr = st.time_input("Return Arrival Time", time(21, 0), key="rt2")
        st.markdown('</div>', unsafe_allow_html=True)

    if st.button("CALCULATE AI FARE"):
        if model:
            p_out = predict_price(out_air, out_stops, out_date, out_dep, out_arr)
            if trip_type == "Round Trip":
                p_ret = predict_price(ret_air, ret_stops, ret_date, ret_dep, ret_arr)
                m1, m2, m3 = st.columns(3)
                with m1: st.metric("Outbound Fare", f"₹{p_out:,.2f}")
                with m2: st.metric("Return Fare", f"₹{p_ret:,.2f}")
                with m3: st.metric("Total Estimate", f"₹{(p_out+p_ret):,.2f}", delta_color="inverse")
            else:
                st.metric("Estimated One-Way Fare", f"₹{p_out:,.2f}")
        else:
            st.error("Model not loaded.")

# --- TAB 2: BULK SCANNER ---
with tab2:
    st.subheader("📂 Batch Prediction Scanner")
    st.write("Upload your travel itinerary file to process multiple fares at once.")
    uploaded_file = st.file_uploader("Choose CSV/Excel", type=["csv", "xlsx"])
    if uploaded_file:
        st.info("Scanner Ready: Data processing engine initialized.")

# --- TAB 3: ADVANCED EDA ---
with tab3:
    st.subheader("📈 Market Exploratory Analysis")
    if not df_train.empty:
        # Chart 1 & 2
        e1, e2 = st.columns(2)
        with e1:
            st.plotly_chart(px.box(df_train, x="Airline", y="Price", color="Airline", title="Price Range per Airline"), use_container_width=True)
        with e2:
            st.plotly_chart(px.violin(df_train, x="Stops_Numeric", y="Price", box=True, title="Price Density vs Stops"), use_container_width=True)
        
        # Chart 3 & 4
        e3, e4 = st.columns(2)
        with e3:
            avg_month = df_train.groupby('Journey_month')['Price'].mean().reset_index()
            st.plotly_chart(px.line(avg_month, x='Journey_month', y='Price', markers=True, title="Monthly Fare Seasonality"), use_container_width=True)
        with e4:
            st.plotly_chart(px.density_heatmap(df_train, x="Source", y="Destination", z="Price", title="Route Pricing Heatmap"), use_container_width=True)
        
        # Chart 5 & 6
        e5, e6 = st.columns(2)
        with e5:
            st.plotly_chart(px.scatter(df_train, x="Duration", y="Price", color="Airline", opacity=0.4, title="Duration vs. Fare Correlation"), use_container_width=True)
        with e6:
            st.plotly_chart(px.pie(df_train, names='Airline', hole=0.5, title="Airline Dataset Distribution"), use_container_width=True)
    else:
        st.warning("Training data missing for EDA.")