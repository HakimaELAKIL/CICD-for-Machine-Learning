# App/diabete_app.py
import gradio as gr
import skops.io as sio
from skops.io._persist import get_untrusted_types
import pandas as pd

# Charger le modèle en mode sûr
# 1️⃣ Obtenir les types non fiables à partir du fichier
untrusted = get_untrusted_types(file="Model/diabetes_pipeline.skops")

# 2️⃣ Charger le modèle en ajoutant ces types à trusted
model = sio.load("Model/diabetes_pipeline.skops", trusted=untrusted)

# Fonction de prédiction
def predict_diabetes(Age, BMI, Glucose, BloodPressure):
    data = pd.DataFrame([[Age, BMI, Glucose, BloodPressure]],
                        columns=["Age", "BMI", "Glucose", "BloodPressure"])
    pred = model.predict(data)
    return "Diabetic" if pred[0] == 1 else "Non-Diabetic"

# Interface Gradio
iface = gr.Interface(
    fn=predict_diabetes,
    inputs=[
        gr.Number(label="Age"),
        gr.Number(label="BMI"),
        gr.Number(label="Glucose"),
        gr.Number(label="Blood Pressure")
    ],
    outputs=gr.Text(label="Prediction"),
    title="Diabetes Prediction",
    description="Predict if a patient is diabetic based on simple features"
)

if __name__ == "__main__":
    iface.launch()
