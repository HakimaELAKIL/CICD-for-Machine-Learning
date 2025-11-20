# App/diabete_app.py
import gradio as gr
import skops.io as sio
import pandas as pd

# Charger le modèle
model = sio.load("Model/diabetes_pipeline.skops", trusted=["sklearn", "numpy", "pandas"])

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