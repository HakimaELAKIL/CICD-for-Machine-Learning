import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay
import skops.io as sio

# Créer les dossiers si nécessaire
os.makedirs("Model", exist_ok=True)
os.makedirs("Results", exist_ok=True)

# Charger le dataset
data_path = "Data/diabetes.csv"  # Remplacez par le chemin réel de votre fichier
diabetes_df = pd.read_csv(data_path)
diabetes_df = diabetes_df.sample(frac=1, random_state=42)  # Shuffle
print("Top 3 lignes du dataset :")
print(diabetes_df.head(3))

# Définir les variables dépendantes et indépendantes
# Supposons que la colonne "Outcome" soit notre cible
X = diabetes_df.drop("Outcome", axis=1).values
y = diabetes_df["Outcome"].values

# Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=125
)

# Identifier les colonnes catégorielles et numériques
# Adaptez selon votre dataset (exemple : toutes les colonnes sauf 'Outcome' sont numériques)
cat_col = []  # Si aucune colonne catégorielle dans ce dataset
num_col = list(range(X.shape[1]))  # Toutes les colonnes sont numériques

# Pipeline de transformation
transform = ColumnTransformer(
    [
        ("num_imputer", SimpleImputer(strategy="median"), num_col),
        ("num_scaler", StandardScaler(), num_col),
    ]
)

# Pipeline complète
pipe = Pipeline(
    steps=[
        ("preprocessing", transform),
        ("model", RandomForestClassifier(n_estimators=100, random_state=125)),
    ]
)

# Entraîner le modèle
pipe.fit(X_train, y_train)

# Évaluation
predictions = pipe.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
f1 = f1_score(y_test, predictions, average="macro")
print("Accuracy:", str(round(accuracy, 2) * 100) + "%", "F1:", round(f1, 2))

# Sauvegarder les métriques
# Sauvegarder les métriques
with open("Results/metrics.txt", "w") as outfile:
    outfile.write(f"Accuracy = {round(accuracy, 2)}, F1 Score = {round(f1, 2)}\n")

# Matrice de confusion
cm = confusion_matrix(y_test, predictions, labels=pipe.classes_)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=pipe.classes_)
disp.plot()
plt.savefig("Results/model_results.png", dpi=120)
plt.close()

# Sauvegarder le modèle
sio.dump(pipe, "Model/diabetes_pipeline.skops")
print("Modèle et résultats sauvegardés avec succès.")