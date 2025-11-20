import streamlit as st
import pandas as pd
import numpy as np
import skops.io as sio
from skops.io import get_untrusted_types

# Charger les types non fiables
untrusted = get_untrusted_types()

# Charger le modèle SKOPS
model = sio.load("Model/diabetes_pipeline.skops", trusted=untrusted)

st.title("Prédiction du diabète")

pregnancies = st.number_input("Pregnancies", 0, 20, 0)
glucose = st.number_input("Glucose", 0, 200, 120)
blood_pressure = st.number_input("Blood Pressure", 0, 150, 70)
skin_thickness = st.number_input("Skin Thickness", 0, 100, 20)
insulin = st.number_input("Insulin", 0, 900, 80)
bmi = st.number_input("BMI", 0.0, 70.0, 25.0)
dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5)
age = st.number_input("Age", 1, 120, 30)

data = np.array([[pregnancies, glucose, blood_pressure, skin_thickness,
                  insulin, bmi, dpf, age]])

if st.button("Predict"):
    pred = model.predict(data)[0]
    if pred == 1:
        st.error("⚠️ Le patient est probablement diabétique.")
    else:
        st.success("✓ Le patient n'est probablement pas diabétique.")