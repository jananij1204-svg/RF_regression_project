import streamlit as st
import pandas as pd
import pickle

# load pipeline
with open("pipeline_model.pkl", "rb") as f:
    model = pickle.load(f)


st.title("House Price Prediction App")

# Inputs (keep categorical as strings)
year_built = st.number_input("Year Built", 1800, 2050, 2000)
bathrooms = st.number_input("Number of Bathrooms", 0.0, 10.0, 2.0)
sqft = st.number_input("Square Feet (sqft)", 200, 20000, 1200)
house_type = st.selectbox("House Type", ["Detached", "Semi-Detached", "Townhouse", "Condo"])
condition = st.selectbox("Condition", ["Poor", "Fair", "Good", "Excellent"])
location = st.selectbox("Location", ["City Center", "Suburban", "Rural"])
bedrooms = st.number_input("Bedrooms", 0, 20, 3)
school_rating = st.number_input("School Rating (0–10)", 0, 10, 7)
has_fireplace = st.selectbox("Has Fireplace?", ["Yes", "No"])
garage = st.number_input("Garage Capacity (0–5)", 0, 5, 1)
lot_size = st.number_input("Lot Size (sqft)", 200, 50000, 3000)
has_pool = st.selectbox("Has Pool?", ["Yes", "No"])
has_basement = st.selectbox("Has Basement?", ["Yes", "No"])
age = st.number_input("Age of House", 0, 300, 20)

# build input dataframe
input_df = pd.DataFrame([{
    "year_built": year_built,
    "bathrooms": bathrooms,
    "sqft": sqft,
    "house_type": house_type,
    "condition": condition,
    "location": location,
    "bedrooms": bedrooms,
    "school_rating": school_rating,
    "has_fireplace": has_fireplace,
    "garage": garage,
    "lot_size": lot_size,
    "has_pool": has_pool,
    "has_basement": has_basement,
    "age": age
}])

# predict
if st.button("Predict Price"):
    try:
        prediction = model.predict(input_df)[0]
        st.success(f"Predicted House Price: ₹ {prediction:,.2f}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
