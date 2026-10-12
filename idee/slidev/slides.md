---
theme: default
background: /cover.jpg
class: text-center
highlighter: shiki
lineNumbers: false
info: |
  PolyMaîtrise : présentation et guide de prise en main pour les maîtrises SGDF
drawings:
  persist: false
transition: slide-left
title: PolyMaîtrise
exportFilename: slides-export
---

# PolyMaîtrise

<div class="text-3xl text-white font-black mt-4 tracking-wide drop-shadow-lg">Le couteau suisse numérique des maîtrises</div>

<div class="mt-10 text-lg text-gray-900 font-bold bg-white/95 px-6 py-4 rounded-xl shadow-xl inline-block">
  Présentation & guide de prise en main
</div>

<div class="abs-b mb-8 text-sm text-white font-bold drop-shadow">polymaitrise.fr</div>

---

# La réalité de l'organisation d'unité

<div class="subtitle">Gérer une unité demande une charge administrative invisible mais lourde.</div>

<div class="grid grid-cols-2 gap-5 mt-6">
  <div class="card" style="border-top-color: var(--pm-orange)">
    <h3 style="color: var(--pm-orange)">Des outils éparpillés</h3>
    <p>WhatsApp, tableurs, papiers volants, Drive partagé… l'information est partout et nulle part.</p>
  </div>
  <div class="card" style="border-top-color: var(--pm-orange)">
    <h3 style="color: var(--pm-orange)">La chasse aux fiches sanitaires</h3>
    <p>Savoir qui a rendu sa fiche, et la retrouver vite le jour J.</p>
  </div>
  <div class="card" style="border-top-color: var(--pm-orange)">
    <h3 style="color: var(--pm-orange)">L'intendance à la main</h3>
    <p>Grammages calculés à la calculette, listes de courses oubliées ou incomplètes.</p>
  </div>
  <div class="card" style="border-top-color: var(--pm-orange)">
    <h3 style="color: var(--pm-orange)">Des passations difficiles</h3>
    <p>Plannings, recettes et bons lieux de camp perdus d'une année sur l'autre.</p>
  </div>
</div>

<div class="tip warn mt-6"><b>Conséquence :</b> moins de temps et d'énergie pour ce qui compte vraiment, l'animation et la pédagogie.</div>

---

# PolyMaîtrise en un coup d'œil

<div class="subtitle">Une application web gratuite, pensée pour le quotidien des maîtrises, connectée à l'intranet SGDF.</div>

<div class="grid grid-cols-4 gap-4 mt-6">
  <div class="card">
    <h3 style="color: var(--pm-blue)">Unité</h3>
    <ul>
      <li>Membres importés de l'intranet</li>
      <li>Fiches sanitaires</li>
      <li>Équipages & progression</li>
    </ul>
  </div>
  <div class="card" style="border-top-color: var(--pm-orange)">
    <h3 style="color: var(--pm-orange)">Camps</h3>
    <ul>
      <li>Calendrier & modèles</li>
      <li>Planning par créneaux</li>
      <li>Fiches d'activité</li>
      <li>Dossier de camp PDF</li>
    </ul>
  </div>
  <div class="card" style="border-top-color: var(--pm-violet)">
    <h3 style="color: var(--pm-violet)">Intendance</h3>
    <ul>
      <li>~180 recettes de camp</li>
      <li>Portions jeunes / adultes</li>
      <li>Liste de courses par rayon</li>
    </ul>
  </div>
  <div class="card" style="border-top-color: var(--pm-green)">
    <h3 style="color: var(--pm-green)">Logistique</h3>
    <ul>
      <li>Parc de tentes du groupe</li>
      <li>Incidents de matériel</li>
      <li>Carnet de lieux de camp</li>
    </ul>
  </div>
</div>

<div class="grid grid-cols-3 gap-4 mt-6 text-center text-sm font-bold" style="color: var(--pm-blue)">
  <div class="bg-white rounded-xl py-3 shadow">Sur téléphone et ordinateur</div>
  <div class="bg-white rounded-xl py-3 shadow">Consultable avec un réseau faible</div>
  <div class="bg-white rounded-xl py-3 shadow">Testable sans compte (mode Démo)</div>
</div>

---

# Le guide de prise en main

<div class="subtitle">Ce document sert aussi de tutoriel : suivez les étapes dans l'ordre lors de votre première utilisation.</div>

<div class="grid grid-cols-2 gap-x-10 gap-y-3 mt-6 text-sm">
  <div><b style="color: var(--pm-orange)">1. Démarrer</b> — se connecter, s'identifier, installer l'appli</div>
  <div><b style="color: var(--pm-orange)">2. Unité</b> — membres, fiches sanitaires, équipages</div>
  <div><b style="color: var(--pm-orange)">3. Camps</b> — créer un week-end, planning, fiches d'activité</div>
  <div><b style="color: var(--pm-orange)">4. Intendance</b> — menus et liste de courses</div>
  <div><b style="color: var(--pm-orange)">5. Effectifs & matériel</b> — présences, tentes, dossier PDF</div>
  <div><b style="color: var(--pm-orange)">6. Logistique & profil</b> — tentes du groupe, lieux, réglages</div>
  <div><b style="color: var(--pm-orange)">7. Sur le terrain</b> — réseau faible et messages d'alerte</div>
  <div><b style="color: var(--pm-orange)">8. Questions fréquentes</b> — et que faire si…</div>
</div>

<div class="tip mt-8"><b>Pour découvrir sans risque :</b> le bouton <span class="btn">Essayer la version Démo</span> de la page de connexion ouvre l'application avec une unité fictive. Toutes les captures de ce guide viennent de ce mode Démo.</div>

---
layout: center
class: section-slide text-center !bg-[#004267]
---

<div class="section-number">Partie 1</div>

# Démarrer

<p>Connexion, première identification et installation sur le téléphone</p>

---

<span class="module-tag">Démarrer</span>

# Se connecter

<div class="grid grid-cols-[1fr_auto] gap-10 mt-4">
<div>

<div class="steps">
  <div class="step">Ouvrez <b>polymaitrise.fr</b> sur votre téléphone ou votre ordinateur.</div>
  <div class="step">Saisissez <b>vos identifiants de l'intranet SGDF</b> : le même identifiant (ou e-mail) et le même mot de passe que sur intranet.sgdf.fr.</div>
  <div class="step">Appuyez sur <span class="btn">Se connecter</span>. La première connexion peut prendre <b>jusqu'à une minute</b> : l'application récupère votre unité et ses membres sur l'intranet.</div>
</div>

<div class="tip">Votre mot de passe sert uniquement à ouvrir votre session sur l'intranet. <b>Il n'est jamais enregistré</b> par PolyMaîtrise.</div>

<div class="tip warn">Vous restez connecté 30 jours. Après une longue absence, l'application vous demandera simplement de vous reconnecter.</div>

</div>
<Phone src="/screens/login.png" alt="Page de connexion" />
</div>

---

<span class="module-tag">Démarrer</span>

# Première connexion : dites qui vous êtes

<div class="grid grid-cols-[1fr_auto] gap-10 mt-4">
<div>

<div class="steps">
  <div class="step">À la première connexion, un bandeau orange <b>« Bienvenue à toi ! »</b> apparaît en haut de l'onglet <b>Unité</b>.</div>
  <div class="step">Dans la liste des chefs, appuyez sur <span class="btn">C'est moi !</span> à côté de votre nom.</div>
  <div class="step">C'est fait : l'application sait qui vous êtes (liens personnels, camps où vous êtes invité, branche).</div>
</div>

<div class="tip"><b>Votre unité a changé sur l'intranet</b> (nouveaux jeunes, départs) ? Appuyez sur <span class="btn">Resynchroniser</span> en haut de la liste des membres. Si l'application vous redemande votre mot de passe intranet, c'est normal : la session intranet dure moins longtemps que celle de PolyMaîtrise.</div>

</div>
<Phone src="/screens/unite.png" alt="Onglet Unité" />
</div>

---

<span class="module-tag">Démarrer</span>

# Installer l'application sur le téléphone

<div class="grid grid-cols-[1fr_auto] gap-10 mt-4">
<div>

<div class="subtitle">Pas besoin de store : PolyMaîtrise s'installe depuis le navigateur et s'ouvre ensuite comme une vraie application.</div>

<div class="grid grid-cols-2 gap-4">
<div>
  <div class="font-black text-sm mb-2" style="color: var(--pm-green)">Android (Chrome)</div>
  <div class="steps">
    <div class="step">Ouvrez le menu <b>⋮</b> en haut à droite.</div>
    <div class="step">Choisissez <b>« Installer l'application »</b> ou <b>« Ajouter à l'écran d'accueil »</b>.</div>
  </div>
</div>
<div>
  <div class="font-black text-sm mb-2" style="color: var(--pm-blue)">iPhone (Safari)</div>
  <div class="steps">
    <div class="step">Touchez l'icône <b>Partager</b> en bas de l'écran.</div>
    <div class="step">Choisissez <b>« Sur l'écran d'accueil »</b>, puis <b>Ajouter</b>.</div>
  </div>
</div>
</div>

<div class="tip">Ces instructions sont aussi dans l'application : <b>Profil</b> → <span class="btn">Installer l'application sur le téléphone</span>.</div>

</div>
<Phone src="/screens/installer.png" alt="Fenêtre d'installation" />
</div>

---
layout: center
class: section-slide text-center !bg-[#004267]
---

<div class="section-number">Partie 2</div>

# Unité

<p>Membres, fiches sanitaires et équipages</p>

---

<span class="module-tag">Unité</span>

# Les membres et leurs fiches sanitaires

<div class="grid grid-cols-[1fr_auto_auto] gap-6 mt-2">
<div>

<div class="steps">
  <div class="step">L'onglet <b>Unité</b> liste les jeunes et la maîtrise. Le badge indique si la fiche sanitaire est <b style="color: var(--pm-green)">rendue</b> ou <b style="color: #dc2626">manquante</b>.</div>
  <div class="step">Appuyez sur un jeune pour ouvrir sa fiche.</div>
  <div class="step">Pour ajouter la fiche sanitaire : cochez la case d'<b>accord de l'autorité parentale</b>, puis <span class="btn">Importer (PDF / IMG)</span>. Une photo prise avec le téléphone suffit.</div>
  <div class="step"><span class="btn">Consulter</span> ouvre la fiche, <span class="btn">Remplacer</span> la met à jour.</div>
  <div class="step">Renseignez aussi sa <b>progression personnelle</b> (étape, défi) et son <b>équipage</b>.</div>
</div>

<div class="tip">Seuls les chefs de votre unité peuvent voir ces fiches.</div>

</div>
<Phone src="/screens/unite.png" alt="Liste des membres" height="22.5rem" />
<Phone src="/screens/fiche-jeune.png" alt="Fiche d'un jeune" height="22.5rem" />
</div>

---

<span class="module-tag">Unité</span>

# Les équipages

<div class="grid grid-cols-[1fr_auto] gap-10 mt-4">
<div>

<div class="steps">
  <div class="step">Dans l'onglet <b>Unité</b>, passez sur <span class="btn">Équipages</span>.</div>
  <div class="step">Appuyez sur <span class="btn">Créer un équipage</span> et donnez-lui un nom.</div>
  <div class="step">Pour chaque jeune non affecté, choisissez son équipage dans <span class="btn">Affecter à…</span></div>
</div>

<div class="tip">Le compteur en haut indique combien de jeunes sont déjà affectés. L'équipage d'un jeune peut aussi être changé depuis sa fiche.</div>

<div class="tip warn">Les équipages sont enregistrés <b>sur l'appareil utilisé</b> : ils ne sont pas encore partagés entre les chefs.</div>

</div>
<Phone src="/screens/equipages.png" alt="Gestion des équipages" />
</div>

---
layout: center
class: section-slide text-center !bg-[#e85d22]
---

<div class="section-number">Partie 3</div>

# Camps

<p>Créer un week-end, construire le planning, préparer les activités</p>

---

<span class="module-tag orange">Camps</span>

# Créer un week-end ou une journée

<div class="grid grid-cols-[1fr_auto_auto] gap-6 mt-2">
<div>

<div class="steps">
  <div class="step">Dans l'onglet <b>Camps</b>, appuyez sur le bouton rond <span class="btn">+</span> en bas à droite.</div>
  <div class="step">Choisissez <b>Journée</b> ou <b>Week-end</b>.</div>
  <div class="step">Optionnel : partez d'un <b>modèle de planning</b> pour récupérer tous les créneaux d'un week-end type.</div>
  <div class="step">Indiquez le titre, les dates et le lieu, puis <span class="btn">Créer l'événement</span>.</div>
  <div class="step">Le week-end apparaît dans le calendrier : appuyez sur <span class="btn">Gérer l'activité</span> pour l'ouvrir.</div>
</div>

</div>
<Phone src="/screens/calendrier.png" alt="Calendrier des camps" height="22.5rem" />
<Phone src="/screens/nouveau-weekend.png" alt="Planifier un événement" height="22.5rem" />
</div>

---

<span class="module-tag orange">Camps</span>

# Construire le planning

<div class="grid grid-cols-[1fr_auto_auto] gap-6 mt-2">
<div>

<div class="steps">
  <div class="step">Dans le week-end, appuyez sur <span class="btn">+</span> pour ajouter un créneau.</div>
  <div class="step">Gagnez du temps avec les <b>presets en 1 clic</b> : Repas, Grand Jeu, Veillée, Rassemblement, Coucher.</div>
  <div class="step">Choisissez le <b>type</b>, les <b>chefs responsables</b>, le jour et les horaires, puis <span class="btn">Ajouter au planning</span>.</div>
  <div class="step">Sur chaque créneau : ✏️ pour modifier, 🗑️ pour supprimer.</div>
</div>

<div class="tip"><b>Un retard ?</b> Le bouton <span class="btn">+15 min</span> décale toute la suite de la journée d'un coup. Deux affichages possibles : cartes ou frise chronologique.</div>

</div>
<Phone src="/screens/planning.png" alt="Planning du week-end" height="22.5rem" />
<Phone src="/screens/ajout-creneau.png" alt="Ajouter une activité" height="22.5rem" />
</div>

---

<span class="module-tag orange">Camps</span>

# Préparer une activité

<div class="grid grid-cols-[1fr_auto] gap-10 mt-2">
<div>

<div class="subtitle">Sur un créneau de type Jeu / Anim, appuyez sur <span class="btn">Ouvrir la fiche</span>.</div>

<div class="steps">
  <div class="step"><b>Chefs présents</b> : qui prépare et anime l'activité.</div>
  <div class="step"><b>Le Déroulé</b> : partez d'une trame (<b>Grand Jeu</b>, <b>Veillée</b>, <b>Olympiades</b>) ou ajoutez vos étapes minutées.</div>
  <div class="step"><b>Lieu & Plan B Météo</b> : l'emplacement prévu et le repli en cas de pluie.</div>
  <div class="step"><b>Imaginaire & Objectifs</b>, puis la liste du <b>Matériel</b>.</div>
  <div class="step">N'oubliez pas <span class="btn">Enregistrer</span> en haut de la fiche.</div>
</div>

</div>
<Phone src="/screens/fiche-activite.png" alt="Fiche d'activité" />
</div>

---
layout: center
class: section-slide text-center !bg-[#5b2b82]
---

<div class="section-number">Partie 4</div>

# Intendance

<p>Des menus à la liste de courses, sans calculatrice</p>

---

<span class="module-tag violet">Intendance</span>

# Menus et liste de courses

<div class="grid grid-cols-[1fr_auto_auto] gap-6 mt-2">
<div>

<div class="steps">
  <div class="step">Sur un créneau de type <b>Repas</b>, appuyez sur <span class="btn">Ouvrir le menu</span>.</div>
  <div class="step"><span class="btn">Ajouter</span> des plats depuis le catalogue (~180 recettes de camp) ou un <b>produit libre</b>.</div>
  <div class="step">Dans le week-end, <span class="btn">Courses globales</span> regroupe tous les ingrédients, <b>classés par rayon</b>, avec des cases à cocher au magasin.</div>
  <div class="step">Activez la <b>marge de sécurité (+10 %)</b> pour que personne n'ait faim.</div>
</div>

<div class="tip"><b>Remplissez d'abord le registre de présence</b> (page suivante) : les quantités sont calculées sur les présents, avec des portions différentes pour les jeunes et les adultes. Sans registre, le calcul prend toute l'unité.</div>

</div>
<Phone src="/screens/menu-repas.png" alt="Composition du menu" height="22.5rem" />
<Phone src="/screens/courses.png" alt="Liste de courses" height="22.5rem" />
</div>

---
layout: center
class: section-slide text-center !bg-[#004267]
---

<div class="section-number">Partie 5</div>

# Effectifs & matériel du week-end

<p>Présences, tentes, chefs renforts et dossier de camp</p>

---

<span class="module-tag">Week-end</span>

# Présences, tentes et matériel

<div class="grid grid-cols-[1fr_auto_auto] gap-6 mt-2">
<div>

<div class="subtitle">En bas du planning, l'encadré <b>Effectifs, Intendance & Matériel</b> :</div>

<div class="steps">
  <div class="step"><span class="btn">Présence au week-end</span> : cochez les jeunes et les chefs présents, puis <span class="btn">Enregistrer les présences</span>.</div>
  <div class="step"><span class="btn">Tentes & Matériel</span>, onglet <b>Matériel à emporter</b> : votre checklist, à remplir à la main ou depuis un <b>modèle de matériel</b> réutilisable.</div>
  <div class="step">Onglet <b>Tentes</b> : réservez les tentes du groupe. La capacité totale s'affiche, et les tentes déjà prises par un autre camp sont signalées.</div>
</div>

</div>
<Phone src="/screens/presence.png" alt="Registre de présence" height="22.5rem" />
<Phone src="/screens/materiel.png" alt="Matériel et tentes" height="22.5rem" />
</div>

---

<span class="module-tag">Week-end</span>

# Les options du week-end

<div class="grid grid-cols-[1fr_auto] gap-10 mt-2">
<div>

<div class="subtitle">Le menu <b>⋮</b> en haut à droite du planning :</div>

<div class="steps">
  <div class="step"><b>Modifier les infos</b> : nom, lieu, dates du week-end.</div>
  <div class="step"><b>Inviter un chef</b> : ajoutez un renfort d'une autre unité avec son <b>numéro d'adhérent SGDF</b>. Il verra ce week-end dans son calendrier.</div>
  <div class="step"><b>Exporter le dossier (PDF)</b> : registre de présence, planning, fiches d'activité, menus et matériel, prêts à imprimer.</div>
  <div class="step"><b>Enregistrer comme modèle</b> : réutilisez ce planning pour vos prochains week-ends.</div>
</div>

<div class="tip">Vos modèles se retrouvent dans <b>Profil</b> → <span class="btn">Gérer mes modèles</span>.</div>

</div>
<Phone src="/screens/planning-options.png" alt="Options du week-end" />
</div>

---
layout: center
class: section-slide text-center !bg-[#16a34a]
---

<div class="section-number">Partie 6</div>

# Logistique & profil

<p>Le matériel du groupe, les lieux de camp et vos réglages</p>

---

<span class="module-tag green">Logistique</span>

# Le parc de tentes et les lieux de camp

<div class="grid grid-cols-[1fr_auto_auto] gap-6 mt-2">
<div>

<div class="subtitle">L'onglet <b>Logistique</b> est partagé entre toutes les unités de votre groupe.</div>

<div class="steps">
  <div class="step"><b>Parc de Tentes</b> : <span class="btn">Ajouter une tente</span> avec sa capacité. Le bilan « prêtes / à réparer » est automatique.</div>
  <div class="step">Au retour de camp, <span class="btn">Signaler incident</span> sur une tente abîmée ou incomplète. Une fois réparée : <span class="btn">Marquer réparée</span>.</div>
  <div class="step"><b>Lieux de camp</b> : votre carnet d'adresses (contact du propriétaire, commodités), en liste ou sur carte. Vous pouvez <b>partager un lieu</b> avec les autres maîtrises.</div>
</div>

</div>
<Phone src="/screens/tentes.png" alt="Parc de tentes" height="22.5rem" />
<Phone src="/screens/lieux.png" alt="Lieux de camp" height="22.5rem" />
</div>

---

<span class="module-tag green">Profil</span>

# Votre profil

<div class="grid grid-cols-[1fr_auto] gap-10 mt-4">
<div>

<div class="steps">
  <div class="step"><b>Mode Sombre</b> : plus confortable le soir, et économe en batterie.</div>
  <div class="step"><b>Liens utiles</b> : <span class="btn">+ Ajouter</span> vos raccourcis (intranet, dossiers partagés, grilles…).</div>
  <div class="step"><b>Gérer mes modèles</b> : vos plannings types et checklists de matériel.</div>
  <div class="step"><b>Mentions Légales & RGPD</b>, installation de l'application, et <b>Se déconnecter</b> en bas de page.</div>
</div>

<div class="tip warn">Sur un téléphone partagé, pensez à <b>vous déconnecter</b> : cela efface aussi les données gardées sur l'appareil.</div>

</div>
<Phone src="/screens/profil.png" alt="Profil" />
</div>

---
layout: center
class: section-slide text-center !bg-[#004267]
---

<div class="section-number">Partie 7</div>

# Sur le terrain

<p>Utiliser PolyMaîtrise avec un réseau faible ou absent</p>

---

<span class="module-tag">Terrain</span>

# Réseau faible : ce qu'il faut savoir

<div class="grid grid-cols-[1fr_auto_auto] gap-6 mt-2">
<div>

<div class="steps">
  <div class="step"><b>Sans réseau</b>, un bandeau orange s'affiche. Les écrans <b>déjà ouverts avec du réseau</b> restent consultables : membres, planning, menus, courses…</div>
  <div class="step"><b>Réseau lent</b> : l'application réessaie toute seule. Si le réseau ne répond pas, elle affiche les dernières données connues.</div>
  <div class="step">Un <b>bandeau rouge</b> signifie qu'une modification <b>n'a pas été enregistrée</b> : refaites-la quand le réseau revient.</div>
</div>

<div class="tip"><b>Avant de partir en camp</b>, avec du réseau, ouvrez une fois chaque écran dont vous aurez besoin (planning, menus, courses, registre).</div>

<div class="tip warn">Les <b>documents</b> (fiches sanitaires) nécessitent du réseau pour être ouverts : imprimez le dossier PDF ou gardez une copie papier pour le camp.</div>

</div>
<Phone src="/screens/hors-ligne.png" alt="Bandeau hors-ligne" height="22.5rem" />
<Phone src="/screens/alerte-reseau.png" alt="Alerte de modification non enregistrée" height="22.5rem" />
</div>

---

# Vos données sont protégées

<div class="subtitle">Les données de santé et d'identité des jeunes exigent une rigueur particulière.</div>

<div class="grid grid-cols-2 gap-5 mt-6">
  <div class="card">
    <h3 style="color: var(--pm-blue)">Cloisonnement par unité</h3>
    <p>Chaque maîtrise n'accède qu'aux jeunes, fiches et week-ends de sa propre unité, et aux week-ends où elle est invitée. Les tentes et les lieux sont partagés au sein du groupe ; les recettes que vous créez enrichissent le catalogue commun.</p>
  </div>
  <div class="card">
    <h3 style="color: var(--pm-blue)">Fiches sanitaires</h3>
    <p>Importées uniquement après confirmation de l'accord de l'autorité parentale. Elles ne s'ouvrent que via des liens temporaires, réservés aux chefs de l'unité.</p>
  </div>
  <div class="card">
    <h3 style="color: var(--pm-blue)">Identifiants intranet</h3>
    <p>Votre mot de passe sert à ouvrir la session intranet SGDF. Il n'est jamais enregistré par PolyMaîtrise.</p>
  </div>
  <div class="card">
    <h3 style="color: var(--pm-blue)">Hébergement</h3>
    <p>Application et documents hébergés en France (OVH, Strasbourg), avec une connexion chiffrée (HTTPS).</p>
  </div>
</div>

---

# Questions fréquentes

<div class="grid grid-cols-2 gap-x-8 gap-y-4 mt-6 text-sm">
<div>

**« Votre session a expiré »**<br>
Reconnectez-vous avec vos identifiants intranet. Vous revenez là où vous étiez.

</div>
<div>

**« Trop de tentatives de connexion »**<br>
Patientez une minute avant de réessayer.

</div>
<div>

**Il manque des jeunes dans mon unité**<br>
Onglet Unité → <span class="btn">Resynchroniser</span> pour récupérer la liste à jour depuis l'intranet.

</div>
<div>

**Je ne vois pas la modification d'un autre chef**<br>
Rechargez la page : les changements des autres chefs n'apparaissent pas en direct.

</div>
<div>

**La fiche sanitaire ne s'ouvre plus**<br>
Les liens vers les documents expirent après 24 h : rechargez la page, puis rouvrez la fiche du jeune.

</div>
<div>

**Un chef d'une autre unité nous rejoint**<br>
Planning du week-end → menu ⋮ → <b>Inviter un chef</b>, avec son numéro d'adhérent.

</div>
</div>

---
layout: center
class: text-center
---

# Prêt à outiller votre maîtrise ?

<div class="grid grid-cols-2 gap-8 max-w-2xl mx-auto mt-6 items-center bg-white p-6 rounded-3xl shadow-xl text-left">
  <div>
    <h3 class="text-2xl font-black text-gray-900 leading-tight">Testez avec le mode Démo</h3>
    <p class="text-sm text-gray-600 mt-2 font-medium leading-relaxed">
      Explorez l'application avec une unité fictive en 1 clic, sans compte ni mot de passe.
    </p>
    <p class="text-sm text-gray-600 mt-3 font-medium leading-relaxed">
      Puis connectez-vous avec vos <b>identifiants de l'intranet SGDF</b> : votre unité est importée automatiquement.
    </p>
  </div>
  <div class="flex flex-col items-center justify-center border-l-2 border-gray-100 pl-6 text-center">
    <div class="bg-white p-3 rounded-2xl shadow-md border border-gray-200">
      <img src="/qr-polymaitrise.png" alt="QR Code PolyMaîtrise" class="w-36 h-36 rounded-lg object-contain">
    </div>
    <span class="text-xs text-gray-500 font-bold mt-3">Scannez pour ouvrir sur smartphone</span>
    <span class="text-sm font-black mt-0.5" style="color: var(--pm-blue)">polymaitrise.fr</span>
  </div>
</div>

<div class="mt-8 text-xs text-gray-400 font-bold uppercase tracking-widest">
  Développé par un chef scout, pour les maîtrises SGDF
</div>
