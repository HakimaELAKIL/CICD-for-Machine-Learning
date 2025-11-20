# App/diabete_app.py
import gradio as gr
import skops.io as sio
from skops.io._persist import get_untrusted_types
import pandas as pd

# Charger le modèle en mode sûr
untrusted = get_untrusted_types(file="Model/diabetes_pipeline.skops")
model = sio.load("Model/diabetes_pipeline.skops", trusted=untrusted)

# Fonction de prédiction
def predict_diabetes(Age, BMI, Glucose, BloodPressure, Insulin, SkinThickness, DPF, Pregnancies):
    data = pd.DataFrame([[Age, BMI, Glucose, BloodPressure, Insulin, SkinThickness, DPF, Pregnancies]],
                        columns=["Age", "BMI", "Glucose", "BloodPressure", "Insulin", "SkinThickness",
                                 "DiabetesPedigreeFunction", "Pregnancies"])
    pred = model.predict(data)
    return "Diabetic" if pred[0] == 1 else "Non-Diabetic"

# Interface Gradio
iface = gr.Interface(
    fn=predict_diabetes,
    inputs=[
        gr.Number(label="Age"),
        gr.Number(label="BMI"),
        gr.Number(label="Glucose"),
        gr.Number(label="Blood Pressure"),
        gr.Number(label="Insulin"),
        gr.Number(label="Skin Thickness"),
        gr.Number(label="Diabetes Pedigree Function (DPF)"),
        gr.Number(label="Pregnancies")
    ],
    outputs=gr.Text(label="Prediction"),
    title="Diabetes Prediction",
    description="Predict if a patient is diabetic based on 8 medical features"
)

if __name__ == "__main__":
    iface.launch()