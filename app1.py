# # # import streamlit as st
# # # import pandas as pd
# # # import numpy as np
# # # import joblib
# # # import io
# # # from datetime import datetime, timedelta

# # # # -------------------------
# # # # 1. PAGE CONFIG & STYLING
# # # # -------------------------
# # # st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# # # # Professional CSS for Dark Mode and Custom Cards
# # # st.markdown("""
# # #     <style>
# # #     .main { background-color: #0e1117; color: white; }
# # #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# # #     .stTabs [data-baseweb="tab"] {
# # #         height: 50px; white-space: pre-wrap; background-color: #1b263b;
# # #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# # #     }
# # #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
# # #     div.stButton > button:first-child {
# # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # #         color: white; border: none; padding: 12px; border-radius: 8px; width: 100%;
# # #     }
# # #     .price-card {
# # #         background: #1b263b; padding: 30px; border-radius: 15px;
# # #         text-align: center; border: 1px solid #415a77; margin-bottom: 20px;
# # #     }
# # #     .price-value { font-size: 3rem; font-weight: 800; color: #00AEEF; }
# # #     </style>
# # #     """, unsafe_allow_html=True)

# # # # -------------------------
# # # # 2. LOAD AI ASSETS
# # # # -------------------------
# # # @st.cache_resource
# # # def load_assets():
# # #     model = joblib.load("xgboost_model.pkl")
# # #     scaler = joblib.load("scaler.pkl")
# # #     columns = joblib.load("columns.pkl")
# # #     ohe = joblib.load("airline_encoder.pkl")
# # #     return model, scaler, columns, ohe

# # # try:
# # #     model, scaler, columns, ohe = load_assets()
# # # except Exception as e:
# # #     st.error(f"🚨 Model files missing: {e}")
# # #     st.stop()

# # # # -------------------------
# # # # 3. HELPER FUNCTION: PREPROCESS
# # # # -------------------------
# # # def process_data(input_dict, airline_name):
# # #     df = pd.DataFrame([input_dict])
    
# # #     # One-hot encode airline
# # #     airline_encoded = ohe.transform([[airline_name]])
# # #     if hasattr(airline_encoded, "toarray"):
# # #         airline_encoded = airline_encoded.toarray()
    
# # #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# # #     df = pd.concat([df, airline_df], axis=1)

# # #     # Ensure all columns exist and are in the correct order
# # #     for col in columns:
# # #         if col not in df.columns:
# # #             df[col] = 0
# # #     df = df[columns]
    
# # #     # Scale and Predict
# # #     df_scaled = scaler.transform(df)
# # #     log_pred = model.predict(df_scaled)
# # #     return np.expm1(log_pred[0]) # Reverse Log transformation

# # # # -------------------------
# # # # 4. MAIN UI - TABS
# # # # -------------------------
# # # st.title("✈️ AirFair Vista")
# # # st.caption("Advanced AI Flight Fare Prediction System | Powered by XGBoost")

# # # tab1, tab2 = st.tabs(["🎯 Single Prediction", "📊 Bulk Scanner"])

# # # # --- TAB 1: SINGLE PREDICTION ---
# # # with tab1:
# # #     col1, col2 = st.columns(2, gap="large")
# # #     with col1:
# # #         st.subheader("📍 Journey Details")
# # #         src = st.selectbox("Source City", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # #         dest = st.selectbox("Destination City", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# # #         air = st.selectbox("Select Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])

# # #     with col2:
# # #         st.subheader("🕒 Schedule")
# # #         dep = st.datetime_input("Departure Date & Time", value=datetime.now())
# # #         arr = st.datetime_input("Arrival Date & Time", value=dep + timedelta(hours=2))
# # #         stops = st.slider("Number of Stops", 0, 4, 0)

# # #     if st.button("Calculate Estimated Fare"):
# # #         if arr <= dep:
# # #             st.error("Arrival must be after Departure!")
# # #         else:
# # #             duration = arr - dep
# # #             dur_h = int(duration.total_seconds() // 3600)
# # #             dur_m = int((duration.total_seconds() % 3600) // 60)
            
# # #             input_features = {
# # #                 "Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month,
# # #                 "Dep_hour": dep.hour, "Dep_min": dep.minute, "Arrival_hour": arr.hour,
# # #                 "Arrival_min": arr.minute, "Duration_hours": dur_h, "Duration_mins": dur_m
# # #             }
            
# # #             final_price = process_data(input_features, air)
            
# # #             st.markdown(f"""
# # #                 <div class="price-card">
# # #                     <p style="color:#778da9; margin-bottom:0;">Estimated Ticket Price</p>
# # #                     <h1 class="price-value">₹ {final_price:,.2f}</h1>
# # #                     <p style="font-size:0.9rem;">{air} | {src} → {dest}</p>
# # #                 </div>
# # #             """, unsafe_allow_html=True)
# # #             st.balloons()

# # # # --- TAB 2: BULK SCANNER ---
# # # with tab2:
# # #     st.subheader("📂 Bulk Flight Price Analysis")
# # #     st.info("Upload a CSV with columns: Airline, Source, Destination, Dep_Time, Arrival_Time, Total_Stops")
    
# # #     upload_col, info_col = st.columns([2, 1])
    
# # #     with upload_col:
# # #         uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
# # #     with info_col:
# # #         # Template Download
# # #         sample = pd.DataFrame({
# # #             'Airline': ['IndiGo'], 'Source': ['Delhi'], 'Destination': ['Cochin'],
# # #             'Dep_Time': ['2026-05-10 10:00'], 'Arrival_Time': ['2026-05-10 13:00'], 'Total_Stops': [0]
# # #         })
# # #         st.download_button("📩 Download CSV Template", sample.to_csv(index=False), "template.csv")

# # #     if uploaded_file:
# # #         df_bulk = pd.read_csv(uploaded_file)
# # #         if st.button("🚀 Run Bulk Prediction"):
# # #             with st.spinner("Analyzing flights..."):
# # #                 prices = []
# # #                 # Simple loop for demo; for huge files, use a vectorized approach
# # #                 for _, row in df_bulk.iterrows():
# # #                     try:
# # #                         d_t = pd.to_datetime(row['Dep_Time'])
# # #                         a_t = pd.to_datetime(row['Arrival_Time'])
# # #                         diff = a_t - d_t
# # #                         feats = {
# # #                             "Total_Stops": row['Total_Stops'], "Journey_day": d_t.day, "Journey_month": d_t.month,
# # #                             "Dep_hour": d_t.hour, "Dep_min": d_t.minute, "Arrival_hour": a_t.hour,
# # #                             "Arrival_min": a_t.minute, "Duration_hours": int(diff.total_seconds()//3600),
# # #                             "Duration_mins": int((diff.total_seconds()%3600)//60)
# # #                         }
# # #                         prices.append(round(process_data(feats, row['Airline']), 2))
# # #                     except:
# # #                         prices.append(np.nan)
                
# # #                 df_bulk['Predicted_Price'] = prices
# # #                 st.write("### Preview of Results", df_bulk.head())
# # #                 st.download_button("📥 Download Results", df_bulk.to_csv(index=False), "predictions.csv")



# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # import joblib
# # import io
# # import json
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
# #         color: white; border: none; border-radius: 8px; width: 100%;
# #     }
# #     .price-card {
# #         background: #1b263b; padding: 30px; border-radius: 15px;
# #         text-align: center; border: 1px solid #415a77;
# #     }
# #     .price-value { font-size: 3rem; font-weight: 800; color: #00AEEF; }
# #     </style>
# #     """, unsafe_allow_html=True)

# # # -------------------------
# # # 2. LOAD ASSETS
# # # -------------------------
# # @st.cache_resource
# # def load_assets():
# #     model = joblib.load("xgboost_model.pkl")
# #     scaler = joblib.load("scaler.pkl")
# #     columns = joblib.load("columns.pkl")
# #     ohe = joblib.load("airline_encoder.pkl")
# #     # Load raw data for EDA tab (Update filename to your actual training data)
# #     try:
# #         raw_data = pd.read_excel("Data_Train.xlsx") 
# #     except:
# #         raw_data = pd.DataFrame() 
# #     return model, scaler, columns, ohe, raw_data

# # model, scaler, columns, ohe, training_data = load_assets()

# # # -------------------------
# # # 3. LOGIC FUNCTIONS
# # # -------------------------
# # def process_data(input_dict, airline_name):
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
# # # 4. MAIN UI - TABS
# # # -------------------------
# # st.title("✈️ AirFair Vista")
# # st.caption("Advanced AI Flight Fare Prediction System | BrainyBeam Internship Project")

# # tab1, tab2, tab3 = st.tabs(["🎯 Single Prediction", "📊 Bulk Scanner", "📈 Dataset EDA"])

# # # --- TAB 1: SINGLE PREDICTION ---
# # with tab1:
# #     col1, col2 = st.columns(2, gap="large")
# #     with col1:
# #         st.subheader("📍 Journey Details")
# #         src = st.selectbox("Source City", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# #         dest = st.selectbox("Destination City", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# #         air = st.selectbox("Select Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])
# #     with col2:
# #         st.subheader("🕒 Schedule")
# #         dep = st.datetime_input("Departure Time", value=datetime.now())
# #         arr = st.datetime_input("Arrival Time", value=dep + timedelta(hours=2))
# #         stops = st.slider("Number of Stops", 0, 4, 0)

# #     if st.button("Calculate Fare"):
# #         duration = arr - dep
# #         dur_h, dur_m = int(duration.total_seconds() // 3600), int((duration.total_seconds() % 3600) // 60)
# #         feats = {"Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month, "Dep_hour": dep.hour, "Dep_min": dep.minute, "Arrival_hour": arr.hour, "Arrival_min": arr.minute, "Duration_hours": dur_h, "Duration_mins": dur_m}
# #         price = process_data(feats, air)
# #         st.markdown(f'<div class="price-card"><p>Estimated Fare</p><h1 class="price-value">₹ {price:,.2f}</h1></div>', unsafe_allow_html=True)

# # # --- TAB 2: BULK SCANNER (UPDATED PER FEEDBACK) ---
# # with tab2:
# #     st.subheader("📂 Bulk Analysis")
    
# #     # 1. Multi-format Sample Downloads
# #     st.markdown("##### 1. Download Samples")
# #     s_col1, s_col2, s_col3 = st.columns(3)
# #     sample_df = pd.DataFrame({'Airline':['IndiGo'], 'Source':['Delhi'], 'Destination':['Cochin'], 'Dep_Time':['2026-05-10 10:00'], 'Arrival_Time':['2026-05-10 13:00'], 'Total_Stops':[0]})
    
# #     s_col1.download_button("CSV Template", sample_df.to_csv(index=False), "sample.csv")
    
# #     output = io.BytesIO()
# #     with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
# #         sample_df.to_excel(writer, index=False)
# #     s_col2.download_button("Excel Template", output.getvalue(), "sample.xlsx")
    
# #     s_col3.download_button("JSON Template", sample_df.to_json(orient='records'), "sample.json")

# #     # 2. Multi-format Upload
# #     st.divider()
# #     uploaded_file = st.file_uploader("Upload File (CSV, Excel, or JSON)", type=["csv", "xlsx", "json"])

# #     if uploaded_file:
# #         if uploaded_file.name.endswith('.csv'): df_bulk = pd.read_csv(uploaded_file)
# #         elif uploaded_file.name.endswith('.xlsx'): df_bulk = pd.read_excel(uploaded_file)
# #         else: df_bulk = pd.read_json(uploaded_file)
        
# #         if st.button("🚀 Run Prediction"):
# #             prices = []
# #             for _, row in df_bulk.iterrows():
# #                 try:
# #                     d_t, a_t = pd.to_datetime(row['Dep_Time']), pd.to_datetime(row['Arrival_Time'])
# #                     diff = a_t - d_t
# #                     f = {"Total_Stops": row['Total_Stops'], "Journey_day": d_t.day, "Journey_month": d_t.month, "Dep_hour": d_t.hour, "Dep_min": d_t.minute, "Arrival_hour": a_t.hour, "Arrival_min": a_t.minute, "Duration_hours": int(diff.total_seconds()//3600), "Duration_mins": int((diff.total_seconds()%3600)//60)}
# #                     prices.append(round(process_data(f, row['Airline']), 2))
# #                 except: prices.append(np.nan)
# #             df_bulk['Predicted_Price'] = prices
# #             st.dataframe(df_bulk.head())
# #             st.download_button("📥 Download Results", df_bulk.to_csv(index=False), "results.csv")

# # # --- TAB 3: EDA (NEW) ---
# # with tab3:
# #     st.subheader("📈 Training Dataset Analysis")
# #     if not training_data.empty:
# #         c1, c2 = st.columns(2)
# #         with c1:
# #             st.write("Data Statistics")
# #             st.dataframe(training_data.describe())
# #         with c2:
# #             st.write("Price Distribution by Airline")
# #             st.bar_chart(training_data.groupby('Airline')['Price'].mean())
        
# #         st.divider()
# #         st.write("Top 10 Routes by Frequency")
# #         st.table(training_data['Route'].value_counts().head(10))
# #     else:
# #         st.warning("Training data (Data_Train.xlsx) not found. Please upload it to enable EDA.")

# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
# import io
# import json
# import plotly.graph_objects as go
# import plotly.express as px
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
# # 2. LOAD ASSETS
# # -------------------------
# @st.cache_resource
# def load_assets():
#     # Ensure these files are in your GitHub repository
#     model = joblib.load("xgboost_model.pkl")
#     scaler = joblib.load("scaler.pkl")
#     columns = joblib.load("columns.pkl")
#     ohe = joblib.load("airline_encoder.pkl")
#     try:
#         # Load training data for the EDA tab
#         raw_data = pd.read_excel("Data_Train.xlsx") 
#     except:
#         raw_data = pd.DataFrame() 
#     return model, scaler, columns, ohe, raw_data

# try:
#     model, scaler, columns, ohe, training_data = load_assets()
# except Exception as e:
#     st.error(f"🚨 Critical Error: Model assets not found. {e}")
#     st.stop()

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
#         if col not in df.columns:
#             df[col] = 0
#     df = df[columns]
#     df_scaled = scaler.transform(df)
#     prediction = model.predict(df_scaled)
#     return np.expm1(prediction[0]) # Inverse log transform

# # -------------------------
# # 4. UI STRUCTURE
# # -------------------------
# st.title("✈️ AirFair Vista")
# st.caption("AI-Powered Flight Fare Forecasting | BrainyBeam Internship Project")

# tab1, tab2, tab3 = st.tabs(["🎯 Single Prediction", "📊 Bulk Scanner", "📈 Dataset EDA"])

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
#         dep = st.datetime_input("Departure Time", value=datetime.now())
#         arr = st.datetime_input("Arrival Time", value=dep + timedelta(hours=2))
#         stops = st.slider("Number of Stops", 0, 4, 0)

#     if st.button("Predict Fare"):
#         if arr <= dep:
#             st.error("❌ Arrival must be after Departure")
#         else:
#             duration = arr - dep
#             dur_h = int(duration.total_seconds() // 3600)
#             dur_m = int((duration.total_seconds() % 3600) // 60)
#             feats = {
#                 "Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month,
#                 "Dep_hour": dep.hour, "Dep_min": dep.minute, "Arrival_hour": arr.hour,
#                 "Arrival_min": arr.minute, "Duration_hours": dur_h, "Duration_mins": dur_m
#             }
#             price = predict_price(feats, air)
#             st.markdown(f'''
#                 <div class="price-card">
#                     <p style="color:#BDC3C7;">Estimated Ticket Price</p>
#                     <h1 class="price-value">₹ {price:,.2f}</h1>
#                     <p>{air} • {src} → {dest}</p>
#                 </div>
#             ''', unsafe_allow_html=True)
#             st.balloons()

# # --- TAB 2: BULK SCANNER ---
# with tab2:
#     st.subheader("📂 Batch Fare Processing")
#     st.info("Upload CSV, Excel, or JSON files for bulk price intelligence.")
    
#     # 1. Downloads
#     st.markdown("##### 1. Get Templates")
#     d1, d2, d3 = st.columns(3)
#     sample = pd.DataFrame({'Airline':['IndiGo'], 'Source':['Delhi'], 'Destination':['Cochin'], 'Dep_Time':['2026-05-10 10:00'], 'Arrival_Time':['2026-05-10 13:00'], 'Total_Stops':[0]})
    
#     d1.download_button("Download CSV", sample.to_csv(index=False), "template.csv")
    
#     excel_buffer = io.BytesIO()
#     with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
#         sample.to_excel(writer, index=False)
#     d2.download_button("Download Excel", excel_buffer.getvalue(), "template.xlsx")
    
#     d3.download_button("Download JSON", sample.to_json(orient='records'), "template.json")

#     # 2. Uploads
#     st.divider()
#     uploaded_file = st.file_uploader("Upload File", type=["csv", "xlsx", "json"])

#     if uploaded_file:
#         try:
#             if uploaded_file.name.endswith('.csv'): df_bulk = pd.read_csv(uploaded_file)
#             elif uploaded_file.name.endswith('.xlsx'): df_bulk = pd.read_excel(uploaded_file)
#             else: df_bulk = pd.read_json(uploaded_file)
            
#             if st.button("🚀 Process Bulk File"):
#                 with st.spinner("AI is analyzing..."):
#                     results = []
#                     for _, row in df_bulk.iterrows():
#                         dt, at = pd.to_datetime(row['Dep_Time']), pd.to_datetime(row['Arrival_Time'])
#                         diff = at - dt
#                         f = {"Total_Stops": row['Total_Stops'], "Journey_day": dt.day, "Journey_month": dt.month, "Dep_hour": dt.hour, "Dep_min": dt.minute, "Arrival_hour": at.hour, "Arrival_min": at.minute, "Duration_hours": int(diff.total_seconds()//3600), "Duration_mins": int((diff.total_seconds()%3600)//60)}
#                         results.append(round(predict_price(f, row['Airline']), 2))
#                     df_bulk['Predicted_Price'] = results
#                     st.success("✅ Prediction Complete!")
#                     st.dataframe(df_bulk.head(10))
#                     st.download_button("📥 Download Result CSV", df_bulk.to_csv(index=False), "predictions.csv")
#         except Exception as e:
#             st.error(f"Error reading file. Ensure column names match the template. {e}")

# # --- TAB 3: ENHANCED EDA ---
# with tab3:
#     st.subheader("📈 Exploratory Data Analysis")
#     if not training_data.empty:
#         # Row 1: Stats and Airline Pricing
#         r1_col1, r1_col2 = st.columns(2)
#         with r1_col1:
#             st.markdown("##### 📊 Descriptive Statistics")
#             st.dataframe(training_data.describe(), use_container_width=True)
#         with r1_col2:
#             st.markdown("##### ✈️ Average Price by Airline")
#             avg_air = training_data.groupby('Airline')['Price'].mean().sort_values()
#             fig1 = go.Figure(go.Bar(x=avg_air.values, y=avg_air.index, orientation='h', marker_color='#00AEEF'))
#             fig1.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
#             st.plotly_chart(fig1, use_container_width=True)

#         st.divider()

#         # Row 2: Correlation and Stop Impact
#         r2_col1, r2_col2 = st.columns(2)
#         with r2_col1:
#             st.markdown("##### 🔗 Feature Correlation Heatmap")
#             corr = training_data.select_dtypes(include=[np.number]).corr()
#             fig2 = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='Blues')
#             fig2.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
#             st.plotly_chart(fig2, use_container_width=True)
#         with r2_col2:
#             st.markdown("##### 🛑 Price Distribution by Stops")
#             fig3 = px.box(training_data, x="Total_Stops", y="Price", color_discrete_sequence=['#00AEEF'])
#             fig3.update_layout(height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
#             st.plotly_chart(fig3, use_container_width=True)

#         st.divider()
        
#         # Row 3: Time Series Trend
#         st.markdown("##### 📅 Monthly Price Trends")
#         if 'Journey_month' in training_data.columns:
#             monthly = training_data.groupby('Journey_month')['Price'].mean()
#             fig4 = px.line(x=monthly.index, y=monthly.values, markers=True)
#             fig4.update_traces(line_color='#00AEEF', line_width=4)
#             fig4.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
#             st.plotly_chart(fig4, use_container_width=True)
#     else:
#         st.warning("⚠️ Training data file (Data_Train.xlsx) missing. Upload it to GitHub to enable visual insights.")