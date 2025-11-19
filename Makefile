# ==============================
# Makefile pour déploiement HF
# ==============================

# Variables
PYTHON = py -3.12
HF_REPO = Hakima2004/diabete_prediction
HF_TOKEN = $(HF)  # Assurez-vous que la variable d'environnement HF est définie

# Installer les dépendances
install:
	@$(PYTHON) -m pip install --upgrade pip &&\
	@$(PYTHON) -m pip install -r requirements.txt

# Formater le code Python
format:
	@$(PYTHON) -m black *.py

# Entraîner le modèle
train:
	@$(PYTHON) train.py

# Générer un rapport d'évaluation
eval:
	@echo "## Model Metrics" > report.md
	@cat ./Results/metrics.txt >> report.md
	@echo '\n## Confusion Matrix Plot' >> report.md
	@echo '![Confusion Matrix](./Results/model_results.png)' >> report.md
	@cml comment create report.md

# Se connecter à Hugging Face
hf-login:
	@echo "Connexion à Hugging Face..."
	@hf auth login --token $(HF_TOKEN)

# Pousser les fichiers sur Hugging Face
push-hub:
	@echo "Uploading App..."
	@hf upload $(HF_REPO) ./App App --repo-type=space
	@echo "Uploading Model..."
	@hf upload $(HF_REPO) ./Model Model --repo-type=space
	@echo "Uploading Results..."
	@hf upload $(HF_REPO) ./Results Results --repo-type=space

# Déploiement complet
deploy: hf-login push-hub
	@echo "Déploiement terminé !"

# Mettre à jour la branche git locale
update-branch:
	@git config --global user.name "$(USER_NAME)"
	@git config --global user.email "$(USER_EMAIL)"
	@git add .
	@git commit -am "Update with new results"
	@git push --force origin HEAD:update