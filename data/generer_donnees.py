"""
Script de génération de données synthétiques pour Tsenan'tsika.

Ce script peuple la base de données PostgreSQL avec un jeu de données
réaliste qui permet de démontrer toutes les fonctionnalités du système
et de tester les quatre algorithmes implémentés. Les données reflètent
le contexte réel de Madagascar avec les sept villes pilotes, les sept
produits de première nécessité et un historique de prix sur six semaines.

Pour exécuter ce script depuis la racine du projet avec l'environnement
virtuel activé, utilise la commande suivante :

    python -m data.generer_donnees

Le script peut être relancé plusieurs fois car il vide les tables avant
de les repeupler, ce qui garantit un état cohérent à chaque exécution.
"""

import random
from datetime import datetime, timedelta
import bcrypt

from src.backend.config.database import SessionLocal
from src.backend.models.modeles import (
    Utilisateur, Produit, Ville, ConnexionVille,
    PrixMarche, RapportPrix, Alerte
)


def hacher_mot_de_passe(mot_de_passe_clair):
    """
    Hache un mot de passe avec bcrypt pour le stockage sécurisé.
    
    Cette fonction utilise bcrypt qui est l'algorithme de hachage
    recommandé pour les mots de passe car il intègre un salt aléatoire
    et un coût computationnel configurable qui rend les attaques par
    force brute extrêmement lentes. Cela correspond à la contrainte
    de sécurité définie dans ton cahier des charges.
    """
    mot_de_passe_bytes = mot_de_passe_clair.encode('utf-8')
    sel = bcrypt.gensalt()
    hachage = bcrypt.hashpw(mot_de_passe_bytes, sel)
    return hachage.decode('utf-8')


def vider_base_de_donnees(db):
    """
    Supprime toutes les données existantes dans les tables avant
    de générer le nouveau jeu de données.
    
    L'ordre de suppression est inversé par rapport à l'ordre de création
    pour respecter les contraintes de clés étrangères. On supprime
    d'abord les tables qui référencent d'autres tables, puis les tables
    référencées.
    """
    print("Suppression des données existantes...")
    db.query(Alerte).delete()
    db.query(PrixMarche).delete()
    db.query(RapportPrix).delete()
    db.query(ConnexionVille).delete()
    db.query(Utilisateur).delete()
    db.query(Produit).delete()
    db.query(Ville).delete()
    db.commit()
    print("Tables vidées avec succès.")


def generer_villes(db):
    """
    Crée les villes du réseau routier malgache pour Tsenan'tsika.
    
    Le réseau comprend deux catégories de villes. Les sept villes pilotes
    sont celles où les agents de collecte saisissent les prix des marchés
    et constituent le périmètre fonctionnel principal du système. Les
    treize villes complémentaires sont des nœuds routiers stratégiques
    qui enrichissent le graphe utilisé par l'algorithme de Dijkstra pour
    le calcul d'itinéraires optimaux d'approvisionnement.
    
    Cette distinction architecturale entre villes pilotes et nœuds routiers
    reflète la réalité métier où la collecte de données et la planification
    logistique opèrent à des granularités différentes.
    """
    print("Génération des villes du réseau routier malgache...")
    
    villes_data = [
        # Les sept villes pilotes pour la collecte des prix
        {"nom": "Antananarivo", "region": "Analamanga", "latitude": -18.8792, "longitude": 47.5079},
        {"nom": "Toamasina", "region": "Atsinanana", "latitude": -18.1492, "longitude": 49.4023},
        {"nom": "Antsirabe", "region": "Vakinankaratra", "latitude": -19.8659, "longitude": 47.0333},
        {"nom": "Mahajanga", "region": "Boeny", "latitude": -15.7167, "longitude": 46.3167},
        {"nom": "Fianarantsoa", "region": "Haute Matsiatra", "latitude": -21.4536, "longitude": 47.0854},
        {"nom": "Toliara", "region": "Atsimo-Andrefana", "latitude": -23.3539, "longitude": 43.6710},
        {"nom": "Antsiranana", "region": "Diana", "latitude": -12.2787, "longitude": 49.2917},
        
        # Les treize villes intermédiaires stratégiques du réseau routier
        {"nom": "Moramanga", "region": "Alaotra-Mangoro", "latitude": -18.9333, "longitude": 48.2000},
        {"nom": "Ambositra", "region": "Amoron'i Mania", "latitude": -20.5333, "longitude": 47.2500},
        {"nom": "Ihosy", "region": "Ihorombe", "latitude": -22.4000, "longitude": 46.1167},
        {"nom": "Tolagnaro", "region": "Anosy", "latitude": -25.0319, "longitude": 46.9994},
        {"nom": "Ambovombe", "region": "Androy", "latitude": -25.1739, "longitude": 46.0900},
        {"nom": "Maevatanana", "region": "Betsiboka", "latitude": -16.9500, "longitude": 46.8333},
        {"nom": "Ambondromamy", "region": "Boeny", "latitude": -16.4167, "longitude": 47.1500},
        {"nom": "Antsohihy", "region": "Sofia", "latitude": -14.8833, "longitude": 47.9833},
        {"nom": "Ambanja", "region": "Diana", "latitude": -13.6833, "longitude": 48.4500},
        {"nom": "Tsiroanomandidy", "region": "Bongolava", "latitude": -18.7667, "longitude": 46.0500},
        {"nom": "Manakara", "region": "Vatovavy", "latitude": -22.1333, "longitude": 48.0167},
        {"nom": "Sambava", "region": "Sava", "latitude": -14.2667, "longitude": 50.1667},
        {"nom": "Maintirano", "region": "Melaky", "latitude": -18.0667, "longitude": 44.0333},
    ]
    
    villes = []
    for data in villes_data:
        ville = Ville(**data)
        db.add(ville)
        villes.append(ville)
    
    db.commit()
    print(f"  - {len(villes)} villes créées dans le réseau routier.")
    return villes


def generer_produits(db):
    """
    Crée les sept produits de première nécessité avec leurs noms en
    français et en malgache. Cette double dénomination prépare le
    support multilingue du système.
    """
    print("Génération des produits...")
    
    produits_data = [
        {"nom_fr": "Riz", "nom_mg": "Vary", "unite": "kg", "categorie": "cereale"},
        {"nom_fr": "Maïs", "nom_mg": "Katsaka", "unite": "kg", "categorie": "cereale"},
        {"nom_fr": "Manioc", "nom_mg": "Mangahazo", "unite": "kg", "categorie": "tubercule"},
        {"nom_fr": "Haricot", "nom_mg": "Tsaramaso", "unite": "kg", "categorie": "legumineuse"},
        {"nom_fr": "Huile", "nom_mg": "Menaka", "unite": "litre", "categorie": "matiere_grasse"},
        {"nom_fr": "Sucre", "nom_mg": "Siramamy", "unite": "kg", "categorie": "epicerie"},
        {"nom_fr": "Sel", "nom_mg": "Sira", "unite": "kg", "categorie": "epicerie"}
    ]
    
    produits = []
    for data in produits_data:
        produit = Produit(**data)
        db.add(produit)
        produits.append(produit)
    
    db.commit()
    print(f"  - {len(produits)} produits créés.")
    return produits


def generer_connexions(db, villes):
    """
    Crée les connexions routières entre les villes du réseau malgache.
    
    Chaque connexion représente un segment de route nationale reliant
    directement deux villes. Le coût de chaque connexion est calculé
    en multipliant la distance approximative en kilomètres par un indice
    carburant régional qui reflète l'état des routes et la difficulté
    d'approvisionnement en carburant dans les différentes régions.
    
    Le graphe résultant comprend une quarantaine d'arêtes qui permettent
    à l'algorithme de Dijkstra d'évaluer véritablement plusieurs alternatives
    pour chaque trajet calculé, mettant en valeur sa puissance algorithmique.
    """
    print("Génération des connexions routières du réseau malgache...")
    
    # Création d'un dictionnaire pour retrouver facilement les villes par nom
    villes_par_nom = {ville.nom: ville for ville in villes}
    
    # Liste des connexions routières basées sur le réseau réel de Madagascar.
    # Le format est ville_depart, ville_arrivee, distance_km, indice_carburant.
    # L'indice carburant varie entre 1.0 pour les routes principales en bon
    # état et 1.5 pour les segments en mauvais état ou difficiles d'accès.
    connexions_data = [
        # Route nationale 2 vers l'est jusqu'à Toamasina
        ("Antananarivo", "Moramanga", 110, 1.0),
        ("Moramanga", "Toamasina", 250, 1.1),
        
        # Route nationale 7 vers le sud jusqu'à Toliara
        ("Antananarivo", "Antsirabe", 165, 1.0),
        ("Antsirabe", "Ambositra", 90, 1.0),
        ("Ambositra", "Fianarantsoa", 145, 1.0),
        ("Fianarantsoa", "Ihosy", 200, 1.1),
        ("Ihosy", "Toliara", 320, 1.2),
        
        # Route nationale 13 du sud-est
        ("Ihosy", "Ambovombe", 280, 1.3),
        ("Ambovombe", "Tolagnaro", 110, 1.3),
        
        # Route nationale 4 vers le nord-ouest jusqu'à Mahajanga
        ("Antananarivo", "Maevatanana", 270, 1.0),
        ("Maevatanana", "Ambondromamy", 180, 1.1),
        ("Ambondromamy", "Mahajanga", 110, 1.0),
        
        # Route nationale 6 vers le nord jusqu'à Antsiranana
        ("Ambondromamy", "Antsohihy", 230, 1.2),
        ("Antsohihy", "Ambanja", 270, 1.3),
        ("Ambanja", "Antsiranana", 240, 1.2),
        
        # Route nationale 1 vers l'ouest
        ("Antananarivo", "Tsiroanomandidy", 220, 1.1),
        ("Tsiroanomandidy", "Maintirano", 360, 1.5),
        
        # Route nationale 12 sur la côte est sud
        ("Fianarantsoa", "Manakara", 240, 1.2),
        ("Manakara", "Tolagnaro", 380, 1.4),
        
        # Route nationale 5a vers le nord-est depuis Antsiranana
        ("Antsiranana", "Sambava", 320, 1.4),
        
        # Connexions secondaires qui enrichissent le graphe
        ("Antsirabe", "Tsiroanomandidy", 180, 1.3),
        ("Antananarivo", "Toamasina", 360, 1.1),
        ("Tsiroanomandidy", "Maevatanana", 200, 1.4),
        ("Sambava", "Antsohihy", 280, 1.5),
        ("Moramanga", "Antsirabe", 240, 1.2),
    ]
    
    connexions_creees = 0
    for nom_depart, nom_arrivee, distance, indice in connexions_data:
        ville_depart = villes_par_nom[nom_depart]
        ville_arrivee = villes_par_nom[nom_arrivee]
        
        # Le coût est calculé selon la formule du cahier des charges
        cout = distance * indice
        
        # Création de la connexion dans les deux sens car le graphe est
        # non orienté, les routes peuvent être empruntées dans les deux
        # directions avec le même coût
        connexion_aller = ConnexionVille(
            ville_depart_id=ville_depart.id,
            ville_destination_id=ville_arrivee.id,
            cout=cout
        )
        connexion_retour = ConnexionVille(
            ville_depart_id=ville_arrivee.id,
            ville_destination_id=ville_depart.id,
            cout=cout
        )
        
        db.add(connexion_aller)
        db.add(connexion_retour)
        connexions_creees += 2
    
    db.commit()
    print(f"  - {connexions_creees} connexions routières créées ({connexions_creees // 2} liaisons bidirectionnelles).")


def generer_utilisateurs(db, villes):
    """
    Crée des utilisateurs de test pour chaque rôle du système avec leurs
    nouveaux attributs de statut de compte et ville assignée.
    
    Sept agents sont créés, un pour chaque ville pilote, ce qui reflète
    la nouvelle architecture où la ville assignée est véritablement
    contraignante. Chaque agent ne peut saisir des prix que pour la ville
    à laquelle il est affecté, garantissant ainsi la cohérence administrative
    et la qualité des données collectées sur le terrain.
    """
    print("Génération des utilisateurs...")
    
    # Création d'un dictionnaire pour retrouver facilement les villes par nom
    villes_par_nom = {ville.nom: ville for ville in villes}
    
    utilisateurs_data = [
        # Administrateur du système qui gère les autres comptes
        {
            "nom": "Rakoto", "prenoms": "Jean",
            "email": "admin@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("admin123"),
            "role": "administrateur",
            "statut_compte": True,
            "ville_assignee_id": None
        },
        # Analystes du ministère qui travaillent depuis Antananarivo
        {
            "nom": "Razafindrabe", "prenoms": "Marie",
            "email": "marie.analyste@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("analyste123"),
            "role": "analyste",
            "statut_compte": True,
            "ville_assignee_id": None
        },
        {
            "nom": "Andrianarisoa", "prenoms": "Paul",
            "email": "paul.analyste@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("analyste123"),
            "role": "analyste",
            "statut_compte": True,
            "ville_assignee_id": None
        },
        # Sept agents de collecte, un pour chaque ville pilote
        {
            "nom": "Rasoamanarivo", "prenoms": "Sophie",
            "email": "sophie.agent@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("agent123"),
            "role": "agent",
            "statut_compte": True,
            "ville_assignee_id": villes_par_nom["Antananarivo"].id
        },
        {
            "nom": "Ratsimba", "prenoms": "Pierre",
            "email": "pierre.agent@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("agent123"),
            "role": "agent",
            "statut_compte": True,
            "ville_assignee_id": villes_par_nom["Toamasina"].id
        },
        {
            "nom": "Andriamanantena", "prenoms": "Claire",
            "email": "claire.agent@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("agent123"),
            "role": "agent",
            "statut_compte": True,
            "ville_assignee_id": villes_par_nom["Fianarantsoa"].id
        },
        {
            "nom": "Rakotondrasoa", "prenoms": "Hery",
            "email": "hery.agent@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("agent123"),
            "role": "agent",
            "statut_compte": True,
            "ville_assignee_id": villes_par_nom["Antsirabe"].id
        },
        {
            "nom": "Razafy", "prenoms": "Lalaina",
            "email": "lalaina.agent@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("agent123"),
            "role": "agent",
            "statut_compte": True,
            "ville_assignee_id": villes_par_nom["Mahajanga"].id
        },
        {
            "nom": "Andrianjafy", "prenoms": "Tahiana",
            "email": "tahiana.agent@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("agent123"),
            "role": "agent",
            "statut_compte": True,
            "ville_assignee_id": villes_par_nom["Toliara"].id
        },
        {
            "nom": "Randrianasolo", "prenoms": "Voahangy",
            "email": "voahangy.agent@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("agent123"),
            "role": "agent",
            "statut_compte": True,
            "ville_assignee_id": villes_par_nom["Antsiranana"].id
        },
        # Citoyen qui consulte le système sans ville assignée
        {
            "nom": "Rakotonirina", "prenoms": "Tiana",
            "email": "tiana.citoyen@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("citoyen123"),
            "role": "citoyen",
            "statut_compte": True,
            "ville_assignee_id": None
        }
    ]
    
    utilisateurs = []
    for data in utilisateurs_data:
        utilisateur = Utilisateur(**data)
        db.add(utilisateur)
        utilisateurs.append(utilisateur)
    
    db.commit()
    print(f"  - {len(utilisateurs)} utilisateurs créés avec assignations.")
    return utilisateurs


def generer_historique_prix(db, villes, produits, utilisateurs):
    """
    Génère un historique de prix réaliste sur six semaines pour permettre
    aux algorithmes Fenwick Tree et Top-k d'avoir suffisamment de données
    à analyser.
    
    Chaque prix est attribué à l'agent affecté à la ville correspondante,
    respectant ainsi la nouvelle logique où la ville assignée est
    véritablement contraignante. Cette cohérence garantit que les saisies
    historiques reflètent fidèlement l'organisation administrative du système.
    """
    print("Génération de l'historique des prix...")
    
    # Filtrage des agents pour la saisie des prix
    agents = [u for u in utilisateurs if u.role == "agent"]
    
    # Création d'un dictionnaire pour retrouver l'agent par ville assignée.
    # Cette structure permet une attribution rapide et cohérente des prix
    # à l'agent qui couvre effectivement chaque ville pilote.
    agent_par_ville = {agent.ville_assignee_id: agent for agent in agents}
    
    # Filtrage pour ne conserver que les sept villes pilotes
    villes_pilotes_noms = ['Antananarivo', 'Toamasina', 'Antsirabe', 'Mahajanga', 'Fianarantsoa', 'Toliara', 'Antsiranana']
    villes_pilotes = [v for v in villes if v.nom in villes_pilotes_noms]

    # Prix de base par produit en Ariary par unité
    # Ces valeurs sont approximatives mais réalistes pour Madagascar en 2026
    prix_de_base = {
        "Riz": 3500,
        "Maïs": 2200,
        "Manioc": 1500,
        "Haricot": 4000,
        "Huile": 8000,
        "Sucre": 4500,
        "Sel": 1200
    }
    
    # Génération sur 42 jours (six semaines) jusqu'à aujourd'hui
    date_fin = datetime.now()
    nombre_jours = 42
    
    prix_generes = []
    
    for jours_avant in range(nombre_jours, 0, -1):
        date_courante = date_fin - timedelta(days=jours_avant)
        
        for ville in villes_pilotes:
            # Sélection de l'agent assigné à cette ville pour respecter
            # la nouvelle logique d'assignation contraignante.
            agent_de_la_ville = agent_par_ville.get(ville.id)
            if not agent_de_la_ville:
                continue  # Ignore les villes sans agent assigné
            
            for produit in produits:
                # Pas toutes les villes ont tous les produits chaque jour
                # On simule une couverture partielle réaliste
                if random.random() < 0.7:  # 70% de chance d'avoir une saisie
                    prix_base = prix_de_base[produit.nom_fr]
                    
                    # Variation aléatoire de plus ou moins 10% autour du prix de base
                    variation = random.uniform(-0.10, 0.10)
                    prix = prix_base * (1 + variation)
                    
                    # Injection d'anomalies pour certains produits dans les derniers jours
                    # Cela permettra au Top-k de détecter des hausses
                    if jours_avant <= 3 and ville.nom == "Toliara" and produit.nom_fr == "Riz":
                        prix = prix * 1.5  # Hausse de 50% pour simuler une pénurie
                    if jours_avant <= 2 and ville.nom == "Antsiranana" and produit.nom_fr == "Huile":
                        prix = prix * 1.4  # Hausse de 40%
                    
                    prix_marche = PrixMarche(
                        produit_id=produit.id,
                        ville_id=ville.id,
                        prix=round(prix, 2),
                        date_saisie=date_courante,
                        agent_id=agent_de_la_ville.id
                    )
                    db.add(prix_marche)
                    prix_generes.append(prix_marche)
    
    db.commit()
    print(f"  - {len(prix_generes)} entrées de prix générées sur {nombre_jours} jours.")
    return prix_generes


def generer_alertes(db, villes, produits):
    """
    Génère quelques alertes correspondant aux anomalies de prix
    injectées dans l'historique. Ces alertes seraient normalement
    créées automatiquement par le Service quand Top-k détecte une
    hausse anormale, mais on les crée manuellement ici pour que
    le tableau de bord ait des données à afficher dès le départ.
    """
    print("Génération des alertes initiales...")
    
    villes_par_nom = {ville.nom: ville for ville in villes}
    produits_par_nom = {produit.nom_fr: produit for produit in produits}
    
    alertes_data = [
        {"ville": "Toliara", "produit": "Riz", "jours_avant": 1},
        {"ville": "Antsiranana", "produit": "Huile", "jours_avant": 1},
        {"ville": "Toliara", "produit": "Riz", "jours_avant": 2}
    ]
    
    alertes = []
    for data in alertes_data:
        alerte = Alerte(
            produit_id=produits_par_nom[data["produit"]].id,
            ville_id=villes_par_nom[data["ville"]].id,
            date=datetime.now() - timedelta(days=data["jours_avant"])
        )
        db.add(alerte)
        alertes.append(alerte)
    
    db.commit()
    print(f"  - {len(alertes)} alertes créées.")
    return alertes


def executer_generation():
    """
    Fonction principale qui orchestre la génération complète des données.
    """
    print("=" * 60)
    print("Génération des données synthétiques pour Tsenan'tsika")
    print("=" * 60)
    
    random.seed(42)
    db = SessionLocal()
    
    try:
        vider_base_de_donnees(db)
        villes = generer_villes(db)
        produits = generer_produits(db)
        generer_connexions(db, villes)
        # Les utilisateurs sont créés après les villes pour permettre l'assignation
        utilisateurs = generer_utilisateurs(db, villes)
        generer_historique_prix(db, villes, produits, utilisateurs)
        generer_alertes(db, villes, produits)
        
        print("\n" + "=" * 60)
        print("Génération terminée avec succès !")
        print("=" * 60)
        print("\nIdentifiants de test pour la connexion :")
        print("  Administrateur : admin@tsenantsika.mg / admin123")
        print("  Analystes :")
        print("    - marie.analyste@tsenantsika.mg / analyste123")
        print("    - paul.analyste@tsenantsika.mg / analyste123")
        print("  Agents de collecte :")
        print("    - sophie.agent@tsenantsika.mg / agent123 (Antananarivo)")
        print("    - pierre.agent@tsenantsika.mg / agent123 (Toamasina)")
        print("    - claire.agent@tsenantsika.mg / agent123 (Fianarantsoa)")
        print("    - hery.agent@tsenantsika.mg / agent123 (Antsirabe)")
        print("    - lalaina.agent@tsenantsika.mg / agent123 (Mahajanga)")
        print("    - tahiana.agent@tsenantsika.mg / agent123 (Toliara)")
        print("    - voahangy.agent@tsenantsika.mg / agent123 (Antsiranana)")
        print("  Citoyen : tiana.citoyen@tsenantsika.mg / citoyen123")
        
    except Exception as e:
        print(f"\nErreur durant la génération : {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    executer_generation()