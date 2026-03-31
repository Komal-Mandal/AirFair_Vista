import streamlit as st
import pandas as pd
import numpy as np
import joblib
import io
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# -------------------------
# 1. PAGE CONFIG & STYLING
# -------------------------
st.set_page_config(page_title="AirFair Vista | AI Price Intelligence", page_icon="✈️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #1b263b;
        border-radius: 10px 10px 0px 0px; color: white; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { background-color: #00AEEF !important; font-weight: bold; }
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #00AEEF 0%, #0077b6 100%);
        color: white; border: none; border-radius: 8px; width: 100%; height: 45px;
    }
    .price-card {
        background: #1b263b; padding: 30px; border-radius: 15px;
        text-align: center; border: 1px solid #415a77; margin-top: 20px;
    }
    .price-value { font-size: 3.5rem; font-weight: 800; color: #00AEEF; margin: 10px 0; }
    </style>
    """, unsafe_allow_html=True)

# -------------------------
# 2. LOAD & CLEAN ASSETS
# -------------------------
@st.cache_resource
def load_assets():
    model = joblib.load("xgboost_model.pkl")
    scaler = joblib.load("scaler.pkl")
    columns = joblib.load("columns.pkl")
    ohe = joblib.load("airline_encoder.pkl")
    
    try:
        # Load Raw Data
        df = pd.read_excel("Data_Train.xlsx", engine='openpyxl')
        
        # --- FEATURE ENGINEERING FOR HEATMAP ---
        if 'Total_Stops' in df.columns:
            df['Total_Stops'] = df['Total_Stops'].replace('non-stop', '0 stops')
            df['Total_Stops'] = df['Total_Stops'].str.extract('(\d+)').fillna(0).astype(int)
            
        if 'Date_of_Journey' in df.columns:
            df['Date_of_Journey'] = pd.to_datetime(df['Date_of_Journey'], dayfirst=True)
            df['Journey_day'] = df['Date_of_Journey'].dt.day
            df['Journey_month'] = df['Date_of_Journey'].dt.month
            
        if 'Duration' in df.columns:
            def convert_duration(duration):
                h = 0
                m = 0
                if 'h' in duration: h = int(duration.split('h')[0])
                if 'm' in duration: m = int(duration.split('m')[0].split()[-1])
                return (h * 60) + m
            df['Duration_minutes'] = df['Duration'].apply(convert_duration)

    except Exception as e:
        st.warning(f"Note: Data_Train.xlsx processing skipped or failed: {e}")
        df = pd.DataFrame()
        
    return model, scaler, columns, ohe, df

model, scaler, columns, ohe, training_data = load_assets()

# -------------------------
# 3. PREDICTION LOGIC
# -------------------------
def predict_price(input_dict, airline_name):
    df = pd.DataFrame([input_dict])
    airline_encoded = ohe.transform([[airline_name]])
    if hasattr(airline_encoded, "toarray"):
        airline_encoded = airline_encoded.toarray()
    airline_df = pd.DataFrame(airline_encoded, columns=ohe.get_feature_names_out())
    df = pd.concat([df, airline_df], axis=1)
    for col in columns:
        if col not in df.columns:
            df[col] = 0
    df = df[columns]
    df_scaled = scaler.transform(df)
    return np.expm1(model.predict(df_scaled)[0])

# -------------------------
# 4. UI STRUCTURE
# -------------------------
st.title("✈️ AirFair Vista")
st.caption("Advanced AI Flight Intelligence | BrainyBeam Internship Project")

tab1, tab2, tab3 = st.tabs(["🎯 Prediction", "📊 Bulk Scanner", "📈 Advanced EDA"])

# --- TAB 1: SINGLE PREDICTION ---
with tab1:
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.subheader("📍 Journey Details")
        src = st.selectbox("Source", ['Delhi', 'Kolkata', 'Mumbai', 'Chennai'])
        dest = st.selectbox("Destination", ['Cochin', 'Delhi', 'New Delhi', 'Hyderabad', 'Kolkata'])
        
        # ADDED: Jet Airways Business included back in the list
        air = st.selectbox("Airline", [
            'IndiGo', 'Air India', 'Jet Airways', 'Jet Airways Business', 
            'SpiceJet', 'Vistara', 'GoAir', 'Multiple carriers', 
            'Air Asia', 'Vistara Premium economy'
        ])
    
    with col2:
        st.subheader("🕒 Schedule")
        # FIX: Define Departure
        dep = st.datetime_input("Departure Time", value=datetime.now())
        
        # FIX: Arrival restricted to be after Departure
        arr = st.datetime_input("Arrival Time", value=dep + timedelta(hours=2), min_value=dep)
        
        stops = st.slider("Total Stops", 0, 4, 0)

    if st.button("Predict Fare"):
        # Validation: Arrival cannot be same as or before departure
        if arr <= dep:
            st.error("❌ Invalid Schedule: Arrival must be after Departure.")
        else:
            duration = arr - dep
            dur_h = int(duration.total_seconds() // 3600)
            dur_m = int((duration.total_seconds() % 3600) // 60)
            
            feats = {
                "Total_Stops": stops, 
                "Journey_day": dep.day, 
                "Journey_month": dep.month, 
                "Dep_hour": dep.hour, 
                "Dep_min": dep.minute, 
                "Arrival_hour": arr.hour, 
                "Arrival_min": arr.minute, 
                "Duration_hours": dur_h, 
                "Duration_mins": dur_m
            }
            
            price = predict_price(feats, air)
            st.markdown(f"""
                <div class="price-card">
                    <p>Estimated Fare</p>
                    <h1 class="price-value">₹ {price:,.2f}</h1>
                    <p style="color: #00AEEF;">Flight Duration: {dur_h}h {dur_m}m</p>
                </div>
            """, unsafe_allow_html=True)

# --- TAB 2: BULK SCANNER ---
with tab2:
    st.subheader("📂 Batch Prediction")
    uploaded_file = st.file_uploader("Upload CSV/Excel/JSON", type=["csv", "xlsx", "json"])
    if uploaded_file:
        st.success("File uploaded successfully. Click 'Process' to begin.")

# --- TAB 3: ADVANCED EDA ---
with tab3:
    st.subheader("📈 Exploratory Data Analysis")
    
    if not training_data.empty:
        st.markdown("##### 1. Full Multi-Feature Correlation Matrix")
        numeric_df = training_data.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()
        fig_corr = px.imshow(corr_matrix, text_auto=".2f", color_continuous_scale='RdBu_r', aspect="auto")
        fig_corr.update_layout(height=500, paper_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
        st.plotly_chart(fig_corr, use_container_width=True)

        st.divider()

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("##### 2. Price Distribution by Airline")
            fig_box = px.box(training_data, x="Airline", y="Price", color_discrete_sequence=['#00AEEF'])
            fig_box.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
            st.plotly_chart(fig_box, use_container_width=True)

        with c2:
            st.markdown("##### 3. Price Density by Stops")
            fig_vio = px.violin(training_data, x="Total_Stops", y="Price", box=True, points="all", color_discrete_sequence=['#00AEEF'])
            fig_vio.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
            st.plotly_chart(fig_vio, use_container_width=True)

        st.divider()

        c3, c4 = st.columns(2)
        with c3:
            st.markdown("##### 4. Average Fare Monthly Trend")
            monthly = training_data.groupby('Journey_month')['Price'].mean()
            fig_line = px.line(x=monthly.index, y=monthly.values, markers=True)
            fig_line.update_traces(line_color='#00AEEF', line_width=4)
            fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
            st.plotly_chart(fig_line, use_container_width=True)

        with c4:
            st.markdown("##### 5. Duration vs Price Intensity")
            fig_dens = px.density_heatmap(training_data, x="Duration_minutes", y="Price", color_continuous_scale='Blues')
            fig_dens.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font={'color':"white"})
            st.plotly_chart(fig_dens, use_container_width=True)

    else:
        st.error("⚠️ Data_Train.xlsx not found. Visuals restricted.")