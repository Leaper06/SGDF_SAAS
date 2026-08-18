# pyrefly: ignore [missing-import]
from flask import Blueprint, jsonify, request, send_file, render_template
import io
import logging
from datetime import datetime
from database import get_db

campPDF_bp = Blueprint('campPDF', __name__)

def parse_iso_dt(dt_str):
    if not dt_str:
        return datetime.now()
    try:
        return datetime.fromisoformat(str(dt_str).replace('Z', '+00:00'))
    except Exception:
        return datetime.now()

@campPDF_bp.route('/api/camps/<camp_id>/export-dossier', methods=['GET'])
def export_dossier_pdf(camp_id):
    try:
        db = get_db()
        
        # 1. Récupération du camp
        camp_res = db.table('camps').select('*').eq('id', camp_id).execute()
        if not camp_res.data:
            return jsonify({"status": "error", "message": "Camp introuvable"}), 404
        camp = camp_res.data[0]
        
        # 2. Récupération du lieu
        lieu = None
        if camp.get('location'):
            lieu_res = db.table('camp_locations').select('*').eq('name', camp['location']).execute()
            if lieu_res.data:
                lieu = lieu_res.data[0]
            else:
                lieu = {'name': camp['location'], 'address': '', 'description': ''}

        # 3. Récupération des présences et des membres
        presents_res = db.table('camp_attendance').select('adherent_id').eq('camp_id', camp_id).execute()
        
        jeunes_presents = []
        chefs_presents = []
        
        present_ids = [str(p['adherent_id']).strip() for p in presents_res.data if p.get('adherent_id')] if presents_res.data else []
        
        if not present_ids:
            unit_id = camp.get('unit_id')
            if unit_id:
                u_res = db.table('unit_members').select('*').eq('unit_id', unit_id).execute()
                if u_res.data:
                    for m in u_res.data:
                        user_obj = {
                            'first_name': m.get('first_name', ''),
                            'last_name': m.get('last_name', ''),
                            'adherent_id': str(m.get('adherent_id', ''))
                        }
                        if m.get('is_jeune'):
                            jeunes_presents.append(user_obj)
                        else:
                            chefs_presents.append(user_obj)
            
            # Chefs invités pour ce camp
            guests_res = db.table('camp_guests').select('adherent_id').eq('camp_id', camp_id).execute()
            if guests_res.data:
                g_ids = [str(g['adherent_id']).strip() for g in guests_res.data if g.get('adherent_id')]
                existing_ids = {u['adherent_id'] for u in (jeunes_presents + chefs_presents)}
                missing_g_ids = [gid for gid in g_ids if gid not in existing_ids]
                
                if missing_g_ids:
                    g_members = db.table('unit_members').select('*').in_('adherent_id', missing_g_ids).execute()
                    found_g = g_members.data if g_members.data else []
                    for m in found_g:
                        chefs_presents.append({
                            'first_name': m.get('first_name', ''),
                            'last_name': m.get('last_name', ''),
                            'adherent_id': str(m.get('adherent_id', ''))
                        })
                    
                    found_g_ids = {str(m['adherent_id']).strip() for m in found_g}
                    still_missing = [gid for gid in missing_g_ids if gid not in found_g_ids]
                    for missing_id in still_missing:
                        mapping = db.table('chef_mappings').select('*').eq('adherent_id', missing_id).execute()
                        unit_label = f" ({mapping.data[0]['unit_name']})" if mapping.data and mapping.data[0].get('unit_name') else ""
                        chefs_presents.append({
                            'first_name': 'Chef',
                            'last_name': f'Invité{unit_label}',
                            'adherent_id': missing_id
                        })
        else:
            members_res = db.table('unit_members').select('*').in_('adherent_id', present_ids).execute()
            found_members = members_res.data if members_res.data else []
            found_ids = {str(m['adherent_id']).strip() for m in found_members}
            missing_ids = [pid for pid in present_ids if pid not in found_ids]
            
            for m in found_members:
                user_obj = {
                    'first_name': m.get('first_name', ''),
                    'last_name': m.get('last_name', ''),
                    'adherent_id': str(m.get('adherent_id', ''))
                }
                if m.get('is_jeune'):
                    jeunes_presents.append(user_obj)
                else:
                    chefs_presents.append(user_obj)
                    
            for missing_id in missing_ids:
                mapping = db.table('chef_mappings').select('*').eq('adherent_id', missing_id).execute()
                unit_label = f" ({mapping.data[0]['unit_name']})" if mapping.data and mapping.data[0].get('unit_name') else ""
                chefs_presents.append({
                    'first_name': 'Chef',
                    'last_name': f'Invité{unit_label}',
                    'adherent_id': missing_id
                })
                    
        total_presents = len(jeunes_presents) + len(chefs_presents)

        chefs_dict = {str(c['adherent_id']): f"{c['first_name']} {c['last_name']}".strip() for c in chefs_presents}

        # 4. Récupération des tentes
        tentes = []
        try:
            tentes_res = db.table('camp_tents').select('tents(*)').eq('camp_id', camp_id).execute()
            if tentes_res.data:
                tentes = [t.get('tents') for t in tentes_res.data if t.get('tents')]
        except Exception as e:
            logging.error(f"Erreur récuperation tentes : {e}")

        # 5. Récupération globale du planning
        slots_res = db.table('planning_slots').select('*').eq('camp_id', camp_id).order('start_time').execute()
        slots = slots_res.data or []
        
        # --- REQUÊTES REGROUPÉES (BULK) POUR ÉVITER LE PROBLÈME N+1 ---
        activity_ids = [s['activity_id'] for s in slots if s.get('activity_id')]
        repas_slot_ids = [s['id'] for s in slots if s.get('slot_type') == 'repas']

        activities_map = {}
        responsibles_map = {}
        meals_map = {}

        if activity_ids:
            act_res = db.table('activities').select('*, activity_steps(*), activity_materials(*)').in_('id', activity_ids).execute()
            if act_res.data:
                for a in act_res.data:
                    activities_map[a['id']] = a

            resp_res = db.table('activity_responsibles').select('activity_id, adherent_id').in_('activity_id', activity_ids).execute()
            if resp_res.data:
                for r in resp_res.data:
                    act_id = r['activity_id']
                    aid = str(r.get('adherent_id')).strip()
                    if act_id not in responsibles_map:
                        responsibles_map[act_id] = []
                    responsibles_map[act_id].append(aid)

        if repas_slot_ids:
            m_res = db.table('meals').select('*, meal_recipes(*, recipes(*, recipe_ingredients(*, ingredients(*))))').in_('planning_slot_id', repas_slot_ids).execute()
            if m_res.data:
                for m in m_res.data:
                    meals_map[m['planning_slot_id']] = m
        # -------------------------------------------------------------

        planning_global = []
        fiches_activites = []
        menus_detailles = []

        for slot in slots:
            start_dt = parse_iso_dt(slot.get('start_time'))
            end_dt = parse_iso_dt(slot.get('end_time'))

            responsables_noms = []
            act_id = slot.get('activity_id')
            if act_id and act_id in responsibles_map:
                for aid in responsibles_map[act_id]:
                    if aid in chefs_dict:
                        responsables_noms.append(chefs_dict[aid])
                    else:
                        responsables_noms.append(f"Chef ({aid})")

            planning_global.append({
                'jour': start_dt.strftime('%A').capitalize(),
                'heure_debut': start_dt.strftime('%H:%M'),
                'heure_fin': end_dt.strftime('%H:%M'),
                'titre': slot.get('title', ''),
                'type': slot.get('slot_type', ''),
                'responsables': responsables_noms
            })

            # 5a. Extraction des fiches d'activités (depuis le cache memory activities_map)
            if act_id and act_id in activities_map:
                activity = activities_map[act_id]
                etapes = activity.get('activity_steps', []) or []
                etapes.sort(key=lambda x: x.get('order_index', 0))
                
                materiel = [m.get('item_name') for m in (activity.get('activity_materials', []) or []) if m.get('item_name')]
                
                fiches_activites.append({
                    'titre': slot.get('title', ''),
                    'horaire': f"{start_dt.strftime('%A %H:%M')} - {end_dt.strftime('%H:%M')}",
                    'imaginaire': activity.get('imaginary_and_objectives', ''),
                    'materiel': materiel,
                    'etapes': etapes
                })

            # 5b. Extraction des repas (depuis le cache memory meals_map)
            if slot.get('slot_type') == 'repas' and slot['id'] in meals_map:
                meal = meals_map[slot['id']]
                repas_data = {
                    'titre': slot.get('title', ''),
                    'horaire': f"{start_dt.strftime('%A')} {start_dt.strftime('%H:%M')}",
                    'recettes': []
                }
                
                for mr in (meal.get('meal_recipes', []) or []):
                    recipe = mr.get('recipes')
                    if recipe:
                        recette_data = {
                            'nom': recipe.get('name', ''),
                            'ingredients': []
                        }
                        for ri in (recipe.get('recipe_ingredients', []) or []):
                            ingredient = ri.get('ingredients')
                            if ingredient:
                                nb_jeunes = len(jeunes_presents)
                                nb_adultes = len(chefs_presents) + meal.get('additional_guests', 0)
                                
                                qty_calculee = (nb_jeunes * float(ri.get('qty_child') or 0)) + (nb_adultes * float(ri.get('qty_adult') or 0))
                                
                                recette_data['ingredients'].append({
                                    'nom': ingredient.get('name', ''),
                                    'quantite': round(qty_calculee, 2),
                                    'unite': ingredient.get('unit_type', '')
                                })
                        
                        repas_data['recettes'].append(recette_data)
                
                menus_detailles.append(repas_data)

        # 6. Génération du PDF
        data_for_template = {
            'camp': camp,
            'lieu': lieu,
            'effectifs': {
                'total': total_presents,
                'jeunes': jeunes_presents,
                'chefs': chefs_presents
            },
            'tentes': tentes,
            'planning': planning_global,
            'activites': fiches_activites,
            'menus': menus_detailles
        }

        rendered_html = render_template('export_weekend.html', **data_for_template)
        try:
            from weasyprint import HTML
            pdf_file = HTML(string=rendered_html).write_pdf()
        except ImportError:
            return jsonify({'status': 'error', 'message': 'WeasyPrint non disponible'}), 500

        nom_camp = camp.get('name', 'Sans_Nom').replace(' ', '_')
        return send_file(
            io.BytesIO(pdf_file),
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"Dossier_{nom_camp}.pdf"
        )

    except Exception as e:
        logging.error(f"Erreur export PDF: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500