import streamlit as st
import pickle
import pandas as pd
import numpy as np

# ------------------------------------------
# Load Model
# ------------------------------------------
@st.cache_resource
def load_model():
    with open("housing_model (1).pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# Extract expected column names from preprocessor
expected_columns = model.named_steps['preprocess'].transformers_[0][2] + \
                   model.named_steps['preprocess'].transformers_[1][2]

st.title("🏡 House Price Prediction App")

st.write("Enter the house details below to estimate the price.")

# ------------------------------------------
# UI Inputs (must match training columns)
# ------------------------------------------

year_built = st.number_input("Year Built", min_value=1800, max_value=2025, step=1, value=2000)
bathrooms = st.number_input("Number of Bathrooms", min_value=0.0, max_value=10.0, step=0.5, value=2.0)
sqft = st.number_input("Square Feet (sqft)", min_value=200, max_value=10000, step=50, value=1200)

house_type = st.selectbox("House Type", ["Detached", "Semi-Detached", "Apartment", "Townhouse"])

condition = st.selectbox("Condition", ["Poor", "Average", "Good", "Excellent"])

location = st.selectbox("Location", ["City Center", "Suburbs", "Rural"])

bedrooms = st.number_input("Bedrooms", min_value=0, max_value=10, step=1, value=3)

school_rating = st.number_input("School Rating (0–10)", min_value=0, max_value=10, step=1, value=7)

has_fireplace = st.selectbox("Has Fireplace?", ["Yes", "No"])
garage = st.number_input("Garage Capacity (0–5)", min_value=0, max_value=5, step=1, value=1)
lot_size = st.number_input("Lot Size (sqft)", min_value=200, max_value=20000, step=50, value=3000)
has_pool = st.selectbox("Has Pool?", ["Yes", "No"])
has_basement = st.selectbox("Has Basement?", ["Yes", "No"])
age = st.number_input("Age of House", min_value=0, max_value=200, step=1, value=20)

# Convert Yes/No → True/False
yn = lambda x: True if x == "Yes" else False

# ------------------------------------------
# Prepare input for prediction
# ------------------------------------------

input_dict = {
    "year_built": year_built,
    "bathrooms": bathrooms,
    "sqft": sqft,
    "house_type": house_type,
    "condition": condition,
    "location": location,
    "bedrooms": bedrooms,
    "school_rating": school_rating,
    "has_fireplace": yn(has_fireplace),
    "garage": garage,
    "lot_size": lot_size,
    "has_pool": yn(has_pool),
    "has_basement": yn(has_basement),
    "age": age
}

# Convert to DataFrame with correct column order
input_df = pd.DataFrame([input_dict])

missing_cols = set(expected_columns) - set(input_df.columns)
if missing_cols:
    st.error(f"Error: Missing columns in input: {missing_cols}")

# ------------------------------------------
# Predict Button
# ------------------------------------------
if st.button("Predict Price"):
    try:
        price = model.predict(input_df)[0]
        st.success(f"🏠 Estimated House Price: **₹ {price:,.2f}**")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
