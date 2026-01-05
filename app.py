import streamlit as st
import numpy as np
import pickle

# -------------------------------
# Load Model
# -------------------------------
@st.cache_resource
def load_model():
    with open("/mnt/data/housing_model.pkl", "rb") as f:
        return pickle.load(f)

model = load_model()

# -------------------------------
# App Title
# -------------------------------
st.title("🏠 House Price Prediction App")
st.write("Enter the house details below to predict the price.")

# -------------------------------
# Input Fields (Change based on features)
# -------------------------------
# ⚠ IMPORTANT:
# Make sure these input features match the same order used while training your model.

col1, col2 = st.columns(2)

with col1:
    area = st.number_input("House Area (sq ft)", min_value=200, max_value=10000, step=50)
    bedrooms = st.number_input("Number of Bedrooms", min_value=1, max_value=10, step=1)
    bathrooms = st.number_input("Number of Bathrooms", min_value=1, max_value=10, step=1)

with col2:
    stories = st.number_input("Number of Stories", min_value=1, max_value=5, step=1)
    parking = st.number_input("Parking Spaces", min_value=0, max_value=5, step=1)
    age = st.number_input("House Age (Years)", min_value=0, max_value=100, step=1)

# -------------------------------
# Prediction
# -------------------------------
if st.button("Predict Price"):
    input_data = np.array([[area, bedrooms, bathrooms, stories, parking, age]])

    prediction = model.predict(input_data)[0]

    st.success(f"💰 Estimated House Price: **₹ {prediction:,.2f}**")
