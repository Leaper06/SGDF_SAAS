# Étape 1 : Le Chantier (Compilation)
FROM node:20-alpine AS builder

WORKDIR /app

# On copie les fichiers de dépendances et on installe
COPY package*.json ./
RUN npm install

# On copie tout le reste du code et on lance la compilation Vite
COPY . .
RUN npm run build

# Étape 2 : La Vitrine (Serveur Web Nginx)
FROM nginx:alpine

# On glisse notre petite configuration Nginx pour le routeur
COPY nginx.conf /etc/nginx/conf.d/default.conf

# On récupère le dossier "dist" généré par Vite à l'étape 1
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]