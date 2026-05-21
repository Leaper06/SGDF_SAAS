from database import get_db

def classify_recipe(name):
    name_low = name.lower()
    
    # 1. VÉGÉTARIEN ?
    # Mots-clés de viandes et poissons
    meats = ['poulet', 'viande', 'bœuf', 'porc', 'saucisse', 'jambon', 'poisson', 'crevette', 
             'calamar', 'thon', 'carbonara', 'bolognaise', 'hamburger', 'paella', 'strogonoff', 
             'chili con carne', 'niçoise', 'nems']
    is_vege = not any(meat in name_low for meat in meats)
    
    # 2. SANS FRIGO ?
    # Les viandes et les produits laitiers frais ont besoin du frigo
    is_fridge_free = True
    if not is_vege: 
        is_fridge_free = False # La viande fraîche va au frigo
    dairy_and_fresh = ['crème', 'beurre', 'fromage', 'chèvre', 'bleu', 'mozzarella', 
                       'yaourt', 'lait', 'mayonnaise', 'oeuf', 'œufs', 'tiramisu', 'mousse']
    if any(df in name_low for df in dairy_and_fresh):
        is_fridge_free = False
    if 'tartiflette' in name_low or 'croziflette' in name_low:
        is_fridge_free = False
        
    # 3. FEU DE BOIS ?
    # Pas de feu de bois pour les trucs au four (gratins) ou les plats froids (salades)
    is_wood_fire = True
    cold_or_oven = ['salade', 'sandwich', 'wrap', 'gratin', 'crumble', 'clafoutis', 
                    'moussaka', 'hachis', 'tiramisu', 'fruit', 'melon', 'yaourt']
    if any(co in name_low for co in cold_or_oven):
        is_wood_fire = False
        
    # Exceptions qui marchent très bien au feu
    if 'au feu' in name_low or 'trappeur' in name_low or 'rôties' in name_low or 'poêlée' in name_low:
        is_wood_fire = True

    return is_vege, is_fridge_free, is_wood_fire


def update_all_recipes():
    db = get_db()
    print("🔄 Démarrage de la mise à jour des recettes...")
    
    # 1. On récupère toutes les recettes actuelles
    res = db.table('recipes').select('id, name').execute()
    recipes = res.data
    
    if not recipes:
        print("❌ Aucune recette trouvée dans la base.")
        return

    print(f"📊 {len(recipes)} recettes trouvées. Analyse en cours...")
    
    count = 0
    for recipe in recipes:
        r_id = recipe['id']
        r_name = recipe['name']
        
        # 2. On fait tourner notre algorithme pour trouver les bons attributs
        vege, frigo, bois = classify_recipe(r_name)
        
        # 3. On met à jour la ligne dans Supabase !
        db.table('recipes').update({
            "is_vegetarian": vege,
            "is_fridge_free": frigo,
            "is_wood_fire": bois
        }).eq('id', r_id).execute()
        
        count += 1
        print(f"✅ [{count}/{len(recipes)}] Mise à jour : {r_name} (VéGé:{vege} | SansFrigo:{frigo} | Feu:{bois})")
        
    print("🎉 TERMINÉ ! Toutes les recettes sont harmonisées.")

if __name__ == "__main__":
    update_all_recipes()