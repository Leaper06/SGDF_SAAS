# PolyMaîtrise (V2)

> **Le couteau suisse numérique des maîtrises Scouts et Guides de France.**  
> Libérez du temps d'organisation et de logistique administrative pour maximiser le temps passé sur le terrain avec les jeunes.

---

## Fonctionnalités principales (V2)

### Gestion des Week-ends & Modèles
- **Planning interactif :** Grille d'activités découpée par créneaux (Veillées, Grands Jeux, Vie quotidienne, etc.).
- **Modèles de week-ends :** Sauvegardez vos week-ends types en modèles (Globaux ou Personnalisés par unité) pour créer vos événements en 1 clic.
- **Export PDF :** Génération et impression des plannings de camp au format PDF prêt à emporter en forêt.

### Logistique & Matériel
- **Parc de tentes :** État du stock de tentes en temps réel, affectation aux unités et suivi/signalement des réparations.
- **Inventaire matériel :** Création de listes de matériel par week-end et modèles types (ex: Liste mathos week-end type).

### Intendance & Repas
- **Base de recettes :** Base de recettes adaptées aux camps avec calcul automatique des quantités (Jeunes vs Adultes).
- **Bordereau de courses global :** Fusion automatique de toutes les recettes du week-end en un bordereau de courses unifié.

### Administration & Présences
- **Registre des présences :** Suivi dynamique des présents et absents à chaque activité du week-end.
- **Suivi individuel :** Visualisation de la progression personnelle (Caps, Atouts) et statut des fiches sanitaires.
- **Espace Profil :** Gestion de liens favoris personnalisés par chef.

---

## Stack Technique

- **Frontend :** Vue.js 3 (Vite, TailwindCSS, Pinia, Vue Router)
- **Backend :** Python (Flask, Gunicorn WSGI)
- **Base de données :** Supabase (PostgreSQL)
- **Présentation :** Slidev (dans le dossier `idee/slidev`)
- **Infrastructure :** Docker & Docker Compose, Nginx, Let's Encrypt

---

## Installation en local (Développement)

### Prérequis
- [Docker & Docker Compose](https://docs.docker.com/get-docker/)
- [Git](https://git-scm.com/)

### Étapes d'installation

1. **Cloner le dépôt :**
   ```bash
   git clone https://github.com/Leaper06/SGDF_SAAS.git
   cd SGDF_SAAS
   ```

2. **Configuration des variables d'environnement :**
   Créez un fichier `.env` à la racine du projet à partir du modèle :
   ```bash
   cp .env.example .env
   ```
   Renseignez vos clés d'API Supabase dans le fichier `.env`.

3. **Lancer les conteneurs :**
   ```bash
   docker compose up -d --build
   ```

4. **Accéder à l'application :**
   - **Frontend :** `http://localhost:80` (ou `http://localhost:5173` en dev Vite)
   - **API Backend :** `http://localhost:5000`
   - **Présentation Slidev :** `http://localhost:3030` (via `cd idee/slidev && npm run dev`)

---

## Licence

Ce projet est distribué sous **Licence PolyMaîtrise - Usage Non Commercial & Scoutisme** (voir le fichier [`LICENSE.md`](./LICENSE.md)).  
Il est **gratuit et libre d'accès** pour les unités et maîtrises des **Scouts et Guides de France (SGDF)** et du Scoutisme Français pour un usage non commercial. Toute exploitation commerciale ou revente est interdite sans accord préalable.

---

<div align="center">
  <sub>Développé pour les maîtrises scouts.</sub>
</div>
