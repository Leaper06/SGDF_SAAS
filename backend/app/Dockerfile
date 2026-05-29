# 1. On part d'une image Python officielle, version légère (slim)
FROM python:3.11-slim

# 2. On définit le dossier de travail à l'intérieur du conteneur
WORKDIR /app

# 3. On copie d'abord SEULEMENT le requirements.txt 
# (C'est une astuce d'optimisation : si ton code change mais pas tes librairies, Docker ira plus vite)
COPY requirements.txt .

# 4. On installe tes dépendances ET on ajoute Gunicorn pour la production
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# 5. On copie tout le reste de ton code 
# (main.py, tes modules de gestion des lieux, des tentes, etc.)
COPY . .

# 6. On indique le port sur lequel l'API va écouter (5000 par défaut)
EXPOSE 5000

# 7. La commande pour lancer le serveur via Gunicorn
# "main:app" signifie : "Dans le fichier main.py, utilise la variable 'app' (qui contient Flask)"
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "main:app"]