import streamlit as st
import pandas as pd
import numpy as np
import skops.io as sio

import skops.io as sio
from skops.io import get_untrusted_types

# Charger les types non fiables
untrusted = get_untrusted_types("Model/diabetes_pipeline.skops")

# Charger le modèle en approuvant ces types
model = sio.load("Model/diabetes_pipeline.skops", trusted=untrusted)

st.title("Prédiction du diabète")

# Inputs
preg = st.number_input("Nombre de grossesses", 0, 20, 1)
glucose = st.number_input("Taux de glucose", 0, 300, 120)
bp = st.number_input("Pression artérielle", 0, 150, 70)
skin = st.number_input("Épaisseur de la peau", 0, 99, 20)
insulin = st.number_input("Insuline", 0, 900, 80)
bmi = st.number_input("Indice IMC", 0.0, 70.0, 25.0)
dpf = st.number_input("Pedigree du diabète", 0.0, 5.0, 0.5)
age = st.number_input("Âge", 1, 120, 30)

if st.button("Prédire"):
    X = [[preg, glucose, bp, skin, insulin, bmi, dpf, age]]
    result = model.predict(X)[0]
    st.success(f"Résultat : {'Diabétique' if result == 1 else 'Non diabétique'}")