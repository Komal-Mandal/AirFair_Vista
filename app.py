# # # # import streamlit as st
# # # # import pandas as pd
# # # # import numpy as np
# # # # import joblib
# # # # import plotly.graph_objects as go
# # # # from datetime import datetime, timedelta

# # # # # -------------------------
# # # # # 1. PAGE CONFIG & STYLING
# # # # # -------------------------
# # # # st.set_page_config(page_title="Flight Price Intelligence", page_icon="✈️", layout="wide")

# # # # st.markdown("""
# # # # <style>
# # # # .main { background-color: #0e1117; color: white; }
# # # # div.stButton > button:first-child {
# # # #     background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
# # # #     color: white; border: none; padding: 15px;
# # # #     font-size: 1.2rem; font-weight: bold; border-radius: 12px;
# # # #     width: 100%; margin-top: 20px;
# # # # }
# # # # .price-card {
# # # #     background: linear-gradient(180deg, rgba(99, 102, 241, 0.1) 0%, rgba(11, 14, 20, 0) 100%);
# # # #     padding: 40px; border-radius: 20px;
# # # #     text-align: center; border: 1px solid rgba(99, 102, 241, 0.2);
# # # # }
# # # # .price-value { font-size: 4rem; font-weight: 800; color: #ffffff; }
# # # # </style>
# # # # """, unsafe_allow_html=True)

# # # # # -------------------------
# # # # # 2. LOAD MODEL & COLUMNS
# # # # # -------------------------
# # # # @st.cache_resource
# # # # def load_model():
# # # #     return joblib.load("xgboost_model.pkl")  # This file must contain {"model": xgb, "columns": X.columns.tolist()}

# # # # try:
# # # #     model_data = load_model()
# # # #     model = model_data["model"]
# # # #     model_columns = model_data["columns"]
# # # # except Exception as e:
# # # #     st.error(f"🚨 Model loading failed: {e}")
# # # #     st.stop()

# # # # # -------------------------
# # # # # 3. STREAMLIT UI
# # # # # -------------------------
# # # # st.title("✈️ Flight Price Intelligence")
# # # # st.caption("Smart AI-based flight fare prediction system")
# # # # st.divider()

# # # # col1, col2 = st.columns(2, gap="large")

# # # # with col1:
# # # #     st.markdown("#### 📍 Route")
# # # #     source = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # # #     destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# # # #     airline = st.selectbox("Airline", [
# # # #         'Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
# # # #         'Multiple carriers', 'Multiple carriers Premium economy', 'SpiceJet',
# # # #         'Trujet', 'Vistara', 'Vistara Premium economy'
# # # #     ])

# # # # with col2:
# # # #     st.markdown("#### 🕒 Schedule")
# # # #     dep_time = st.datetime_input("Departure Time", value=datetime.now())
# # # #     arr_time = st.datetime_input("Arrival Time", value=dep_time + timedelta(hours=2))
# # # #     total_stops = st.select_slider("Total Stops", options=[0,1,2,3,4])

# # # # # Calculate Duration
# # # # duration = arr_time - dep_time
# # # # duration_seconds = duration.total_seconds()
# # # # if duration_seconds < 0:
# # # #     st.error("❌ Arrival cannot be before Departure.")
# # # #     st.stop()
# # # # dur_hour = int(duration_seconds // 3600)
# # # # dur_min = int((duration_seconds % 3600) // 60)
# # # # st.info(f"⏱️ Flight Duration: {dur_hour}h {dur_min}m")

# # # # # -------------------------
# # # # # 4. PREDICTION
# # # # # -------------------------
# # # # if st.button("Calculate Best Fare"):
# # # #     # Base numeric features
# # # #     input_dict = {
# # # #         "Total_Stops": total_stops,
# # # #         "Journey_day": dep_time.day,
# # # #         "Journey_month": dep_time.month,
# # # #         "Dep_hour": dep_time.hour,
# # # #         "Dep_min": dep_time.minute,
# # # #         "Arrival_hour": arr_time.hour,
# # # #         "Arrival_min": arr_time.minute,
# # # #         "Duration_hours": dur_hour,
# # # #         "Duration_mins": dur_min
# # # #     }

# # # #     # Create DataFrame with all zeros
# # # #     input_df = pd.DataFrame(0, index=[0], columns=model_columns)

# # # #     # Fill numeric features
# # # #     for col in input_dict:
# # # #         if col in input_df.columns:
# # # #             input_df[col] = input_dict[col]

# # # #     # Fill one-hot categorical features
# # # #     airline_col = f"Airline_{airline}"
# # # #     source_col = f"Source_{source}"
# # # #     dest_col = f"Destination_{destination}"
# # # #     for col in [airline_col, source_col, dest_col]:
# # # #         if col in input_df.columns:
# # # #             input_df[col] = 1

# # # #     # Predict
# # # #     try:
# # # #         pred = model.predict(input_df)
# # # #         final_price = np.expm1(pred[0])  # Reverse log1p

# # # #         st.divider()
# # # #         colA, colB = st.columns([1.2,1])

# # # #         with colA:
# # # #             st.markdown(f"""
# # # #             <div class="price-card">
# # # #                 <p style="color:#6366f1;">Estimated Fare</p>
# # # #                 <h1 class="price-value">₹ {final_price:,.2f}</h1>
# # # #                 <p>{airline} • {source} → {destination}</p>
# # # #             </div>
# # # #             """, unsafe_allow_html=True)
# # # #             st.balloons()

# # # #         with colB:
# # # #             fig = go.Figure(go.Indicator(
# # # #                 mode="gauge+number",
# # # #                 value=final_price,
# # # #                 gauge={
# # # #                     'axis': {'range':[None,30000]},
# # # #                     'bar': {'color':"#6366f1"},
# # # #                     'steps':[{'range':[0,8000],'color':'rgba(0,255,0,0.1)'},
# # # #                              {'range':[8000,18000],'color':'rgba(255,255,0,0.1)'},
# # # #                              {'range':[18000,30000],'color':'rgba(255,0,0,0.1)'}]
# # # #                 }
# # # #             ))
# # # #             fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
# # # #             st.plotly_chart(fig, use_container_width=True)

# # # #     except Exception as e:
# # # #         st.error(f"Prediction Error: {e}")
# # # #         st.write("⚠️ Make sure your input features exactly match the training features.")


# # # import streamlit as st
# # # import pandas as pd
# # # import numpy as np
# # # import joblib
# # # import plotly.graph_objects as go
# # # from datetime import datetime, timedelta

# # # # -------------------------
# # # # 1. PAGE CONFIG
# # # # -------------------------
# # # st.set_page_config(page_title="Flight Price Intelligence", page_icon="✈️", layout="wide")

# # # # -------------------------
# # # # 2. LOAD MODEL + SCALER + COLUMNS
# # # # -------------------------
# # # @st.cache_resource
# # # def load_all():
# # #     model = joblib.load("xgboost_model.pkl")
# # #     scaler = joblib.load("scaler.pkl")
# # #     columns = joblib.load("columns.pkl")
# # #     return model, scaler, columns

# # # model, scaler, model_columns = load_all()

# # # # -------------------------
# # # # 3. UI
# # # # -------------------------
# # # st.title("✈️ Flight Price Intelligence")
# # # st.caption("AI-based Flight Fare Prediction System")

# # # col1, col2 = st.columns(2)

# # # with col1:
# # #     source = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# # #     destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# # #     airline = st.selectbox("Airline", [
# # #         'Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
# # #         'Multiple carriers', 'Multiple carriers Premium economy', 'SpiceJet',
# # #         'Trujet', 'Vistara', 'Vistara Premium economy'
# # #     ])

# # # with col2:
# # #     dep_time = st.datetime_input("Departure Time", value=datetime.now())
# # #     arr_time = st.datetime_input("Arrival Time", value=dep_time + timedelta(hours=2))
# # #     total_stops = st.select_slider("Total Stops", options=[0,1,2,3,4])

# # # # -------------------------
# # # # 4. FEATURE ENGINEERING
# # # # -------------------------
# # # duration = arr_time - dep_time
# # # if duration.total_seconds() < 0:
# # #     st.error("Arrival cannot be before Departure")
# # #     st.stop()

# # # dur_hour = int(duration.total_seconds() // 3600)
# # # dur_min = int((duration.total_seconds() % 3600) // 60)

# # # # -------------------------
# # # # 5. PREDICTION
# # # # -------------------------
# # # if st.button("Predict Price"):

# # #     # Create empty dataframe with all columns
# # #     input_df = pd.DataFrame(0, index=[0], columns=model_columns)

# # #     # Fill numeric features
# # #     input_df["Total_Stops"] = total_stops
# # #     input_df["Journey_day"] = dep_time.day
# # #     input_df["Journey_month"] = dep_time.month
# # #     input_df["Dep_hour"] = dep_time.hour
# # #     input_df["Dep_min"] = dep_time.minute
# # #     input_df["Arrival_hour"] = arr_time.hour
# # #     input_df["Arrival_min"] = arr_time.minute
# # #     input_df["Duration_hours"] = dur_hour
# # #     input_df["Duration_mins"] = dur_min

# # #     # Reset all categorical columns
# # #     for col in model_columns:
# # #         if "Airline_" in col or "Source_" in col or "Destination_" in col:
# # #             input_df[col] = 0

# # #     # Set selected categorical values
# # #     if f"Airline_{airline}" in input_df.columns:
# # #         input_df[f"Airline_{airline}"] = 1

# # #     if f"Source_{source}" in input_df.columns:
# # #         input_df[f"Source_{source}"] = 1

# # #     if f"Destination_{destination}" in input_df.columns:
# # #         input_df[f"Destination_{destination}"] = 1

# # #     # ✅ APPLY SCALING (CRITICAL FIX)
# # #     input_scaled = scaler.transform(input_df)

# # #     # Predict
# # #     prediction = model.predict(input_scaled)

# # #     # Reverse log transform
# # #     final_price = np.expm1(prediction[0])

# # #     # -------------------------
# # #     # 6. OUTPUT
# # #     # -------------------------
# # #     st.success(f"💰 Estimated Price: ₹ {final_price:,.2f}")

# # #     # Optional chart
# # #     fig = go.Figure(go.Indicator(
# # #         mode="gauge+number",
# # #         value=final_price,
# # #         gauge={'axis': {'range': [None, 30000]}}
# # #     ))
# # #     st.plotly_chart(fig)

# # #     # Debug (remove later)
# # #     st.write("DEBUG INPUT:", input_df)


# # import streamlit as st
# # import pandas as pd
# # import numpy as np
# # import joblib

# # # ================= LOAD FILES =================
# # model = joblib.load("xgboost_model.pkl")
# # scaler = joblib.load("scaler.pkl")
# # columns = joblib.load("columns.pkl")
# # ohe = joblib.load("airline_encoder.pkl")

# # st.set_page_config(page_title="Flight Price Predictor", layout="wide")

# # st.title("✈️ AI-based Flight Fare Prediction System")

# # # ================= INPUT UI =================
# # col1, col2 = st.columns(2)

# # with col1:
# #     source = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
# #     destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
# #     airline = st.selectbox("Airline", ['Jet Airways', 'IndiGo', 'Air India', 'SpiceJet', 'Multiple carriers'])

# # with col2:
# #     departure_time = st.datetime_input("Departure Time")
    
# #     # 🔥 IMPORTANT FIX: arrival must be after departure
# #     arrival_time = st.datetime_input(
# #         "Arrival Time",
# #         min_value=departure_time
# #     )
    
# #     stops = st.slider("Total Stops", 0, 4, 0)

# # # ================= VALIDATION =================
# # if arrival_time <= departure_time:
# #     st.error("❌ Arrival time must be AFTER departure time")

# # # ================= FEATURE ENGINEERING =================
# # def preprocess():
# #     dep_hour = departure_time.hour
# #     dep_min = departure_time.minute

# #     arr_hour = arrival_time.hour
# #     arr_min = arrival_time.minute

# #     duration = (arrival_time - departure_time).total_seconds() / 3600

# #     # base dataframe
# #     input_dict = {
# #         'Total_Stops': stops,
# #         'Journey_day': departure_time.day,
# #         'Journey_month': departure_time.month,
# #         'Dep_hour': dep_hour,
# #         'Dep_min': dep_min,
# #         'Arrival_hour': arr_hour,
# #         'Arrival_min': arr_min,
# #         'Duration': duration
# #     }

# #     df = pd.DataFrame([input_dict])

# #     # ================= ENCODING =================
# #     airline_encoded = ohe.transform([[airline]]).toarray()
# #     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out(['Airline']))

# #     df = pd.concat([df, airline_df], axis=1)

# #     # ================= SOURCE & DEST =================
# #     for col in columns:
# #         if col.startswith("Source_"):
# #             df[col] = 1 if col == f"Source_{source}" else 0
# #         if col.startswith("Destination_"):
# #             df[col] = 1 if col == f"Destination_{destination}" else 0

# #     # ================= MATCH COLUMN ORDER =================
# #     for col in columns:
# #         if col not in df.columns:
# #             df[col] = 0

# #     df = df[columns]

# #     # ================= SCALING =================
# #     df_scaled = scaler.transform(df)

# #     return df_scaled

# # # ================= PREDICTION =================
# # if st.button("Predict Price"):
# #     if arrival_time <= departure_time:
# #         st.error("❌ Fix time input first")
# #     else:
# #         final_input = preprocess()
# #         prediction = model.predict(final_input)

# #         st.success(f"💰 Estimated Price: ₹ {prediction[0]:,.2f}")




# import streamlit as st
# import pandas as pd
# import numpy as np
# import joblib
# from datetime import datetime, timedelta

# # -------------------------
# # PAGE CONFIG
# # -------------------------
# st.set_page_config(page_title="Flight Price Predictor", layout="wide")

# st.title("✈️ AI-based Flight Fare Prediction System")

# # -------------------------
# # LOAD FILES
# # -------------------------
# model = joblib.load("xgboost_model.pkl")
# scaler = joblib.load("scaler.pkl")
# columns = joblib.load("columns.pkl")
# ohe = joblib.load("airline_encoder.pkl")

# # -------------------------
# # INPUT UI
# # -------------------------
# col1, col2 = st.columns(2)

# with col1:
#     source = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
#     destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
#     airline = st.selectbox("Airline", [
#         'Air India', 'GoAir', 'IndiGo', 'Jet Airways',
#         'Jet Airways Business', 'Multiple carriers',
#         'Multiple carriers Premium economy', 'SpiceJet',
#         'Trujet', 'Vistara', 'Vistara Premium economy'
#     ])

# with col2:
#     departure_time = st.datetime_input("Departure Time", value=datetime.now())

#     # 🔥 Constraint: arrival must be after departure
#     arrival_time = st.datetime_input(
#         "Arrival Time",
#         value=departure_time + timedelta(hours=2),
#         min_value=departure_time
#     )

#     total_stops = st.slider("Total Stops", 0, 4, 0)

# # -------------------------
# # PREPROCESS FUNCTION
# # -------------------------
# def preprocess():
#     duration = arrival_time - departure_time
#     duration_hours = int(duration.total_seconds() // 3600)
#     duration_mins = int((duration.total_seconds() % 3600) // 60)

#     data = {
#         "Total_Stops": total_stops,
#         "Journey_day": departure_time.day,
#         "Journey_month": departure_time.month,
#         "Dep_hour": departure_time.hour,
#         "Dep_min": departure_time.minute,
#         "Arrival_hour": arrival_time.hour,
#         "Arrival_min": arrival_time.minute,
#         "Duration_hours": duration_hours,
#         "Duration_mins": duration_mins
#     }

#     df = pd.DataFrame([data])

#     # One-hot encode airline (FIXED ERROR HERE)
#     airline_encoded = ohe.transform([[airline]])

#     # Handle both sparse & dense safely
#     if hasattr(airline_encoded, "toarray"):
#         airline_encoded = airline_encoded.toarray()

#     airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())

#     # Combine
#     df = pd.concat([df, airline_df], axis=1)

#     # Add missing columns
#     for col in columns:
#         if col not in df.columns:
#             df[col] = 0

#     # Correct order
#     df = df[columns]

#     # Scale
#     df_scaled = scaler.transform(df)

#     return df_scaled

# # -------------------------
# # PREDICTION
# # -------------------------
# if st.button("Predict Price"):
#     if arrival_time <= departure_time:
#         st.error("❌ Arrival time must be AFTER departure time")
#     else:
#         final_input = preprocess()
#         prediction = model.predict(final_input)
#         final_price = np.expm1(prediction[0])

#         st.success(f"💰 Estimated Price: ₹ {final_price:,.2f}")

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import io
from datetime import datetime, timedelta

# -------------------------
# 1. PAGE CONFIG & STYLING
# -------------------------
st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

# Professional CSS for Dark Mode and Custom Cards
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; white-space: pre-wrap; background-color: #1b263b;
        border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
        color: white; border: none; padding: 12px; border-radius: 8px; width: 100%;
    }
    .price-card {
        background: #1b263b; padding: 30px; border-radius: 15px;
        text-align: center; border: 1px solid #415a77; margin-bottom: 20px;
    }
    .price-value { font-size: 3rem; font-weight: 800; color: #00AEEF; }
    </style>
    """, unsafe_allow_html=True)

# -------------------------
# 2. LOAD AI ASSETS
# -------------------------
@st.cache_resource
def load_assets():
    model = joblib.load("xgboost_model.pkl")
    scaler = joblib.load("scaler.pkl")
    columns = joblib.load("columns.pkl")
    ohe = joblib.load("airline_encoder.pkl")
    return model, scaler, columns, ohe

try:
    model, scaler, columns, ohe = load_assets()
except Exception as e:
    st.error(f"🚨 Model files missing: {e}")
    st.stop()

# -------------------------
# 3. HELPER FUNCTION: PREPROCESS
# -------------------------
def process_data(input_dict, airline_name):
    df = pd.DataFrame([input_dict])
    
    # One-hot encode airline
    airline_encoded = ohe.transform([[airline_name]])
    if hasattr(airline_encoded, "toarray"):
        airline_encoded = airline_encoded.toarray()
    
    airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
    df = pd.concat([df, airline_df], axis=1)

    # Ensure all columns exist and are in the correct order
    for col in columns:
        if col not in df.columns:
            df[col] = 0
    df = df[columns]
    
    # Scale and Predict
    df_scaled = scaler.transform(df)
    log_pred = model.predict(df_scaled)
    return np.expm1(log_pred[0]) # Reverse Log transformation

# -------------------------
# 4. MAIN UI - TABS
# -------------------------
st.title("✈️ AirFair Vista")
st.caption("Advanced AI Flight Fare Prediction System | Powered by XGBoost")

tab1, tab2 = st.tabs(["🎯 Single Prediction", "📊 Bulk Scanner"])

# --- TAB 1: SINGLE PREDICTION ---
with tab1:
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("📍 Journey Details")
        src = st.selectbox("Source City", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
        dest = st.selectbox("Destination City", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
        air = st.selectbox("Select Airline", ['IndiGo', 'Air India', 'Jet Airways', 'SpiceJet', 'Vistara', 'GoAir'])

    with col2:
        st.subheader("🕒 Schedule")
        dep = st.datetime_input("Departure Date & Time", value=datetime.now())
        arr = st.datetime_input("Arrival Date & Time", value=dep + timedelta(hours=2))
        stops = st.slider("Number of Stops", 0, 4, 0)

    if st.button("Calculate Estimated Fare"):
        if arr <= dep:
            st.error("Arrival must be after Departure!")
        else:
            duration = arr - dep
            dur_h = int(duration.total_seconds() // 3600)
            dur_m = int((duration.total_seconds() % 3600) // 60)
            
            input_features = {
                "Total_Stops": stops, "Journey_day": dep.day, "Journey_month": dep.month,
                "Dep_hour": dep.hour, "Dep_min": dep.minute, "Arrival_hour": arr.hour,
                "Arrival_min": arr.minute, "Duration_hours": dur_h, "Duration_mins": dur_m
            }
            
            final_price = process_data(input_features, air)
            
            st.markdown(f"""
                <div class="price-card">
                    <p style="color:#778da9; margin-bottom:0;">Estimated Ticket Price</p>
                    <h1 class="price-value">₹ {final_price:,.2f}</h1>
                    <p style="font-size:0.9rem;">{air} | {src} → {dest}</p>
                </div>
            """, unsafe_allow_html=True)
            st.balloons()

# --- TAB 2: BULK SCANNER ---
with tab2:
    st.subheader("📂 Bulk Flight Price Analysis")
    st.info("Upload a CSV with columns: Airline, Source, Destination, Dep_Time, Arrival_Time, Total_Stops")
    
    upload_col, info_col = st.columns([2, 1])
    
    with upload_col:
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    with info_col:
        # Template Download
        sample = pd.DataFrame({
            'Airline': ['IndiGo'], 'Source': ['Delhi'], 'Destination': ['Cochin'],
            'Dep_Time': ['2026-05-10 10:00'], 'Arrival_Time': ['2026-05-10 13:00'], 'Total_Stops': [0]
        })
        st.download_button("📩 Download CSV Template", sample.to_csv(index=False), "template.csv")

    if uploaded_file:
        df_bulk = pd.read_csv(uploaded_file)
        if st.button("🚀 Run Bulk Prediction"):
            with st.spinner("Analyzing flights..."):
                prices = []
                # Simple loop for demo; for huge files, use a vectorized approach
                for _, row in df_bulk.iterrows():
                    try:
                        d_t = pd.to_datetime(row['Dep_Time'])
                        a_t = pd.to_datetime(row['Arrival_Time'])
                        diff = a_t - d_t
                        feats = {
                            "Total_Stops": row['Total_Stops'], "Journey_day": d_t.day, "Journey_month": d_t.month,
                            "Dep_hour": d_t.hour, "Dep_min": d_t.minute, "Arrival_hour": a_t.hour,
                            "Arrival_min": a_t.minute, "Duration_hours": int(diff.total_seconds()//3600),
                            "Duration_mins": int((diff.total_seconds()%3600)//60)
                        }
                        prices.append(round(process_data(feats, row['Airline']), 2))
                    except:
                        prices.append(np.nan)
                
                df_bulk['Predicted_Price'] = prices
                st.write("### Preview of Results", df_bulk.head())
                st.download_button("📥 Download Results", df_bulk.to_csv(index=False), "predictions.csv")


