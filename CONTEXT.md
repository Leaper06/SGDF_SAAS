1. Standards de Code et Style
Tu interviens sur le projet SGDF_SAAS. Tes réponses et ton code doivent strictement respecter les règles suivantes :

Lisibilité avant tout : Produis un code clair, structuré et de niveau universitaire. Évite les abstractions inutiles, le code trop bas niveau ou les architectures excessivement complexes. Le code doit être facilement compréhensible et maintenable.

Frontend : Utilise Vue.js 3 avec la Composition API (<script setup>). Les composants doivent être modulaires. Le style est géré avec Tailwind CSS.

Backend : Le code Python doit être idiomatique, typé lorsque c'est pertinent, et modulaire (utilisation des Blueprints Flask).

Sécurité : Ne jamais exposer de données sensibles. Les routes d'API doivent être protégées et vérifier systématiquement les autorisations associées au token fourni.

2. Stack Technique
Frontend : Vue.js 3 (Vite), Tailwind CSS.

Backend : Python 3.12, Framework Flask.

Base de données : PostgreSQL. Les requêtes sont effectuées via le client Supabase (ex: db.table('...').select()).

Authentification : Génération de tokens de session internes (UUID) renvoyés en format Bearer token au frontend. L'authentification initiale vérifie la validité de l'utilisateur en récupérant les cookies de l'intranet SGDF (Scouts et Guides de France) via du web scraping.

3. Lexique Métier (Domain Driven Design)
Le projet est un SaaS de gestion pour les groupes locaux des Scouts et Guides de France. Voici les concepts clés à maîtriser :

SGDF : Scouts et Guides de France (l'association).

Adhérent / Member : Toute personne enregistrée. Peut être un "Jeune" (participant) ou un "Chef/Cheftaine" (encadrant/gestionnaire).

Unité (Unit) : Groupe d'adhérents (ex: Mousses, Louveteaux-Jeannettes, Pionniers-Caravelles). Chaque unité a un identifiant unique (unit_id). Les chefs gèrent une unité spécifique.

Camp / Week-end : Événement organisé par une unité à des dates précises, dans un lieu donné.

Planning & Activités : Le déroulé d'un camp. Le planning est divisé en créneaux (planning_slots) qui contiennent des activités. Ces activités ont des étapes (activity_steps), du matériel nécessaire (activity_materials) et des responsables (activity_responsibles).

Intendance / Repas : Gestion de la nourriture. Les repas (meals) sont liés au planning et composés de recettes (recipes) qui utilisent des ingrédients (ingredients). Cela génère des listes de courses (shopping_lists).

Logistique / Tentes : Gestion du matériel de campement. Les tentes (tents) ont une capacité et un statut (ex: opérationnelle, à réparer via tent_incidents) et sont assignées aux camps (camp_tents).

Registre de présence (Attendance/Roster) : Permet de lier les adhérents d'une unité à un camp spécifique.

4. Schéma de Base de Données
Pour comprendre la structure de la base de données et rédiger les requêtes Supabase, réfère-toi toujours à l'architecture ci-dessous.

Relations principales :

L'entité centrale est units. Les users, camps et unit_members lui sont rattachés via unit_id.

Un camps possède des planning_slots, des camp_guests, des camp_tents et un camp_attendance.

Les activities sont rattachées aux planning_slots et se décomposent en activity_steps, activity_materials et activity_responsibles.

L'intendance relie les meals (liés aux plannings) aux recipes, qui elles-mêmes nécessitent des ingredients.

Définition DDL de référence :

CREATE TABLE public.units ( id uuid PRIMARY KEY, name text NOT NULL, branch text, created_at timestamp );
CREATE TABLE public.users ( id uuid PRIMARY KEY, unit_id uuid REFERENCES public.units(id), first_name text, last_name text, role text );
CREATE TABLE public.camps ( id uuid PRIMARY KEY, unit_id uuid REFERENCES public.units(id), name text, location text, start_date timestamp, end_date timestamp, unit_name text );
CREATE TABLE public.activities ( id uuid PRIMARY KEY, title text, duration_minutes integer, imaginary_and_objectives text );
CREATE TABLE public.planning_slots ( id uuid PRIMARY KEY, camp_id uuid REFERENCES public.camps(id), activity_id uuid REFERENCES public.activities(id), start_time timestamp, end_time timestamp, title text, slot_type text );
CREATE TABLE public.activity_steps ( id uuid PRIMARY KEY, activity_id uuid REFERENCES public.activities(id), start_time text, duration_minutes integer, title text, description text, order_index integer );
CREATE TABLE public.activity_materials ( id uuid PRIMARY KEY, activity_id uuid REFERENCES public.activities(id), item_name text, is_checked boolean );
CREATE TABLE public.activity_responsibles ( id uuid PRIMARY KEY, activity_id uuid REFERENCES public.activities(id), adherent_id text );
CREATE TABLE public.ingredients ( id uuid PRIMARY KEY, name text, category text, unit_type text );
CREATE TABLE public.recipes ( id uuid PRIMARY KEY, name text, dish_type text, instructions text, is_vegetarian boolean, is_fridge_free boolean, is_wood_fire boolean );
CREATE TABLE public.recipe_ingredients ( id uuid PRIMARY KEY, recipe_id uuid REFERENCES public.recipes(id), ingredient_id uuid REFERENCES public.ingredients(id), qty_child numeric, qty_adult numeric );
CREATE TABLE public.meals ( id uuid PRIMARY KEY, planning_slot_id uuid REFERENCES public.planning_slots(id), additional_guests integer );
CREATE TABLE public.meal_recipes ( id uuid PRIMARY KEY, meal_id uuid REFERENCES public.meals(id), recipe_id uuid REFERENCES public.recipes(id) );
CREATE TABLE public.shopping_lists ( id uuid PRIMARY KEY, camp_id uuid REFERENCES public.camps(id), ingredient_id uuid REFERENCES public.ingredients(id), total_quantity numeric, is_checked boolean );
CREATE TABLE public.adherent_extras ( id bigint PRIMARY KEY, adherent_id character varying, photo_url text, fiche_url text, progression_symbole text, progression_action text );
CREATE TABLE public.chef_mappings ( email text PRIMARY KEY, adherent_id text, unit_name text );
CREATE TABLE public.camp_guests ( id bigint PRIMARY KEY, adherent_id text, camp_id uuid REFERENCES public.camps(id) );
CREATE TABLE public.tents ( id integer PRIMARY KEY, name text, capacity integer, status text, group_name text );
CREATE TABLE public.camp_tents ( id integer PRIMARY KEY, camp_id uuid REFERENCES public.camps(id), tent_id integer REFERENCES public.tents(id) );
CREATE TABLE public.tent_incidents ( id integer PRIMARY KEY, tent_id integer REFERENCES public.tents(id), camp_id uuid, description text, status text, created_at timestamp );
CREATE TABLE public.camp_attendance ( id integer PRIMARY KEY, camp_id uuid REFERENCES public.camps(id), adherent_id text );
CREATE TABLE public.camp_locations ( id uuid PRIMARY KEY, name text, address text, contact_info text, description text, is_shared boolean, group_name text, latitude numeric, longitude numeric );
CREATE TABLE public.favorite_links ( id uuid PRIMARY KEY, adherent_id text, name text, url text );
CREATE TABLE public.unit_members ( adherent_id text PRIMARY KEY, unit_id uuid REFERENCES public.units(id), first_name text, last_name text, is_jeune boolean, is_chef boolean, last_synced_at timestamp );


je ne veut aucun émojie mais des svg