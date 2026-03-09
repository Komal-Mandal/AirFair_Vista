# import streamlit as st
# import pickle
# import numpy as np
# from datetime import datetime

# # Load trained model
# model = pickle.load(open("xgboost_model.pkl", "rb"))

# st.set_page_config(page_title="Flight Price Predictor", page_icon="✈️")

# st.title("✈️ Flight Price Prediction")
# st.write("Enter flight details to estimate ticket price")

# # Departure Time
# dep_time = st.datetime_input("Departure Time")

# # Arrival Time
# arr_time = st.datetime_input("Arrival Time")

# # Stops
# Total_stops = st.selectbox("Total Stops", [0,1,2,3,4])

# # Airline
# airline = st.selectbox(
#     "Airline",
#     [
#         'Jet Airways','IndiGo','Air India','Multiple carriers',
#         'SpiceJet','Vistara','GoAir',
#         'Multiple carriers Premium economy',
#         'Jet Airways Business',
#         'Vistara Premium economy','Trujet'
#     ]
# )

# # Source
# Source = st.selectbox(
#     "Source",
#     ['Delhi','Kolkata','Mumbai','Chennai']
# )

# # Destination
# Destination = st.selectbox(
#     "Destination",
#     ['Cochin','Delhi','New_Delhi','Hyderabad','Kolkata']
# )

# # -------------------------
# # Feature Engineering
# # -------------------------

# Journey_day = dep_time.day
# Journey_month = dep_time.month

# Dep_hour = dep_time.hour
# Dep_min = dep_time.minute

# Arrival_hour = arr_time.hour
# Arrival_min = arr_time.minute

# # -------------------------
# # Duration Validation
# # -------------------------

# duration = arr_time - dep_time

# if duration.total_seconds() <= 0:
#     dur_hour = 0
#     dur_min = 0
#     st.warning("⚠️ Arrival time must be after departure time.")
# else:
#     dur_hour = int(duration.total_seconds() // 3600)
#     dur_min = int((duration.total_seconds() % 3600) // 60)

# # -------------------------
# # Airline Encoding
# # -------------------------

# Jet_Airways=IndiGo=Air_India=Multiple_carriers=SpiceJet=Vistara=GoAir=0
# Multiple_carriers_Premium_economy=Jet_Airways_Business=Vistara_Premium_economy=Trujet=0

# if airline == 'Jet Airways':
#     Jet_Airways = 1
# elif airline == 'IndiGo':
#     IndiGo = 1
# elif airline == 'Air India':
#     Air_India = 1
# elif airline == 'Multiple carriers':
#     Multiple_carriers = 1
# elif airline == 'SpiceJet':
#     SpiceJet = 1
# elif airline == 'Vistara':
#     Vistara = 1
# elif airline == 'GoAir':
#     GoAir = 1
# elif airline == 'Multiple carriers Premium economy':
#     Multiple_carriers_Premium_economy = 1
# elif airline == 'Jet Airways Business':
#     Jet_Airways_Business = 1
# elif airline == 'Vistara Premium economy':
#     Vistara_Premium_economy = 1
# elif airline == 'Trujet':
#     Trujet = 1

# # -------------------------
# # Source Encoding
# # -------------------------

# s_Delhi=s_Kolkata=s_Mumbai=s_Chennai=0

# if Source == "Delhi":
#     s_Delhi=1
# elif Source == "Kolkata":
#     s_Kolkata=1
# elif Source == "Mumbai":
#     s_Mumbai=1
# elif Source == "Chennai":
#     s_Chennai=1

# # -------------------------
# # Destination Encoding
# # -------------------------

# d_Cochin=d_Delhi=d_New_Delhi=d_Hyderabad=d_Kolkata=0

# if Destination == "Cochin":
#     d_Cochin=1
# elif Destination == "Delhi":
#     d_Delhi=1
# elif Destination == "New_Delhi":
#     d_New_Delhi=1
# elif Destination == "Hyderabad":
#     d_Hyderabad=1
# elif Destination == "Kolkata":
#     d_Kolkata=1

# # -------------------------
# # Prediction
# # -------------------------

# if st.button("Predict Price 💰"):

#     if duration.total_seconds() <= 0:
#         st.error("❌ Please select valid arrival time.")
#     else:
#         try:

#             features = [[
#                 Total_stops,
#                 Journey_day,
#                 Journey_month,
#                 Dep_hour,
#                 Dep_min,
#                 Arrival_hour,
#                 Arrival_min,
#                 dur_hour,
#                 dur_min,
#                 Air_India,
#                 GoAir,
#                 IndiGo,
#                 Jet_Airways,
#                 Jet_Airways_Business,
#                 Multiple_carriers,
#                 Multiple_carriers_Premium_economy,
#                 SpiceJet,
#                 Trujet,
#                 Vistara,
#                 Vistara_Premium_economy,
#                 s_Chennai,
#                 s_Delhi,
#                 s_Kolkata,
#                 s_Mumbai,
#                 d_Cochin,
#                 d_Delhi,
#                 d_Hyderabad,
#                 d_Kolkata,
#                 d_New_Delhi
#             ]]

#             prediction = model.predict(features)

#             price = round(np.exp(prediction[0]))

#             st.success(f"💰 Estimated Flight Price: ₹ {price:,}")

#         except Exception as e:

#             st.error("Prediction Error")
#             st.write(e)

import streamlit as st
import pickle
import numpy as np
from datetime import datetime, timedelta

# Load trained model
model = pickle.load(open("xgboost_model.pkl", "rb"))

st.set_page_config(page_title="Flight Price Predictor", page_icon="✈️")

st.title("✈️ Flight Price Prediction")
st.write("Enter flight details to estimate ticket price")

# -------------------------
# User Inputs
# -------------------------

dep_time = st.datetime_input("Departure Time")
arr_time = st.datetime_input("Arrival Time")

Total_stops = st.selectbox("Total Stops", [0,1,2,3,4])

airline = st.selectbox(
    "Airline",
    [
        'Jet Airways','IndiGo','Air India','Multiple carriers',
        'SpiceJet','Vistara','GoAir',
        'Multiple carriers Premium economy',
        'Jet Airways Business',
        'Vistara Premium economy','Trujet'
    ]
)

Source = st.selectbox(
    "Source",
    ['Delhi','Kolkata','Mumbai','Chennai']
)

Destination = st.selectbox(
    "Destination",
    ['Cochin','Delhi','New_Delhi','Hyderabad','Kolkata']
)

# -------------------------
# Feature Engineering
# -------------------------

Journey_day = dep_time.day
Journey_month = dep_time.month

Dep_hour = dep_time.hour
Dep_min = dep_time.minute

Arrival_hour = arr_time.hour
Arrival_min = arr_time.minute

# -------------------------
# Duration Calculation
# -------------------------

duration = arr_time - dep_time

# Handle overnight flights
if duration.total_seconds() < 0:
    arr_time = arr_time + timedelta(days=1)
    duration = arr_time - dep_time

# Prevent zero duration
if duration.total_seconds() == 0:
    st.error("❌ Arrival time must be after departure time.")
    st.stop()

dur_hour = int(duration.total_seconds() // 3600)
dur_min = int((duration.total_seconds() % 3600) // 60)

# Warn if duration unrealistic
if duration.days > 2:
    st.warning("⚠️ Flight duration seems unrealistic.")

# -------------------------
# Airline Encoding
# -------------------------

Jet_Airways=IndiGo=Air_India=Multiple_carriers=SpiceJet=Vistara=GoAir=0
Multiple_carriers_Premium_economy=Jet_Airways_Business=Vistara_Premium_economy=Trujet=0

if airline == 'Jet Airways':
    Jet_Airways = 1
elif airline == 'IndiGo':
    IndiGo = 1
elif airline == 'Air India':
    Air_India = 1
elif airline == 'Multiple carriers':
    Multiple_carriers = 1
elif airline == 'SpiceJet':
    SpiceJet = 1
elif airline == 'Vistara':
    Vistara = 1
elif airline == 'GoAir':
    GoAir = 1
elif airline == 'Multiple carriers Premium economy':
    Multiple_carriers_Premium_economy = 1
elif airline == 'Jet Airways Business':
    Jet_Airways_Business = 1
elif airline == 'Vistara Premium economy':
    Vistara_Premium_economy = 1
elif airline == 'Trujet':
    Trujet = 1

# -------------------------
# Source Encoding
# -------------------------

s_Delhi=s_Kolkata=s_Mumbai=s_Chennai=0

if Source == "Delhi":
    s_Delhi=1
elif Source == "Kolkata":
    s_Kolkata=1
elif Source == "Mumbai":
    s_Mumbai=1
elif Source == "Chennai":
    s_Chennai=1

# -------------------------
# Destination Encoding
# -------------------------

d_Cochin=d_Delhi=d_New_Delhi=d_Hyderabad=d_Kolkata=0

if Destination == "Cochin":
    d_Cochin=1
elif Destination == "Delhi":
    d_Delhi=1
elif Destination == "New_Delhi":
    d_New_Delhi=1
elif Destination == "Hyderabad":
    d_Hyderabad=1
elif Destination == "Kolkata":
    d_Kolkata=1

# -------------------------
# Prediction
# -------------------------

if st.button("Predict Price 💰"):

    try:

        features = [[
            Total_stops,
            Journey_day,
            Journey_month,
            Dep_hour,
            Dep_min,
            Arrival_hour,
            Arrival_min,
            dur_hour,
            dur_min,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Trujet,
            Vistara,
            Vistara_Premium_economy,
            s_Chennai,
            s_Delhi,
            s_Kolkata,
            s_Mumbai,
            d_Cochin,
            d_Delhi,
            d_Hyderabad,
            d_Kolkata,
            d_New_Delhi
        ]]

        prediction = model.predict(features)

        price = round(np.exp(prediction[0]))

        st.success(f"💰 Estimated Flight Price: ₹ {price:,}")

    except Exception as e:

        st.error("Prediction Error")
        st.write(e)