import math
import logging
from flask import Blueprint, request, jsonify
from database import get_db

intendance_bp = Blueprint('intendance', __name__)

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
def get_slot_meal(slot_id):
    """
    Récupère le repas associé à un créneau de type 'repas'.
    Initialise une nouvelle entité 'meal' silencieusement si elle n'existe pas encore.
    """
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
def add_recipe_to_meal(meal_id):
    """
    Associe une recette existante à un repas planifié.
    """
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
def remove_recipe_from_meal(meal_id, recipe_id):
    """
    Supprime l'association entre une recette et un repas planifié.
    """
    try:
        db = get_db()
        db.table('meal_recipes').delete().eq('meal_id', meal_id).eq('recipe_id', recipe_id).execute()
        return jsonify({"status": "success", "message": "Recette retirée du repas"}), 200

    except Exception as e:
        logging.error(f"Erreur lors de la suppression du plat : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500


@intendance_bp.route('/api/meals/<meal_id>/shopping-list', methods=['GET'])
def get_shopping_list(meal_id):
    """
    Calcule la liste de courses consolidée pour un repas spécifique.
    """
    try:
        db = get_db()
        adults = int(request.args.get('adults', 17))
        children = int(request.args.get('children', 0))

        mr_res = db.table('meal_recipes').select('recipe_id').eq('meal_id', meal_id).execute()
        if not mr_res.data:
            return jsonify({"status": "success", "data": []}), 200

        recipe_ids = [item['recipe_id'] for item in mr_res.data]
        ing_res = db.table('recipe_ingredients').select(
            'qty_adult, qty_child, ingredients(name, unit_type, category)'
        ).in_('recipe_id', recipe_ids).execute()

        shopping_dict = {}

        for item in ing_res.data:
            ing_info = item['ingredients']
            if not ing_info:
                continue
                
            ing_name = ing_info['name']
            unit = ing_info['unit_type']
            category = ing_info.get('category', 'Autre')

            qty_raw = (item.get('qty_adult', 0) * adults) + (item.get('qty_child', 0) * children)
            qty = math.ceil(qty_raw)

            if ing_name in shopping_dict:
                shopping_dict[ing_name]['qty'] = math.ceil(shopping_dict[ing_name]['qty_raw_accumulated'] + qty_raw)
                shopping_dict[ing_name]['qty_raw_accumulated'] += qty_raw
            else:
                shopping_dict[ing_name] = {
                    'name': ing_name,
                    'qty': qty,
                    'qty_raw_accumulated': qty_raw, 
                    'unit': unit,
                    'category': category
                }

        result = [{'name': v['name'], 'qty': v['qty'], 'unit': v['unit'], 'category': v['category']} for v in shopping_dict.values()]
        result.sort(key=lambda x: x['name'])

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        logging.error(f"Erreur lors du calcul des courses (repas) : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500
    

@intendance_bp.route('/api/camps/<camp_id>/shopping-list', methods=['GET'])
def get_camp_shopping_list(camp_id):
    """
    Calcule la liste de courses globale consolidée pour l'ensemble des repas d'un week-end.
    """
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
        if not recipe_ids:
            return jsonify({"status": "success", "data": []}), 200

        ing_res = db.table('recipe_ingredients').select(
            'qty_adult, qty_child, ingredients(name, unit_type, category)'
        ).in_('recipe_id', recipe_ids).execute()

        shopping_dict = {}

        for item in ing_res.data:
            ing_info = item['ingredients']
            if not ing_info: continue
                
            ing_name = ing_info['name']
            unit = ing_info['unit_type']
            category = ing_info.get('category', 'Autre')

            qty_raw = (item.get('qty_adult', 0) * adults) + (item.get('qty_child', 0) * children)
            
            if ing_name in shopping_dict:
                shopping_dict[ing_name]['qty'] = math.ceil(shopping_dict[ing_name]['qty_raw_accumulated'] + qty_raw)
                shopping_dict[ing_name]['qty_raw_accumulated'] += qty_raw
            else:
                shopping_dict[ing_name] = {
                    'name': ing_name,
                    'qty': math.ceil(qty_raw),
                    'qty_raw_accumulated': qty_raw,
                    'unit': unit,
                    'category': category
                }

        result = [{'name': v['name'], 'qty': v['qty'], 'unit': v['unit'], 'category': v['category']} for v in shopping_dict.values()]
        result.sort(key=lambda x: x['name'])

        return jsonify({"status": "success", "data": result}), 200

    except Exception as e:
        logging.error(f"Erreur globale courses (camp) : {e}")
        return jsonify({"status": "error", "message": "Erreur serveur interne"}), 500