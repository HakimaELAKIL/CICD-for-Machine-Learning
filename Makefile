# Installer les dépendances
install:
	@pip install --upgrade pip
	@pip install -r requirements.txt

# Formater le code
format:
	@black *.py

# Entraîner le modèle
train:
	@python train.py

# Évaluer et générer le rapport
eval:
	@echo "## Model Metrics" > report.md
	@type .\Results\metrics.txt >> report.md
	@echo '\n## Confusion Matrix Plot' >> report.md
	@echo '![Confusion Matrix](./Results/model_results.png)' >> report.md
	@cml comment create report.md

# Mettre à jour la branche avec ton nom et email
update-branch:
	@git config --global user.name "$(USER_NAME)"
	@git config --global user.email "$(USER_EMAIL)"
	@git add .
	@git commit -am "Update with new results"
	@git push --force origin HEAD:update

# Se connecter et préparer Hugging Face
hf-login:
	@git pull origin update
	@git switch update
	@pip install -U "huggingface_hub[cli]"
	@huggingface-cli login --token $(HF) --add-to-git-credential

# Pousser App, Model et Results sur HF
push-hub:
	@huggingface-cli upload kingabzpro/Drug-Classification ./App --repo-type=space --commit-message="Sync App files"
	@huggingface-cli upload kingabzpro/Drug-Classification ./Model /Model --repo-type=space --commit-message="Sync Model"
	@huggingface-cli upload kingabzpro/Drug-Classification ./Results /Metrics --repo-type=space --commit-message="Sync Model"

# Déployer : exécute hf-login puis push-hub
deploy: hf-login push-hub

# Run le training (locally)
run:
	@py -3.12 train.py