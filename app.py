import pandas as pd
import streamlit as st

if st.button("Predict Price 💰"):
    
    input_data = {
        "Total_Stops": Total_stops,
        "Journey_day": Journey_day,
        "Journey_month": Journey_month,
        "Dep_hour": Dep_hour,
        "Dep_min": Dep_min,
        "Arrival_hour": Arrival_hour,
        "Arrival_min": Arrival_min,
        "Duration_hours": dur_hour,
        "Duration_mins": dur_min,
        "Airline_Air India": Air_India,
        "Airline_GoAir": GoAir,
        "Airline_IndiGo": IndiGo,
        "Airline_Jet Airways": Jet_Airways,
        "Airline_Jet Airways Business": Jet_Airways_Business,
        "Airline_Multiple carriers": Multiple_carriers,
        "Airline_Multiple carriers Premium economy": Multiple_carriers_Premium_economy,
        "Airline_SpiceJet": SpiceJet,
        "Airline_Trujet": Trujet,
        "Airline_Vistara": Vistara,
        "Airline_Vistara Premium economy": Vistara_Premium_economy,
        "Source_Chennai": s_Chennai,
        "Source_Delhi": s_Delhi,
        "Source_Kolkata": s_Kolkata,
        "Source_Mumbai": s_Mumbai,
        "Destination_Cochin": d_Cochin,
        "Destination_Delhi": d_Delhi,
        "Destination_Hyderabad": d_Hyderabad,
        "Destination_Kolkata": d_Kolkata,
        "Destination_New_Delhi": d_New_Delhi
    }

    df = pd.DataFrame([input_data])

    prediction = model.predict(df)[0]

    price = round(prediction)

    st.success(f"💰 Estimated Flight Price: ₹ {price:,}")