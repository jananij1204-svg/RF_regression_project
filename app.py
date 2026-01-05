import streamlit as st
import pickle
import pandas as pd

# Load model
def load_model():
    with open("housing_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

st.title("House Price Prediction App")

# ======= INPUT FIELDS =======

year_built = st.number_input("Year Built", min_value=1800, max_value=2050, value=2000)
bathrooms = st.number_input("Number of Bathrooms", min_value=0.0, value=2.0)

# 👉 Missing sqft field (ADDED now)
sqft = st.number_input("Square Feet (sqft)", min_value=200, max_value=10000, value=1200)

# categorical (should remain strings!)
house_type = st.selectbox("House Type", ["Detached", "Semi-Detached", "Townhouse", "Condo"])
condition = st.selectbox("Condition", ["Poor", "Fair", "Good", "Excellent"])
location = st.selectbox("Location", ["City Center", "Suburban", "Rural"])

bedrooms = st.number_input("Bedrooms", min_value=0, max_value=20, value=3)
school_rating = st.number_input("School Rating (0–10)", min_value=0, max_value=10, value=7)

has_fireplace = st.selectbox("Has Fireplace?", ["Yes", "No"])
garage = st.number_input("Garage Capacity (0–5)", min_value=0, max_value=5, value=1)
lot_size = st.number_input("Lot Size (sqft)", min_value=200, max_value=50000, value=3000)

has_pool = st.selectbox("Has Pool?", ["Yes", "No"])
has_basement = st.selectbox("Has Basement?", ["Yes", "No"])
age = st.number_input("Age of House", min_value=0, max_value=300, value=20)

# Convert only the binary ones
binary_map = {"Yes": 1, "No": 0}
has_fireplace = binary_map[has_fireplace]
has_pool = binary_map[has_pool]
has_basement = binary_map[has_basement]

# ======= BUILD INPUT DATAFRAME =======

input_data = pd.DataFrame([{
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

# ======= PREDICT =======

if st.button("Predict Price"):
    try:
        prediction = model.predict(input_data)[0]
        st.success(f"Predicted House Price: ₹ {prediction:,.2f}")
    except Exception as e:
        st.error(f"Prediction failed: {e}")
