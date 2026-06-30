# PolyMaîtrise (SGDF SaaS)

PolyMaîtrise est un outil compagnon conçu pour faciliter l'organisation, la gestion logistique et le suivi pédagogique des activités et des camps scouts. 

## Fonctionnalités principales

- **Gestion des adhérents :** Suivi des jeunes, contacts d'urgence et informations médicales basiques.
- **Logistique & Matériel :** Suivi de l'état des tentes, répartition du matériel d'animation et de la flotte.
- **Intendance :** Gestion des menus, des courses et des fiches d'intentions.
- **Planning :** Organisation des grilles d'activités pour les week-ends et les camps d'été.

## Stack Technique

L'architecture est séparée entre un frontend réactif et une API backend légère, le tout conteneurisé pour un déploiement fluide.

*   **Frontend :** Vue.js (Vite)
*   **Backend :** Python (Flask) / Serveur WSGI Gunicorn
*   **Base de données :** Supabase (PostgreSQL)
*   **Infrastructure & Déploiement :** Docker & Docker Compose
*   **Proxy & Sécurité :** Nginx, Let's Encrypt (Certbot)

## Installation en local (Développement)

### Prérequis
- [Docker](https://docs.docker.com/get-docker/) et Docker Compose installés sur votre machine.
- [Git](https://git-scm.com/)

### Étapes d'installation

1. **Cloner le dépôt :**
```bash
git clone https://github.com/Leaper06/SGDF_SAAS.git
cd SGDF_SAAS
```
2. Configuration des variables d'environnement :
Créez un fichier .env à la racine du projet en vous basant sur le modèle fourni :
```bash
cp .env.example .env
```
Renseignez ensuite vos clés d'API Supabase dans ce nouveau fichier .env.
3. Lancer les conteneurs :
```bash
docker compose up -d --build
```
4. Accéder à l'application :
   * Frontend : http://localhost:80
   * API Backend : http://localhost:5000
# Déploiement en production
Le projet est configuré pour être déployé sur un VPS via Docker.
Le routage et la terminaison SSL sont gérés par un conteneur Nginx avec Let's Encrypt.
1. Récupérer le code sur le serveur.
2. Configurer le fichier .env avec les identifiants de production.
3. Générer le certificat SSL initial via Certbot en mode standalone (voir la documentation interne).
4. Lancer le service : docker compose up -d --build

# Sécurité et RGPD
Ce projet manipule des données concernant des mineurs.
Les variables d'environnement (.env) et les fichiers de cache (__pycache__, node_modules) sont strictement ignorés par Git.
Les mots de passe et accès base de données ne doivent jamais être commités.
Les données en production sont protégées par un chiffrement SSL/TLS (HTTPS).

## Développé pour les maîtrises.
