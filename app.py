import streamlit as st
import pandas as pd
import pickle

# -------------------------------
# Load Model
# -------------------------------
@st.cache_resource
def load_model():
    with open("housing_model (2).pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# -------------------------------
# UI Title
# -------------------------------
st.title("🏡 House Price Prediction App")

# -------------------------------
# Input Fields
# -------------------------------
year_built = st.number_input("Year Built", 1800, 2030, 2000)
bathrooms = st.number_input("Number of Bathrooms", 0.0, 10.0, 2.0, step=0.5)
sqft = st.number_input("Square Feet (sqft)", 300, 10000, 1200)

house_type = st.selectbox("House Type", ["Detached", "Semi-Detached", "Apartment", "Townhouse"])
condition = st.selectbox("Condition", ["Poor", "Average", "Good", "Excellent"])
location = st.selectbox("Location", ["City Center", "Suburbs", "Rural"])

bedrooms = st.number_input("Bedrooms", 0, 10, 3)
school_rating = st.number_input("School Rating (0–10)", 0, 10, 7)

fireplace = st.selectbox("Has Fireplace?", ["Yes", "No"])
garage = st.number_input("Garage Capacity (0–5)", 0, 5, 1)
lot_size = st.number_input("Lot Size (sqft)", 200, 20000, 3000)

pool = st.selectbox("Has Pool?", ["Yes", "No"])
basement = st.selectbox("Has Basement?", ["Yes", "No"])

age = st.number_input("Age of House", 0, 200, 20)

# Convert Yes/No to actual categories expected by encoder
fireplace = "Yes" if fireplace == "Yes" else "No"
pool = "Yes" if pool == "Yes" else "No"
basement = "Yes" if basement == "Yes" else "No"

# -------------------------------
# Create Input DataFrame
# -------------------------------
input_data = pd.DataFrame([{
    "year_built": year_built,
    "bathrooms": bathrooms,
    "sqft": sqft,
    "bedrooms": bedrooms,
    "school_rating": school_rating,
    "garage": garage,
    "lot_size": lot_size,
    "age": age,
    "house_type": house_type,
    "condition": condition,
    "location": location,
    "has_fireplace": fireplace,
    "has_pool": pool,
    "has_basement": basement
}])

# -------------------------------
# Prediction
# -------------------------------
if st.button("Predict Price"):
    try:
        prediction = model.predict(input_data)[0]
        st.success(f"Predicted House Price: ₹ {prediction:,.2f}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
