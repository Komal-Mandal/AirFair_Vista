# # # # # # # import streamlit as st
# # # # # # # import pandas as pd
# # # # # # # import numpy as np
# # # # # # # import joblib
# # # # # # # import io
# # # # # # # import plotly.express as px
# # # # # # # import plotly.graph_objects as go
# # # # # # # from datetime import datetime, timedelta

# # # # # # # # -------------------------
# # # # # # # # 1. PAGE CONFIG & STYLING
# # # # # # # # -------------------------
# # # # # # # st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

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
# # # # # # # # 2. LOAD & CLEAN ASSETS
# # # # # # # # -------------------------
# # # # # # # @st.cache_resource
# # # # # # # def load_assets():
# # # # # # #     model = joblib.load("xgboost_model.pkl")
# # # # # # #     scaler = joblib.load("scaler.pkl")
# # # # # # #     columns = joblib.load("columns.pkl")
# # # # # # #     ohe = joblib.load("airline_encoder.pkl")
    
# # # # # # #     try:
# # # # # # #         df = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
# # # # # # #         if 'Total_Stops' in df.columns:
# # # # # # #             df['Total_Stops'] = df['Total_Stops'].replace('non-stop', '0 stops')
# # # # # # #             df['Total_Stops'] = df['Total_Stops'].str.extract('(\d+)').fillna(0).astype(int)
# # # # # # #         if 'Date_of_Journey' in df.columns:
# # # # # # #             df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True)
# # # # # # #             df['Journey_day'] = df['Date_of_Journey'].dt.day
# # # # # # #             df['Journey_month'] = df['Date_of_Journey'].dt.month
# # # # # # #         if 'Duration' in df.columns:
# # # # # # #             def convert_duration(duration):
# # # # # # #                 h, m = 0, 0
# # # # # # #                 if 'h' in duration: h = int(duration.split('h')[0])
# # # # # # #                 if 'm' in duration: m = int(duration.split('m')[0].split()[-1])
# # # # # # #                 return (h * 60) + m
# # # # # # #             df['Duration_minutes'] = df['Duration'].apply(convert_duration)
# # # # # # #     except Exception as e:
# # # # # # #         st.warning(f"Note: Data_Train.xlsx processing skipped or failed: {e}")
# # # # # # #         df = pd.DataFrame()
# # # # # # #     return model, scaler, columns, ohe, df

# # # # # # # model, scaler, columns, ohe, training_data = load_assets()

# # # # # # # # -------------------------
# # # # # # # # 3. PREDICTION LOGIC
# # # # # # # # -------------------------
# # # # # # # def predict_price(input_dict, airline_name):
# # # # # # #     df = pd.DataFrame([input_dict])
# # # # # # #     airline_encoded = ohe.transform([[airline_name]])
# # # # # # #     if hasattr(airline_encoded, "toarray"):
# # # # # # #         airline_encoded = airline_encoded.toarray()
# # # # # # #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# # # # # # #     df = pd.concat([df, airline_df], axis=1)
# # # # # # #     for col in columns:
# # # # # # #         if col not in df.columns: df[col] = 0
# # # # # # #     df = df[columns]
# # # # # # #     df_scaled = scaler.transform(df)
# # # # # # #     return np.expm1(model.predict(df_scaled)[0])

# # # # # # # # -------------------------
# # # # # # # # 4. UI STRUCTURE
# # # # # # # # -------------------------
# # # # # # # st.title("✈️ AirFair Vista")
# # # # # # # st.caption("Advanced AI Flight Intelligence | BrainyBeam Internship Project")

# # # # # # # tab1, tab2, tab3 = st.tabs(["🎯 Prediction", "📊 Bulk Scanner", "📈 Advanced EDA"])

# # # # # # # # --- TAB 1: SINGLE PREDICTION ---
# # # # # # # with tab1:
# # # # # # #     col1, col2 = st.columns(2, gap="large")
# # # # # # #     with col1:
# # # # # # #         st.subheader("📍 Journey Details")
# # # # # # #         src = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # # # # # #         dest = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# # # # # # #         air = st.selectbox("Airline", [
# # # # # # #             'IndiGo', 'Air India', 'Jet Airways', 'Jet Airways Business', 
# # # # # # #             'SpiceJet', 'Vistara', 'GoAir', 'Multiple carriers', 
# # # # # # #             'Air Asia', 'Vistara Premium economy'
# # # # # # #         ])
    
# # # # # # #     with col2:
# # # # # # #         st.subheader("🕒 Schedule")
        
# # # # # # #         # FIX: min_value=datetime.now() ensures you cannot pick a past date for Departure
# # # # # # #         current_time = datetime.now()
# # # # # # #         dep = st.datetime_input("Departure Time", value=current_time, min_value=current_time)
        
# # # # # # #         # FIX: min_value=dep ensures Arrival is always after Departure
# # # # # # #         arr = st.datetime_input("Arrival Time", value=dep + timedelta(hours=2), min_value=dep)
        
# # # # # # #         stops = st.slider("Total Stops", 0, 4, 0)

# # # # # # #     if st.button("Predict Fare"):
# # # # # # #         if arr <= dep:
# # # # # # #             st.error("❌ Invalid Schedule: Arrival must be after Departure.")
# # # # # # #         else:
# # # # # # #             duration = arr - dep
# # # # # # #             dur_h = int(duration.total_seconds() // 3600)
# # # # # # #             dur_m = int((duration.total_seconds() % 3600) // 60)
            
# # # # # # #             feats = {
# # # # # # #                 "Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month, 
# # # # # # #                 "Dep_hour": dep.hour, "Dep_min": dep.minute, 
# # # # # # #                 "Arrival_hour": arr.hour, "Arrival_min": arr.minute, 
# # # # # # #                 "Duration_hours": dur_h, "Duration_mins": dur_m
# # # # # # #             }
            
# # # # # # #             price = predict_price(feats, air)
# # # # # # #             st.markdown(f"""
# # # # # # #                 <div class="price-card">
# # # # # # #                     <p>Estimated Fare</p>
# # # # # # #                     <h1 class="price-value">₹ {price:,.2f}</h1>
# # # # # # #                     <p style="color: #00AEEF;">Flight Duration: {dur_h}h {dur_m}m</p>
# # # # # # #                 </div>
# # # # # # #             """, unsafe_allow_html=True)

# # # # # # # # --- TAB 2: BULK SCANNER ---
# # # # # # # with tab2:
# # # # # # #     st.subheader("📂 Batch Prediction")
# # # # # # #     uploaded_file = st.file_uploader("Upload CSV/Excel/JSON", type=["csv", "xlsx", "json"])
# # # # # # #     if uploaded_file:
# # # # # # #         st.success("File uploaded successfully. Click 'Process' to begin.")

# # # # # # # # --- TAB 3: ADVANCED EDA ---
# # # # # # # with tab3:
# # # # # # #     st.subheader("📈 Exploratory Data Analysis")
# # # # # # #     if not training_data.empty:
# # # # # # #         st.markdown("##### 1. Full Multi-Feature Correlation Matrix")
# # # # # # #         numeric_df = training_data.select_dtypes(include=[np.number])
# # # # # # #         corr_matrix = numeric_df.corr()
# # # # # # #         fig_corr = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto")
# # # # # # #         fig_corr.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # #         st.plotly_chart(fig_corr, use_container_width=True)

# # # # # # #         st.divider()

# # # # # # #         c1, c2 = st.columns(2)
# # # # # # #         with c1:
# # # # # # #             st.markdown("##### 2. Price Distribution by Airline")
# # # # # # #             fig_box = px.box(training_data, x="Airline", y="Price", color_discrete_sequence=['#00AEEF'])
# # # # # # #             fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # #             st.plotly_chart(fig_box, use_container_width=True)

# # # # # # #         with c2:
# # # # # # #             st.markdown("##### 3. Price Density by Stops")
# # # # # # #             fig_vio = px.violin(training_data, x="Total_Stops", y="Price", box=True, points="all", color_discrete_sequence=['#00AEEF'])
# # # # # # #             fig_vio.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # #             st.plotly_chart(fig_vio, use_container_width=True)

# # # # # # #         st.divider()

# # # # # # #         c3, c4 = st.columns(2)
# # # # # # #         with c3:
# # # # # # #             st.markdown("##### 4. Average Fare Monthly Trend")
# # # # # # #             monthly = training_data.groupby('Journey_month')['Price'].mean()
# # # # # # #             fig_line = px.line(x=monthly.index, y=monthly.values, markers=True)
# # # # # # #             fig_line.update_traces(line_color='#00AEEF', line_width=4)
# # # # # # #             fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # #             st.plotly_chart(fig_line, use_container_width=True)

# # # # # # #         with c4:
# # # # # # #             st.markdown("##### 5. Duration vs Price Intensity")
# # # # # # #             fig_dens = px.density_heatmap(training_data, x="Duration_minutes", y="Price", color_continuous_scale='Blues')
# # # # # # #             fig_dens.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # # # # #             st.plotly_chart(fig_dens, use_container_width=True)
# # # # # # #     else:
# # # # # # #         st.error("⚠️ Data_Train.xlsx not found.")

# # # # # # import streamlit as st
# # # # # # import pandas as pd
# # # # # # import numpy as np
# # # # # # import joblib
# # # # # # from datetime import datetime, timedelta

# # # # # # # -------------------------
# # # # # # # 1. PAGE CONFIG & STYLING
# # # # # # # -------------------------
# # # # # # st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# # # # # # # Enhanced CSS for a "Proper" UI
# # # # # # st.markdown("""
# # # # # #     <style>
# # # # # #     .main { background-color: #0e1117; color: white; }
# # # # # #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# # # # # #     .stTabs [data-baseweb="tab"] {
# # # # # #         height: 50px; background-color: #1b263b;
# # # # # #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# # # # # #     }
# # # # # #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
    
# # # # # #     /* Better Container Styling */
# # # # # #     .feature-container {
# # # # # #         background-color: #1b263b;
# # # # # #         padding: 20px;
# # # # # #         border-radius: 15px;
# # # # # #         border-left: 5px solid #00AEEF;
# # # # # #         margin-bottom: 20px;
# # # # # #     }
    
# # # # # #     div.stButton > button:first-child {
# # # # # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # # # # #         color: white; border: none; border-radius: 8px; width: 100%; height: 50px;
# # # # # #         font-weight: bold; font-size: 18px; margin-top: 20px;
# # # # # #     }
    
# # # # # #     .price-card {
# # # # # #         background: #1b263b; padding: 25px; border-radius: 15px;
# # # # # #         text-align: center; border: 2px solid #00AEEF; margin-top: 10px;
# # # # # #     }
# # # # # #     .price-value { font-size: 2.8rem; font-weight: 800; color: #00AEEF; margin: 5px 0; }
# # # # # #     </style>
# # # # # #     """, unsafe_allow_html=True)

# # # # # # # -------------------------
# # # # # # # 2. LOAD ASSETS
# # # # # # # -------------------------
# # # # # # @st.cache_resource
# # # # # # def load_assets():
# # # # # #     # Placeholder for your actual model loading logic
# # # # # #     try:
# # # # # #         model = joblib.load("xgboost_model.pkl")
# # # # # #         scaler = joblib.load("scaler.pkl")
# # # # # #         columns = joblib.load("columns.pkl")
# # # # # #         ohe = joblib.load("airline_encoder.pkl")
# # # # # #         training_data = pd.read_excel("Data_Train.xlsx", engine='openpyxl') # Ensure this exists
# # # # # #         return model, scaler, columns, ohe, training_data
# # # # # #     except:
# # # # # #         # Returning dummy objects if files are missing for preview
# # # # # #         return None, None, None, None, pd.DataFrame()

# # # # # # model, scaler, columns, ohe, training_data = load_assets()

# # # # # # # -------------------------
# # # # # # # 3. PREDICTION LOGIC
# # # # # # # -------------------------
# # # # # # def predict_price(input_dict, airline_name):
# # # # # #     if model is None: return 5420.00 # Dummy fallback
    
# # # # # #     df = pd.DataFrame([input_dict])
# # # # # #     airline_encoded = ohe.transform([[airline_name]])
# # # # # #     if hasattr(airline_encoded, "toarray"):
# # # # # #         airline_encoded = airline_encoded.toarray()
# # # # # #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# # # # # #     df = pd.concat([df, airline_df], axis=1)
# # # # # #     for col in columns:
# # # # # #         if col not in df.columns: df[col] = 0
# # # # # #     df = df[columns]
# # # # # #     df_scaled = scaler.transform(df)
# # # # # #     return np.expm1(model.predict(df_scaled)[0])

# # # # # # # -------------------------
# # # # # # # 4. UI STRUCTURE
# # # # # # # -------------------------
# # # # # # st.title("✈️ AirFair Vista")
# # # # # # st.markdown("### AI-Powered Flight Fare Intelligence")

# # # # # # tab1, tab2, tab3 = st.tabs(["🎯 Fare Prediction", "📊 Batch Analysis", "📈 Market Trends"])

# # # # # # with tab1:
# # # # # #     # TRIP TYPE SELECTION (The requested Change #2)
# # # # # #     trip_type = st.radio("Select Journey Type", ["One Way", "Round Trip"], horizontal=True)
    
# # # # # #     st.markdown('<div class="feature-container">', unsafe_allow_html=True)
# # # # # #     col1, col2, col3 = st.columns(3)
    
# # # # # #     with col1:
# # # # # #         st.subheader("📍 Route")
# # # # # #         src = st.selectbox("From", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # # # # #         dest = st.selectbox("To", ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata'])
# # # # # #         air = st.selectbox("Preferred Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara'])
    
# # # # # #     with col2:
# # # # # #         st.subheader("🕒 Outbound")
# # # # # #         dep_date = st.date_input("Departure Date", value=datetime.now())
# # # # # #         dep_time = st.time_input("Departure Time", value=datetime.now().time())
# # # # # #         stops = st.slider("Max Stops", 0, 4, 0)

# # # # # #     with col3:
# # # # # #         if trip_type == "Round Trip":
# # # # # #             st.subheader("🕒 Return")
# # # # # #             ret_date = st.date_input("Return Date", value=dep_date + timedelta(days=2))
# # # # # #             ret_time = st.time_input("Return Time", value=datetime.now().time())
# # # # # #         else:
# # # # # #             st.subheader("🕒 Info")
# # # # # #             st.info("One-way journey selected. Only outbound fare will be calculated.")
    
# # # # # #     st.markdown('</div>', unsafe_allow_html=True)

# # # # # #     if st.button("Calculate Intelligence Fare"):
# # # # # #         # Process Outbound
# # # # # #         outbound_feats = {
# # # # # #             "Total_Stops": stops, "Journey_day": dep_date.day, "Journey_month": dep_date.month,
# # # # # #             "Dep_hour": dep_time.hour, "Dep_min": dep_time.minute,
# # # # # #             "Arrival_hour": (dep_time.hour + 2) % 24, "Arrival_min": dep_time.minute, # Simplified arrival
# # # # # #             "Duration_hours": 2, "Duration_mins": 0
# # # # # #         }
        
# # # # # #         fare_out = predict_price(outbound_feats, air)
        
# # # # # #         # Display Results
# # # # # #         res_col1, res_col2 = st.columns(2 if trip_type == "Round Trip" else [1, 1])
        
# # # # # #         with res_col1:
# # # # # #             st.markdown(f"""
# # # # # #                 <div class="price-card">
# # # # # #                     <p>OUTBOUND FARE</p>
# # # # # #                     <h1 class="price-value">₹ {fare_out:,.2f}</h1>
# # # # # #                     <small>{src} → {dest}</small>
# # # # # #                 </div>
# # # # # #             """, unsafe_allow_html=True)
            
# # # # # #         if trip_type == "Round Trip":
# # # # # #             # Process Return (Swap src and dest)
# # # # # #             return_feats = outbound_feats.copy()
# # # # # #             return_feats["Journey_day"] = ret_date.day
# # # # # #             return_feats["Journey_month"] = ret_date.month
# # # # # #             fare_ret = predict_price(return_feats, air)
            
# # # # # #             with res_col2:
# # # # # #                 st.markdown(f"""
# # # # # #                     <div class="price-card">
# # # # # #                         <p>RETURN FARE</p>
# # # # # #                         <h1 class="price-value">₹ {fare_ret:,.2f}</h1>
# # # # # #                         <small>{dest} → {src}</small>
# # # # # #                     </div>
# # # # # #                 """, unsafe_allow_html=True)
            
# # # # # #             st.markdown(f"""
# # # # # #                 <div style="text-align: center; margin-top: 20px;">
# # # # # #                     <h3>Total Trip Estimate: <span style="color:#00AEEF;">₹ {(fare_out + fare_ret):,.2f}</span></h3>
# # # # # #                 </div>
# # # # # #             """, unsafe_allow_html=True)

# # # # # # # (Remaining tabs 2 and 3 can stay largely the same as your previous logic)



# # # # # import streamlit as st
# # # # # import pandas as pd
# # # # # import numpy as np
# # # # # import joblib
# # # # # from datetime import datetime, date, timedelta

# # # # # # -------------------------
# # # # # # 1. PAGE CONFIG & UI STYLING
# # # # # # -------------------------
# # # # # st.set_page_config(page_title="AirFair Vista Pro", page_icon="✈️", layout="wide")

# # # # # st.markdown("""
# # # # #     <style>
# # # # #     .main { background-color: #0e1117; }
# # # # #     .stMetric { background-color: #1b263b; padding: 15px; border-radius: 10px; border: 1px solid #00AEEF; }
# # # # #     div.stButton > button:first-child {
# # # # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # # # #         color: white; border-radius: 8px; height: 50px; width: 100%; font-weight: bold;
# # # # #     }
# # # # #     .flight-box {
# # # # #         padding: 20px; background-color: #1b263b; border-radius: 10px; margin-bottom: 15px;
# # # # #     }
# # # # #     </style>
# # # # #     """, unsafe_allow_html=True)

# # # # # # -------------------------
# # # # # # 2. LOAD ASSETS
# # # # # # -------------------------
# # # # # @st.cache_resource
# # # # # def load_assets():
# # # # #     try:
# # # # #         model = joblib.load("xgboost_model.pkl")
# # # # #         scaler = joblib.load("scaler.pkl")
# # # # #         columns = joblib.load("columns.pkl")
# # # # #         ohe = joblib.load("airline_encoder.pkl")
# # # # #         df = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
# # # # #         return model, scaler, columns, ohe, df
# # # # #     except Exception as e:
# # # # #         st.error(f"Error loading model files: {e}")
# # # # #         return None, None, None, None, pd.DataFrame()

# # # # # model, scaler, columns, ohe, training_data = load_assets()

# # # # # # -------------------------
# # # # # # 3. PREDICTION ENGINE
# # # # # # -------------------------
# # # # # def predict_price(airline, stops, journey_date, dep_time, arr_time):
# # # # #     # Dummy duration calculation for the model
# # # # #     duration = datetime.combine(date.today(), arr_time) - datetime.combine(date.today(), dep_time)
# # # # #     dur_h = duration.seconds // 3600
# # # # #     dur_m = (duration.seconds % 3600) // 60

# # # # #     input_dict = {
# # # # #         "Total_Stops": stops,
# # # # #         "Journey_day": journey_date.day,
# # # # #         "Journey_month": journey_date.month,
# # # # #         "Dep_hour": dep_time.hour,
# # # # #         "Dep_min": dep_time.minute,
# # # # #         "Arrival_hour": arr_time.hour,
# # # # #         "Arrival_min": arr_time.minute,
# # # # #         "Duration_hours": dur_h,
# # # # #         "Duration_mins": dur_m
# # # # #     }
    
# # # # #     df = pd.DataFrame([input_dict])
# # # # #     airline_encoded = ohe.transform([[airline]])
# # # # #     if hasattr(airline_encoded, "toarray"):
# # # # #         airline_encoded = airline_encoded.toarray()
    
# # # # #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
# # # # #     df = pd.concat([df, airline_df], axis=1)
    
# # # # #     for col in columns:
# # # # #         if col not in df.columns: df[col] = 0
# # # # #     df = df[columns]
# # # # #     df_scaled = scaler.transform(df)
    
# # # # #     price = np.expm1(model.predict(df_scaled)[0])
# # # # #     return price

# # # # # # -------------------------
# # # # # # 4. PRO UI LAYOUT
# # # # # # -------------------------
# # # # # st.title("✈️ AirFair Vista: AI Price Intelligence")
# # # # # st.markdown("---")

# # # # # # CHANGE #2: TRIP TYPE SELECTOR
# # # # # journey_type = st.radio("Select Journey Type", ["One Way", "Round Trip"], horizontal=True)

# # # # # # SHARED ROUTE SETTINGS
# # # # # col_src, col_dest = st.columns(2)
# # # # # with col_src:
# # # # #     src = st.selectbox("Departure City", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # # # # with col_dest:
# # # # #     dest = st.selectbox("Destination City", ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata'])

# # # # # st.write("###")

# # # # # # OUTBOUND SECTION
# # # # # with st.container():
# # # # #     st.subheader("🛫 Outbound Flight Details")
# # # # #     c1, c2, c3, c4 = st.columns(4)
# # # # #     with c1:
# # # # #         dep_date = st.date_input("Departure Date", min_value=date.today())
# # # # #     with c2:
# # # # #         out_airline = st.selectbox("Select Airline", ohe.categories_[0], key="out_air")
# # # # #     with c3:
# # # # #         out_stops = st.number_input("Stops", 0, 4, 0, key="out_stop")
# # # # #     with c4:
# # # # #         out_time = st.time_input("Dep. Time", value=datetime.now().time(), key="out_time")

# # # # # # RETURN SECTION (Conditional based on Journey Type)
# # # # # if journey_type == "Round Trip":
# # # # #     with st.container():
# # # # #         st.subheader("🛬 Return Flight Details")
# # # # #         st.info(f"Route: {dest} → {src}")
        
# # # # #         # PRO UI: Allow changing settings for return leg
# # # # #         diff_return = st.checkbox("Change airline/stops for return journey?")
        
# # # # #         r1, r2, r3, r4 = st.columns(4)
# # # # #         with r1:
# # # # #             # PRO UI: Return date cannot be before departure
# # # # #             ret_date = st.date_input("Return Date", min_value=dep_date, value=dep_date + timedelta(days=2))
        
# # # # #         if diff_return:
# # # # #             with r2:
# # # # #                 ret_airline = st.selectbox("Return Airline", ohe.categories_[0], key="ret_air")
# # # # #             with r3:
# # # # #                 ret_stops = st.number_input("Return Stops", 0, 4, 0, key="ret_stop")
# # # # #         else:
# # # # #             ret_airline = out_airline
# # # # #             ret_stops = out_stops
# # # # #             st.caption(f"Using {out_airline} with {out_stops} stops (same as outbound).")
        
# # # # #         with r4:
# # # # #             ret_time = st.time_input("Return Dep. Time", value=datetime.now().time(), key="ret_time")

# # # # # st.markdown("---")

# # # # # # -------------------------
# # # # # # 5. EXECUTION & RESULTS
# # # # # # -------------------------
# # # # # if st.button("GET AI PRICE PREDICTION"):
# # # # #     if model is None:
# # # # #         st.error("Model not loaded. Check your .pkl files.")
# # # # #     else:
# # # # #         # Predict Outbound
# # # # #         # Using a 2-hour buffer for arrival time for simplicity in features
# # # # #         out_arr_time = (datetime.combine(date.today(), out_time) + timedelta(hours=2)).time()
# # # # #         price_out = predict_price(out_airline, out_stops, dep_date, out_time, out_arr_time)
        
# # # # #         if journey_type == "Round Trip":
# # # # #             ret_arr_time = (datetime.combine(date.today(), ret_time) + timedelta(hours=2)).time()
# # # # #             price_ret = predict_price(ret_airline, ret_stops, ret_date, ret_time, ret_arr_time)
            
# # # # #             # Display Round Trip Results
# # # # #             res_col1, res_col2, res_col3 = st.columns(3)
# # # # #             res_col1.metric("Outbound Fare", f"₹{price_out:,.2f}")
# # # # #             res_col2.metric("Return Fare", f"₹{price_ret:,.2f}")
# # # # #             res_col3.metric("Total Trip Cost", f"₹{(price_out + price_ret):,.2f}", delta_color="inverse")
            
# # # # #             st.success(f"Total estimated cost for your round trip is ₹{(price_out + price_ret):,.2f}")
# # # # #         else:
# # # # #             # Display One Way Results
# # # # #             st.metric("Estimated One-Way Fare", f"₹{price_out:,.2f}")
# # # # #             st.balloons()

# # # # # # TAB SECTION FOR EDA (Keep your previous EDA logic here)
# # # # # with st.expander("View Market Data Insights"):
# # # # #     if not training_data.empty:
# # # # #         st.write(training_data.head())
# # # # #     else:
# # # # #         st.warning("Training data not available for preview.")

# # # # import streamlit as st
# # # # import pandas as pd
# # # # import numpy as np
# # # # import joblib
# # # # import plotly.express as px
# # # # from datetime import datetime, date, timedelta, time

# # # # # -------------------------
# # # # # 1. PAGE CONFIG & STYLING
# # # # # -------------------------
# # # # st.set_page_config(page_title="AirFair Vista Pro", page_icon="✈️", layout="wide")

# # # # st.markdown("""
# # # #     <style>
# # # #     .main { background-color: #0e1117; }
# # # #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# # # #     .stTabs [data-baseweb="tab"] {
# # # #         height: 50px; background-color: #1b263b;
# # # #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# # # #     }
# # # #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
# # # #     .section-box {
# # # #         padding: 20px; background-color: #16213e; border-radius: 15px; 
# # # #         border-left: 5px solid #00AEEF; margin-bottom: 25px;
# # # #     }
# # # #     div.stButton > button:first-child {
# # # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # # #         color: white; border-radius: 8px; height: 55px; width: 100%; font-weight: bold; font-size: 1.2rem;
# # # #     }
# # # #     </style>
# # # #     """, unsafe_allow_html=True)

# # # # # -------------------------
# # # # # 2. LOAD ASSETS
# # # # # -------------------------
# # # # @st.cache_resource
# # # # def load_assets():
# # # #     try:
# # # #         model = joblib.load("xgboost_model.pkl")
# # # #         scaler = joblib.load("scaler.pkl")
# # # #         columns = joblib.load("columns.pkl")
# # # #         ohe = joblib.load("airline_encoder.pkl")
# # # #         # Load training data for EDA tab
# # # #         training_data = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
# # # #         return model, scaler, columns, ohe, training_data
# # # #     except:
# # # #         return None, None, None, None, pd.DataFrame()

# # # # model, scaler, columns, ohe, df_train = load_assets()

# # # # # -------------------------
# # # # # 3. HELPER FUNCTIONS
# # # # # -------------------------
# # # # def predict_price(airline, stops, j_date, d_time, a_time):
# # # #     start = datetime.combine(j_date, d_time)
# # # #     end = datetime.combine(j_date, a_time)
# # # #     if end <= start: end += timedelta(days=1)
# # # #     duration = end - start
    
# # # #     feats = {
# # # #         "Total_Stops": stops, "Journey_day": j_date.day, "Journey_month": j_date.month,
# # # #         "Dep_hour": d_time.hour, "Dep_min": d_time.minute,
# # # #         "Arrival_hour": a_time.hour, "Arrival_min": a_time.minute,
# # # #         "Duration_hours": duration.seconds // 3600, 
# # # #         "Duration_mins": (duration.seconds % 3600) // 60
# # # #     }
    
# # # #     input_df = pd.DataFrame([feats])
# # # #     air_enc = ohe.transform([[airline]])
# # # #     if hasattr(air_enc, "toarray"): air_enc = air_enc.toarray()
    
# # # #     input_df = pd.concat([input_df, pd.DataFrame(air_enc, columns=ohe.get_feature_names_out())], axis=1)
# # # #     for col in columns:
# # # #         if col not in input_df.columns: input_df[col] = 0
    
# # # #     return np.expm1(model.predict(scaler.transform(input_df[columns]))[0])

# # # # # -------------------------
# # # # # 4. MAIN DASHBOARD
# # # # # -------------------------
# # # # st.title("✈️ AirFair Vista: AI Price Intelligence")
# # # # tab1, tab2, tab3 = st.tabs(["🎯 Fare Prediction", "📂 Bulk Scanner", "📈 Advanced EDA"])

# # # # # --- TAB 1: PREDICTION ---
# # # # with tab1:
# # # #     trip_type = st.radio("Journey Type", ["One Way", "Round Trip"], horizontal=True)
    
# # # #     # Global Route
# # # #     c_src, c_dest = st.columns(2)
# # # #     with c_src: src = st.selectbox("From", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # # #     with c_dest: dest = st.selectbox("To", ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata'])

# # # #     # Outbound
# # # #     st.markdown('<div class="section-box">', unsafe_allow_html=True)
# # # #     st.subheader("🛫 Outbound Flight")
# # # #     o1, o2, o3 = st.columns(3)
# # # #     with o1:
# # # #         out_date = st.date_input("Departure Date", min_value=date.today())
# # # #         out_air = st.selectbox("Airline", ohe.categories_[0], key="oa")
# # # #     with o2:
# # # #         out_dep = st.time_input("Dep. Time", time(10, 0), key="ot1")
# # # #         out_stops = st.number_input("Stops", 0, 4, 0, key="os")
# # # #     with o3:
# # # #         out_arr = st.time_input("Arrival Time", time(13, 0), key="ot2")
# # # #     st.markdown('</div>', unsafe_allow_html=True)

# # # #     # Return
# # # #     if trip_type == "Round Trip":
# # # #         st.markdown('<div class="section-box">', unsafe_allow_html=True)
# # # #         st.subheader("🛬 Return Flight")
# # # #         diff_ret = st.checkbox("Different details for return?")
# # # #         r1, r2, r3 = st.columns(3)
# # # #         with r1:
# # # #             ret_date = st.date_input("Return Date", min_value=out_date)
# # # #             ret_air = st.selectbox("Return Airline", ohe.categories_[0], key="ra") if diff_ret else out_air
# # # #         with r2:
# # # #             ret_dep = st.time_input("Return Dep. Time", time(18, 0), key="rt1")
# # # #             ret_stops = st.number_input("Return Stops", 0, 4, 0, key="rs") if diff_ret else out_stops
# # # #         with r3:
# # # #             ret_arr = st.time_input("Return Arrival Time", time(21, 0), key="rt2")
# # # #         st.markdown('</div>', unsafe_allow_html=True)

# # # #     if st.button("CALCULATE AI FARE"):
# # # #         p_out = predict_price(out_air, out_stops, out_date, out_dep, out_arr)
# # # #         if trip_type == "Round Trip":
# # # #             p_ret = predict_price(ret_air, ret_stops, ret_date, ret_dep, ret_arr)
# # # #             c1, c2, c3 = st.columns(3)
# # # #             c1.metric("Outbound", f"₹{p_out:,.2f}")
# # # #             c2.metric("Inbound", f"₹{p_ret:,.2f}")
# # # #             c3.metric("Total", f"₹{(p_out+p_ret):,.2f}")
# # # #         else:
# # # #             st.metric("One-Way Fare", f"₹{p_out:,.2f}")

# # # # # --- TAB 2: BULK SCANNER ---
# # # # with tab2:
# # # #     st.subheader("📂 Batch Prediction")
# # # #     uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
# # # #     if uploaded_file:
# # # #         st.success("File uploaded successfully. Processing logic ready.")

# # # # # --- TAB 3: ADVANCED EDA ---
# # # # with tab3:
# # # #     st.subheader("📈 Exploratory Data Analysis")
# # # #     if not df_train.empty:
# # # #         c1, c2 = st.columns(2)
# # # #         with c1:
# # # #             fig1 = px.box(df_train, x="Airline", y="Price", title="Price by Airline")
# # # #             st.plotly_chart(fig1, use_container_width=True)
# # # #         with c2:
# # # #             # Simple preprocessing for stop visualization
# # # #             df_train['Stops_Clean'] = df_train['Total_Stops'].astype(str)
# # # #             fig2 = px.violin(df_train, x="Stops_Clean", y="Price", title="Price Density by Stops")
# # # #             st.plotly_chart(fig2, use_container_width=True)
# # # #     else:
# # # #         st.error("Data_Train.xlsx not found. Please upload it to enable EDA.")



# # # import streamlit as st
# # # import pandas as pd
# # # import numpy as np
# # # import joblib
# # # import plotly.express as px
# # # from datetime import datetime, date, timedelta, time

# # # # -------------------------
# # # # 1. PAGE CONFIG & STYLING
# # # # -------------------------
# # # st.set_page_config(page_title="AirFair Vista Pro", page_icon="✈️", layout="wide")

# # # st.markdown("""
# # #     <style>
# # #     .main { background-color: #0e1117; }
# # #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# # #     .stTabs [data-baseweb="tab"] {
# # #         height: 50px; background-color: #1b263b;
# # #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# # #     }
# # #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
# # #     .section-box {
# # #         padding: 20px; background-color: #16213e; border-radius: 15px; 
# # #         border-left: 5px solid #00AEEF; margin-bottom: 25px;
# # #     }
# # #     div.stButton > button:first-child {
# # #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# # #         color: white; border-radius: 8px; height: 55px; width: 100%; font-weight: bold; font-size: 1.2rem;
# # #     }
# # #     </style>
# # #     """, unsafe_allow_html=True)

# # # # -------------------------
# # # # 2. LOAD ASSETS
# # # # -------------------------
# # # @st.cache_resource
# # # def load_assets():
# # #     try:
# # #         model = joblib.load("xgboost_model.pkl")
# # #         scaler = joblib.load("scaler.pkl")
# # #         columns = joblib.load("columns.pkl")
# # #         ohe = joblib.load("airline_encoder.pkl")
# # #         # Load training data for EDA tab
# # #         training_data = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
# # #         return model, scaler, columns, ohe, training_data
# # #     except:
# # #         return None, None, None, None, pd.DataFrame()

# # # model, scaler, columns, ohe, df_train = load_assets()

# # # # -------------------------
# # # # 3. HELPER FUNCTIONS
# # # # -------------------------
# # # def predict_price(airline, stops, j_date, d_time, a_time):
# # #     start = datetime.combine(j_date, d_time)
# # #     end = datetime.combine(j_date, a_time)
# # #     if end <= start: end += timedelta(days=1)
# # #     duration = end - start
    
# # #     feats = {
# # #         "Total_Stops": stops, "Journey_day": j_date.day, "Journey_month": j_date.month,
# # #         "Dep_hour": d_time.hour, "Dep_min": d_time.minute,
# # #         "Arrival_hour": a_time.hour, "Arrival_min": a_time.minute,
# # #         "Duration_hours": duration.seconds // 3600, 
# # #         "Duration_mins": (duration.seconds % 3600) // 60
# # #     }
    
# # #     input_df = pd.DataFrame([feats])
# # #     air_enc = ohe.transform([[airline]])
# # #     if hasattr(air_enc, "toarray"): air_enc = air_enc.toarray()
    
# # #     input_df = pd.concat([input_df, pd.DataFrame(air_enc, columns=ohe.get_feature_names_out())], axis=1)
# # #     for col in columns:
# # #         if col not in input_df.columns: input_df[col] = 0
    
# # #     return np.expm1(model.predict(scaler.transform(input_df[columns]))[0])

# # # # -------------------------
# # # # 4. MAIN DASHBOARD
# # # # -------------------------
# # # st.title("✈️ AirFair Vista: AI Price Intelligence")
# # # tab1, tab2, tab3 = st.tabs(["🎯 Fare Prediction", "📂 Bulk Scanner", "📈 Advanced EDA"])

# # # # --- TAB 1: PREDICTION ---
# # # with tab1:
# # #     trip_type = st.radio("Journey Type", ["One Way", "Round Trip"], horizontal=True)
    
# # #     # Global Route
# # #     c_src, c_dest = st.columns(2)
# # #     with c_src: src = st.selectbox("From", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # #     with c_dest: dest = st.selectbox("To", ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata'])

# # #     # Outbound
# # #     st.markdown('<div class="section-box">', unsafe_allow_html=True)
# # #     st.subheader("🛫 Outbound Flight")
# # #     o1, o2, o3 = st.columns(3)
# # #     with o1:
# # #         out_date = st.date_input("Departure Date", min_value=date.today())
# # #         out_air = st.selectbox("Airline", ohe.categories_[0], key="oa")
# # #     with o2:
# # #         out_dep = st.time_input("Dep. Time", time(10, 0), key="ot1")
# # #         out_stops = st.number_input("Stops", 0, 4, 0, key="os")
# # #     with o3:
# # #         out_arr = st.time_input("Arrival Time", time(13, 0), key="ot2")
# # #     st.markdown('</div>', unsafe_allow_html=True)

# # #     # Return
# # #     if trip_type == "Round Trip":
# # #         st.markdown('<div class="section-box">', unsafe_allow_html=True)
# # #         st.subheader("🛬 Return Flight")
# # #         diff_ret = st.checkbox("Different details for return?")
# # #         r1, r2, r3 = st.columns(3)
# # #         with r1:
# # #             ret_date = st.date_input("Return Date", min_value=out_date)
# # #             ret_air = st.selectbox("Return Airline", ohe.categories_[0], key="ra") if diff_ret else out_air
# # #         with r2:
# # #             ret_dep = st.time_input("Return Dep. Time", time(18, 0), key="rt1")
# # #             ret_stops = st.number_input("Return Stops", 0, 4, 0, key="rs") if diff_ret else out_stops
# # #         with r3:
# # #             ret_arr = st.time_input("Return Arrival Time", time(21, 0), key="rt2")
# # #         st.markdown('</div>', unsafe_allow_html=True)

# # #     if st.button("CALCULATE AI FARE"):
# # #         p_out = predict_price(out_air, out_stops, out_date, out_dep, out_arr)
# # #         if trip_type == "Round Trip":
# # #             p_ret = predict_price(ret_air, ret_stops, ret_date, ret_dep, ret_arr)
# # #             c1, c2, c3 = st.columns(3)
# # #             c1.metric("Outbound", f"₹{p_out:,.2f}")
# # #             c2.metric("Inbound", f"₹{p_ret:,.2f}")
# # #             c3.metric("Total", f"₹{(p_out+p_ret):,.2f}")
# # #         else:
# # #             st.metric("One-Way Fare", f"₹{p_out:,.2f}")

# # # # --- TAB 2: BULK SCANNER ---
# # # with tab2:
# # #     st.subheader("📂 Batch Prediction")
# # #     uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
# # #     if uploaded_file:
# # #         st.success("File uploaded successfully. Processing logic ready.")

# # # # --- TAB 3: ADVANCED EDA ---
# # # with tab3:
# # #     st.subheader("📈 Exploratory Data Analysis")
# # #     if not df_train.empty:
# # #         c1, c2 = st.columns(2)
# # #         with c1:
# # #             fig1 = px.box(df_train, x="Airline", y="Price", title="Price by Airline")
# # #             st.plotly_chart(fig1, use_container_width=True)
# # #         with c2:
# # #             # Simple preprocessing for stop visualization
# # #             df_train['Stops_Clean'] = df_train['Total_Stops'].astype(str)
# # #             fig2 = px.violin(df_train, x="Stops_Clean", y="Price", title="Price Density by Stops")
# # #             st.plotly_chart(fig2, use_container_width=True)
# # #     else:
# # #         st.error("Data_Train.xlsx not found. Please upload it to enable EDA.")



# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # import joblib
# # import plotly.express as px
# # from datetime import datetime, date, timedelta, time

# # # 1. PAGE CONFIG
# # st.set_page_config(page_title="AirFair Vista Pro", page_icon="✈️", layout="wide")

# # st.markdown("""
# #     <style>
# #     .main { background-color: #0e1117; }
# #     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
# #     .stTabs [data-baseweb="tab"] {
# #         height: 50px; background-color: #1b263b;
# #         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
# #     }
# #     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; }
# #     .section-box {
# #         padding: 25px; background-color: #16213e; border-radius: 15px; 
# #         border-left: 5px solid #00AEEF; margin-bottom: 25px;
# #     }
# #     div.stButton > button:first-child {
# #         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
# #         color: white; border-radius: 8px; height: 55px; width: 100%; font-weight: bold;
# #     }
# #     </style>
# #     """, unsafe_allow_html=True)

# # # 2. LOAD ASSETS
# # @st.cache_resource
# # def load_assets():
# #     try:
# #         model = joblib.load("xgboost_model.pkl")
# #         scaler = joblib.load("scaler.pkl")
# #         columns = joblib.load("columns.pkl")
# #         ohe = joblib.load("airline_encoder.pkl")
# #         df_train = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
# #         return model, scaler, columns, ohe, df_train
# #     except:
# #         return None, None, None, None, pd.DataFrame()

# # model, scaler, columns, ohe, df_train = load_assets()

# # # 3. PREDICTION ENGINE (With Overnight Fix)
# # def predict_price(airline, stops, j_date, d_time, a_time):
# #     start = datetime.combine(j_date, d_time)
# #     end = datetime.combine(j_date, a_time)
    
# #     # FIX: If arrival is earlier than departure, it's the next day
# #     if end <= start:
# #         end += timedelta(days=1)
        
# #     duration = end - start
# #     dur_h = duration.seconds // 3600
# #     dur_m = (duration.seconds % 3600) // 60

# #     feats = {
# #         "Total_Stops": stops, "Journey_day": j_date.day, "Journey_month": j_date.month,
# #         "Dep_hour": d_time.hour, "Dep_min": d_time.minute,
# #         "Arrival_hour": a_time.hour, "Arrival_min": a_time.minute,
# #         "Duration_hours": dur_h, "Duration_mins": dur_m
# #     }
    
# #     input_df = pd.DataFrame([feats])
# #     air_enc = ohe.transform([[airline]])
# #     if hasattr(air_enc, "toarray"): air_enc = air_enc.toarray()
    
# #     input_df = pd.concat([input_df, pd.DataFrame(air_enc, columns=ohe.get_feature_names_out())], axis=1)
# #     for col in columns:
# #         if col not in input_df.columns: input_df[col] = 0
    
# #     return np.expm1(model.predict(scaler.transform(input_df[columns]))[0])

# # # 4. MAIN UI
# # st.title("✈️ AirFair Vista: AI Price Intelligence")
# # tab1, tab2, tab3 = st.tabs(["🎯 Fare Prediction", "📂 Bulk Scanner", "📈 Advanced EDA"])

# # with tab1:
# #     trip_type = st.radio("Trip Type", ["One Way", "Round Trip"], horizontal=True)
    
# #     c_src, c_dest = st.columns(2)
# #     with c_src: src = st.selectbox("From", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# #     with c_dest: dest = st.selectbox("To", ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata'])

# #     # OUTBOUND
# #     st.markdown('<div class="section-box">', unsafe_allow_html=True)
# #     st.subheader("🛫 Outbound Flight")
# #     o1, o2, o3 = st.columns(3)
# #     with o1:
# #         out_date = st.date_input("Departure Date", min_value=date.today())
# #         out_air = st.selectbox("Airline", ohe.categories_[0], key="oa")
# #     with o2:
# #         out_dep = st.time_input("Dep. Time", time(10, 0))
# #         out_stops = st.number_input("Stops", 0, 4, 0)
# #     with o3:
# #         out_arr = st.time_input("Arrival Time", time(0, 15)) # 00:15 as per your image
# #     st.markdown('</div>', unsafe_allow_html=True)

# #     # RETURN
# #     if trip_type == "Round Trip":
# #         st.markdown('<div class="section-box">', unsafe_allow_html=True)
# #         st.subheader("🛬 Return Flight")
# #         r1, r2, r3 = st.columns(3)
# #         with r1:
# #             ret_date = st.date_input("Return Date", min_value=out_date)
# #             ret_air = st.selectbox("Return Airline", ohe.categories_[0], key="ra")
# #         with r2:
# #             ret_dep = st.time_input("Return Dep. Time", time(18, 0))
# #             ret_stops = st.number_input("Return Stops", 0, 4, 0, key="rs")
# #         with r3:
# #             ret_arr = st.time_input("Return Arrival Time", time(21, 0))
# #         st.markdown('</div>', unsafe_allow_html=True)

# #     if st.button("CALCULATE AI FARE"):
# #         p_out = predict_price(out_air, out_stops, out_date, out_dep, out_arr)
# #         if trip_type == "Round Trip":
# #             p_ret = predict_price(ret_air, ret_stops, ret_date, ret_dep, ret_arr)
# #             c1, c2, c3 = st.columns(3)
# #             c1.metric("Outbound", f"₹{p_out:,.2f}")
# #             c2.metric("Return", f"₹{p_ret:,.2f}")
# #             c3.metric("Total", f"₹{(p_out+p_ret):,.2f}")
# #         else:
# #             st.metric("One-Way Fare", f"₹{p_out:,.2f}")

# # with tab2:
# #     st.subheader("📂 Batch Prediction")
# #     st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])

# # with tab3:
# #     st.subheader("📈 Market Insights")
# #     if not df_train.empty:
# #         fig = px.box(df_train, x="Airline", y="Price", title="Price Distribution")
# #         st.plotly_chart(fig, use_container_width=True)

# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
# import plotly.express as px
# import plotly.graph_objects as go
# from datetime import datetime, date, timedelta, time

# # -------------------------
# # 1. PAGE CONFIG & STYLING
# # -------------------------
# st.set_page_config(page_title="AirFair Vista Pro", page_icon="✈️", layout="wide")

# st.markdown("""
#     <style>
#     .main { background-color: #0e1117; }
#     .stTabs [data-baseweb="tab-list"] { gap: 24px; }
#     .stTabs [data-baseweb="tab"] {
#         height: 50px; background-color: #1b263b;
#         border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
#     }
#     .stTabs [aria-selected="true"] { background-color: #00AEEF !important; }
#     .section-box {
#         padding: 25px; background-color: #16213e; border-radius: 15px; 
#         border-left: 5px solid #00AEEF; margin-bottom: 25px;
#     }
#     div.stButton > button:first-child {
#         background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
#         color: white; border-radius: 8px; height: 55px; width: 100%; font-weight: bold;
#     }
#     </style>
#     """, unsafe_allow_html=True)

# # -------------------------
# # 2. ASSET LOADING
# # -------------------------
# @st.cache_resource
# def load_assets():
#     try:
#         model = joblib.load("xgboost_model.pkl")
#         scaler = joblib.load("scaler.pkl")
#         columns = joblib.load("columns.pkl")
#         ohe = joblib.load("airline_encoder.pkl")
#         df = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
#         return model, scaler, columns, ohe, df
#     except:
#         return None, None, None, None, pd.DataFrame()

# model, scaler, columns, ohe, df_train = load_assets()

# # -------------------------
# # 3. PREDICTION ENGINE
# # -------------------------
# def predict_price(airline, stops, j_date, d_time, a_time):
#     start = datetime.combine(j_date, d_time)
#     end = datetime.combine(j_date, a_time)
#     if end <= start: end += timedelta(days=1)
#     duration = end - start
    
#     feats = {
#         "Total_Stops": stops, "Journey_day": j_date.day, "Journey_month": j_date.month,
#         "Dep_hour": d_time.hour, "Dep_min": d_time.minute,
#         "Arrival_hour": a_time.hour, "Arrival_min": a_time.minute,
#         "Duration_hours": duration.seconds // 3600, 
#         "Duration_mins": (duration.seconds % 3600) // 60
#     }
    
#     input_df = pd.DataFrame([feats])
#     air_enc = ohe.transform([[airline]])
#     if hasattr(air_enc, "toarray"): air_enc = air_enc.toarray()
    
#     input_df = pd.concat([input_df, pd.DataFrame(air_enc, columns=ohe.get_feature_names_out())], axis=1)
#     for col in columns:
#         if col not in input_df.columns: input_df[col] = 0
    
#     return np.expm1(model.predict(scaler.transform(input_df[columns]))[0])

# # -------------------------
# # 4. DASHBOARD TABS
# # -------------------------
# tab1, tab2, tab3 = st.tabs(["🎯 Fare Prediction", "📂 Bulk Scanner", "📈 Advanced EDA"])

# # --- TAB 1: PREDICTION ---
# with tab1:
#     st.subheader("Flight Fare Intelligence")
#     trip_type = st.radio("Trip Type", ["One Way", "Round Trip"], horizontal=True)
    
#     c1, c2 = st.columns(2)
#     with c1: src = st.selectbox("From", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
#     with c2: dest = st.selectbox("To", ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata'])

#     # Outbound Section
#     st.markdown('<div class="section-box">', unsafe_allow_html=True)
#     st.write("🛫 **Outbound Details**")
#     o1, o2, o3 = st.columns(3)
#     with o1:
#         out_date = st.date_input("Date", min_value=date.today(), key="od")
#         out_air = st.selectbox("Airline", ohe.categories_[0], key="oa")
#     with o2:
#         out_dep = st.time_input("Departure", time(10, 0), key="ot1")
#         out_stops = st.number_input("Stops", 0, 4, 0, key="os")
#     with o3:
#         out_arr = st.time_input("Arrival", time(13, 0), key="ot2")
#     st.markdown('</div>', unsafe_allow_html=True)

#     # Return Section
#     if trip_type == "Round Trip":
#         st.markdown('<div class="section-box">', unsafe_allow_html=True)
#         st.write("🛬 **Return Details**")
#         r1, r2, r3 = st.columns(3)
#         with r1:
#             ret_date = st.date_input("Date", min_value=out_date, value=out_date+timedelta(days=2))
#             ret_air = st.selectbox("Return Airline", ohe.categories_[0], key="ra")
#         with r2:
#             ret_dep = st.time_input("Departure", time(18, 0), key="rt1")
#             ret_stops = st.number_input("Stops", 0, 4, 0, key="rs")
#         with r3:
#             ret_arr = st.time_input("Arrival", time(21, 0), key="rt2")
#         st.markdown('</div>', unsafe_allow_html=True)

#     if st.button("CALCULATE ESTIMATED FARE"):
#         p_out = predict_price(out_air, out_stops, out_date, out_dep, out_arr)
#         if trip_type == "Round Trip":
#             p_ret = predict_price(ret_air, ret_stops, ret_date, ret_dep, ret_arr)
#             m1, m2, m3 = st.columns(3)
#             m1.metric("Outbound Fare", f"₹{p_out:,.2f}")
#             m2.metric("Return Fare", f"₹{p_ret:,.2f}")
#             m3.metric("Total Trip Cost", f"₹{(p_out+p_ret):,.2f}")
#         else:
#             st.metric("One-Way Fare", f"₹{p_out:,.2f}")

# # --- TAB 2: BULK SCANNER ---
# with tab2:
#     st.subheader("📂 Batch Analysis")
#     uploaded_file = st.file_uploader("Upload CSV for Multi-Prediction", type=["csv"])
#     if uploaded_file:
#         st.info("Scanner Ready: System will process all rows against the AI model.")

# # --- TAB 3: ADVANCED EDA ---
# with tab3:
#     st.subheader("📈 Market Exploratory Analysis")
#     if not df_train.empty:
#         # Visualization 1 & 2
#         row1_c1, row1_c2 = st.columns(2)
#         with row1_c1:
#             fig1 = px.box(df_train, x="Airline", y="Price", color="Airline", title="1. Airline Price Distribution")
#             st.plotly_chart(fig1, use_container_width=True)
#         with row1_c2:
#             df_train['Stops_Str'] = df_train['Total_Stops'].astype(str)
#             fig2 = px.violin(df_train, x="Stops_Str", y="Price", box=True, title="2. Price Density by Number of Stops")
#             st.plotly_chart(fig2, use_container_width=True)
        
#         # Visualization 3 & 4
#         row2_c1, row2_c2 = st.columns(2)
#         with row2_c1:
#             avg_month = df_train.groupby('Journey_month')['Price'].mean().reset_index()
#             fig3 = px.line(avg_month, x='Journey_month', y='Price', markers=True, title="3. Average Fare Monthly Trend")
#             st.plotly_chart(fig3, use_container_width=True)
#         with row2_c2:
#             route_map = df_train.groupby(['Source', 'Destination'])['Price'].mean().reset_index()
#             fig4 = px.density_heatmap(route_map, x="Source", y="Destination", z="Price", title="4. Route Pricing Intensity")
#             st.plotly_chart(fig4, use_container_width=True)

#         # Visualization 5 & 6
#         row3_c1, row3_c2 = st.columns(2)
#         with row3_c1:
#             # Assuming Duration_minutes exists from your cleanup logic
#             fig5 = px.scatter(df_train, x="Duration", y="Price", color="Total_Stops", opacity=0.5, title="5. Duration vs Price Relationship")
#             st.plotly_chart(fig5, use_container_width=True)
#         with row3_c2:
#             fig6 = px.pie(df_train, names='Airline', hole=0.4, title="6. Airline Market Volume (Dataset Share)")
#             st.plotly_chart(fig6, use_container_width=True)
#     else:
#         st.error("Please ensure Data_Train.xlsx is in the root folder to view EDA.")



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