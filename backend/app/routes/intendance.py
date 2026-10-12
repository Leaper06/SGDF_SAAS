import math
from collections import Counter
import logging
from flask import Blueprint, request, jsonify, g
from database import get_db
from services.permissions import (
    login_required, forbidden, can_access_camp,
    get_camp_id_of_slot, get_camp_id_of_meal,
)

intendance_bp = Blueprint('intendance', __name__)


def build_shopping_list(recipe_ids, adults, children):
    """
    Additionne les ingrédients d'une liste de recettes pour un effectif donné.
    Une recette présente dans plusieurs repas compte autant de fois qu'elle apparaît.
    Quantités arrondies à l'unité supérieure, liste triée par nom d'ingrédient.
    """
    if not recipe_ids:
        return []
    occurrences = Counter(recipe_ids)
    ing_res = get_db().table('recipe_ingredients').select(
        'recipe_id, qty_adult, qty_child, ingredients(name, unit_type, category)'
    ).in_('recipe_id', list(occurrences)).execute()

    totals = {}
    for item in ing_res.data:
        ing_info = item['ingredients']
        if not ing_info:
            continue
        qty_raw = ((item.get('qty_adult') or 0) * adults + (item.get('qty_child') or 0) * children) \
            * occurrences[item['recipe_id']]
        entry = totals.setdefault(ing_info['name'], {
            'name': ing_info['name'],
            'qty_raw': 0,
            'unit': ing_info['unit_type'],
            'category': ing_info.get('category', 'Autre')
        })
        entry['qty_raw'] += qty_raw

    result = [{'name': e['name'], 'qty': math.ceil(e['qty_raw']), 'unit': e['unit'], 'category': e['category']}
              for e in totals.values()]
    result.sort(key=lambda x: x['name'])
    return result

@intendance_bp.route('/api/recipes', methods=['GET'])
def get_recipes():
    """
    Récupère le catalogue complet des recettes disponibles.
    """
    try:
        db = get_db()
        recipes_res = db.table('recipes').select('*').execute()
        return jsonify({"status": "success", "data": recipes_res.data}), 200
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des recettes : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@intendance_bp.route('/api/recipes', methods=['POST'])
@login_required
def create_recipe():
    """
    Crée une nouvelle recette et l'ensemble de ses ingrédients associés avec leurs grammages.
    """
    try:
        db = get_db()
        data = request.json

        recipe_data = {
            "name": data.get('name'),
            "dish_type": data.get('type'),
            "instructions": "", 
            "is_vegetarian": data.get('is_vegetarian', False),
            "is_fridge_free": data.get('is_fridge_free', False), 
            "is_wood_fire": data.get('is_wood_fire', False)
        }
        
        recipe_res = db.table('recipes').insert(recipe_data).execute()
        new_recipe_id = recipe_res.data[0]['id']

        ingredients_list = data.get('ingredients', [])
        for ing in ingredients_list:
            ing_name = ing.get('name', '').strip()
            if not ing_name:
                continue 
            
            ing_res = db.table('ingredients').select('*').eq('name', ing_name).execute()
            
            if not ing_res.data:
                new_ing = db.table('ingredients').insert({
                    "name": ing_name,
                    "category": "Autre",
                    "unit_type": "g"
                }).execute()
                ingredient_id = new_ing.data[0]['id']
            else:
                ingredient_id = ing_res.data[0]['id']
            
            db.table('recipe_ingredients').insert({
                "recipe_id": new_recipe_id,
                "ingredient_id": ingredient_id,
                "qty_child": float(ing.get('qty_child') or 0),
                "qty_adult": float(ing.get('qty_adult') or 0)
            }).execute()

        return jsonify({"status": "success", "message": "Recette créée avec succès !"}), 201

    except Exception as e:
        logging.error(f"Erreur lors de la création de la recette : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@intendance_bp.route('/api/planning_slots/<slot_id>/meal', methods=['GET'])
@login_required
def get_slot_meal(slot_id):
    """
    Récupère le repas associé à un créneau de type 'repas'.
    Initialise une nouvelle entité 'meal' silencieusement si elle n'existe pas encore.
    """
    if not can_access_camp(g.user, get_camp_id_of_slot(slot_id)):
        return forbidden()
    try:
        db = get_db()
        meal_res = db.table('meals').select('*').eq('planning_slot_id', slot_id).execute()
        
        if not meal_res.data:
            new_meal = db.table('meals').insert({
                "planning_slot_id": slot_id, 
                "additional_guests": 0
            }).execute()
            meal = new_meal.data[0]
        else:
            meal = meal_res.data[0]
            
        meal_id = meal['id']
        jointure_res = db.table('meal_recipes').select('recipe_id, recipes(*)').eq('meal_id', meal_id).execute()
        
        recipes = []
        if jointure_res.data:
            for item in jointure_res.data:
                if item.get('recipes'):
                    recipes.append(item['recipes'])
        
        return jsonify({
            "status": "success",
            "data": {
                "meal": meal,
                "recipes": recipes
            }
        }), 200

    except Exception as e:
        logging.error(f"Erreur lors de la récupération du repas : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@intendance_bp.route('/api/meals/<meal_id>/recipes', methods=['POST'])
@login_required
def add_recipe_to_meal(meal_id):
    """
    Associe une recette existante à un repas planifié.
    """
    if not can_access_camp(g.user, get_camp_id_of_meal(meal_id)):
        return forbidden()
    try:
        db = get_db()
        data = request.json
        recipe_id = data.get('recipe_id')

        if not recipe_id:
            return jsonify({"status": "error", "message": "ID de recette manquant"}), 400

        db.table('meal_recipes').insert({
            "meal_id": meal_id,
            "recipe_id": recipe_id
        }).execute()

        return jsonify({"status": "success", "message": "Recette ajoutée au repas"}), 201

    except Exception as e:
        logging.error(f"Erreur lors de l'ajout du plat : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@intendance_bp.route('/api/meals/<meal_id>/recipes/<recipe_id>', methods=['DELETE'])
@login_required
def remove_recipe_from_meal(meal_id, recipe_id):
    """
    Supprime l'association entre une recette et un repas planifié.
    """
    if not can_access_camp(g.user, get_camp_id_of_meal(meal_id)):
        return forbidden()
    try:
        db = get_db()
        db.table('meal_recipes').delete().eq('meal_id', meal_id).eq('recipe_id', recipe_id).execute()
        return jsonify({"status": "success", "message": "Recette retirée du repas"}), 200

    except Exception as e:
        logging.error(f"Erreur lors de la suppression du plat : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@intendance_bp.route('/api/meals/<meal_id>/shopping-list', methods=['GET'])
@login_required
def get_shopping_list(meal_id):
    """
    Calcule la liste de courses consolidée pour un repas spécifique.
    """
    if not can_access_camp(g.user, get_camp_id_of_meal(meal_id)):
        return forbidden()
    try:
        db = get_db()
        adults = int(request.args.get('adults', 17))
        children = int(request.args.get('children', 0))

        mr_res = db.table('meal_recipes').select('recipe_id').eq('meal_id', meal_id).execute()
        recipe_ids = [item['recipe_id'] for item in mr_res.data]
        result = build_shopping_list(recipe_ids, adults, children)

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        logging.error(f"Erreur lors du calcul des courses (repas) : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500
    

@intendance_bp.route('/api/camps/<camp_id>/shopping-list', methods=['GET'])
@login_required
def get_camp_shopping_list(camp_id):
    """
    Calcule la liste de courses globale consolidée pour l'ensemble des repas d'un week-end.
    """
    if not can_access_camp(g.user, camp_id):
        return forbidden()
    try:
        db = get_db()
        adults = int(request.args.get('adults', 0))
        children = int(request.args.get('children', 0))

        slots_res = db.table('planning_slots').select('id').eq('camp_id', camp_id).eq('slot_type', 'repas').execute()
        slot_ids = [s['id'] for s in slots_res.data]
        if not slot_ids:
            return jsonify({"status": "success", "data": []}), 200

        meals_res = db.table('meals').select('id').in_('planning_slot_id', slot_ids).execute()
        meal_ids = [m['id'] for m in meals_res.data]
        if not meal_ids:
            return jsonify({"status": "success", "data": []}), 200

        mr_res = db.table('meal_recipes').select('recipe_id').in_('meal_id', meal_ids).execute()
        recipe_ids = [item['recipe_id'] for item in mr_res.data]
        result = build_shopping_list(recipe_ids, adults, children)

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        logging.error(f"Erreur globale courses (camp) : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500