import gradio as gr
import skops.io as sio

pipe = sio.load("./Model/diabetes_pipeline.skops", trusted=True)

def predict_diabetes(pregnancies, glucose, blood_pressure, skin_thickness,
                     insulin, bmi, diabetes_pedigree, age):

    features = [
        pregnancies, glucose, blood_pressure, skin_thickness,
        insulin, bmi, diabetes_pedigree, age
    ]

    prediction = pipe.predict([features])[0]
    label = "Diabetic" if prediction == 1 else "Non-Diabetic"
    return f"Prediction: {label}"

inputs = [
    gr.Slider(0, 17, step=1, label="Pregnancies"),
    gr.Slider(0, 200, step=1, label="Glucose"),
    gr.Slider(0, 122, step=1, label="Blood Pressure"),
    gr.Slider(0, 100, step=1, label="Skin Thickness"),
    gr.Slider(0, 846, step=1, label="Insulin"),
    gr.Slider(0.0, 67.1, step=0.1, label="BMI"),
    gr.Slider(0.078, 2.42, step=0.01, label="Diabetes Pedigree Function"),
    gr.Slider(21, 81, step=1, label="Age"),
]

examples = [
    [2, 120, 70, 20, 80, 25.3, 0.28, 35],
    [0, 150, 82, 30, 90, 33.6, 0.41, 28],
]

gr.Interface(
    fn=predict_diabetes,
    inputs=inputs,
    outputs=gr.Label(),
    examples=examples,
    title="Diabetes Prediction App",
    description="Enter patient data to predict diabetes",
    theme=gr.themes.Soft()
).launch()