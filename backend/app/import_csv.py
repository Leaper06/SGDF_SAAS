import csv
from database import get_db

def import_recipes_from_csv(filepath):
    db = get_db()
    
    print("Démarrage de l'importation...")
    
    # On ouvre le fichier (attention à l'encodage et au délimiteur)
    # Si le script plante sur les colonnes, change delimiter=',' par delimiter=';'
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=',')
        headers = next(reader) # On saute la première ligne (les titres des colonnes)
        
        current_recipe_name = None
        current_recipe_id = None
        
        for row in reader:
            # Sécurité : si la ligne est vide, on passe
            if not row or (not row[0].strip() and not row[3].strip()):
                continue 
            
            recipe_name = row[0].strip()
            qty_str = row[1].strip()
            unit = row[2].strip()
            ingredient_name = row[3].strip()
            category = row[4].strip()
            instructions = row[5].strip() if len(row) > 5 else ""
            
            # --- 1. GESTION DE LA RECETTE ---
            # Si on détecte un nouveau nom dans la 1ère colonne, on crée la recette
            if recipe_name and recipe_name != current_recipe_name:
                current_recipe_name = recipe_name
                print(f"Création de la recette : {recipe_name}")
                
                # On détermine le type avec des mots-clés simples
                dish_type = "Plat chaud"
                if "salade" in recipe_name.lower(): dish_type = "Entrée froide"
                elif "dessert" in recipe_name.lower() or "fruit" in recipe_name.lower(): dish_type = "Dessert"

                recipe_data = {
                    "name": recipe_name,
                    "dish_type": dish_type,
                    "instructions": instructions,
                    "is_vegetarian": "végétarien" in recipe_name.lower() or "légume" in recipe_name.lower(),
                    "is_pork_free": True, # Par défaut
                    "is_eco": False
                }
                
                # Insertion dans Supabase
                res = db.table('recipes').insert(recipe_data).execute()
                current_recipe_id = res.data[0]['id']
            
            # --- 2. GESTION DE L'INGRÉDIENT ---
            if ingredient_name and current_recipe_id:
                # On vérifie si l'ingrédient existe déjà dans la base
                ing_res = db.table('ingredients').select('*').eq('name', ingredient_name).execute()
                
                if not ing_res.data:
                    # S'il n'existe pas, on le crée
                    ing_data = {
                        "name": ingredient_name,
                        "category": category if category else "Autre",
                        "unit_type": unit if unit else "g"
                    }
                    ing_res = db.table('ingredients').insert(ing_data).execute()
                
                ingredient_id = ing_res.data[0]['id']
                
                # --- 3. LIAISON RECETTE <-> INGRÉDIENT ---
                # Conversion de la quantité (Excel met souvent des virgules à la place des points)
                try:
                    qty_float = float(qty_str.replace(',', '.')) if qty_str else 0.0
                except ValueError:
                    qty_float = 0.0
                    
                # On lie l'ingrédient à la recette dans la table de jointure
                rec_ing_data = {
                    "recipe_id": current_recipe_id,
                    "ingredient_id": ingredient_id,
                    "qty_child": qty_float,
                    "qty_adult": qty_float * 1.5 # On estime qu'un adulte mange 1.5x plus qu'un enfant
                }
                db.table('recipe_ingredients').insert(rec_ing_data).execute()

    print("✅ Importation terminée avec succès !")

if __name__ == "__main__":
    import_recipes_from_csv('recettes.csv')