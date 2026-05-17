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
    Crée les sept villes pilotes de Tsenan'tsika avec leurs coordonnées
    géographiques réelles. Ces coordonnées correspondent aux centres
    de chaque ville et permettront un affichage sur carte si on ajoute
    cette fonctionnalité au frontend.
    """
    print("Génération des villes...")
    
    villes_data = [
        {"nom": "Antananarivo", "region": "Analamanga", "latitude": -18.8792, "longitude": 47.5079},
        {"nom": "Toamasina", "region": "Atsinanana", "latitude": -18.1497, "longitude": 49.4022},
        {"nom": "Antsirabe", "region": "Vakinankaratra", "latitude": -19.8666, "longitude": 47.0333},
        {"nom": "Mahajanga", "region": "Boeny", "latitude": -15.7167, "longitude": 46.3167},
        {"nom": "Fianarantsoa", "region": "Haute Matsiatra", "latitude": -21.4536, "longitude": 47.0858},
        {"nom": "Toliara", "region": "Atsimo-Andrefana", "latitude": -23.3500, "longitude": 43.6667},
        {"nom": "Antsiranana", "region": "Diana", "latitude": -12.2787, "longitude": 49.2917}
    ]
    
    villes = []
    for data in villes_data:
        ville = Ville(**data)
        db.add(ville)
        villes.append(ville)
    
    db.commit()
    print(f"  - {len(villes)} villes créées.")
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
    Crée les connexions routières entre les villes avec leurs coûts
    de transport. Les coûts sont calculés à partir des distances
    approximatives entre les villes multipliées par un indice carburant
    fictif. Ces données alimentent l'algorithme de Dijkstra pour le
    calcul des itinéraires d'approvisionnement.
    
    Le graphe est non orienté donc on crée une connexion dans chaque
    sens pour chaque paire de villes connectées. Cela facilite
    l'utilisation par Dijkstra qui traite les arêtes comme directionnelles.
    """
    print("Génération des connexions routières...")
    
    # Dictionnaire pour retrouver facilement les villes par leur nom
    villes_par_nom = {ville.nom: ville for ville in villes}
    
    # Liste des connexions avec leurs coûts en unité arbitraire
    # Les coûts sont basés sur les distances routières réelles
    connexions_data = [
        ("Antananarivo", "Toamasina", 350),
        ("Antananarivo", "Antsirabe", 170),
        ("Antananarivo", "Mahajanga", 570),
        ("Antananarivo", "Fianarantsoa", 410),
        ("Antsirabe", "Fianarantsoa", 240),
        ("Fianarantsoa", "Toliara", 410),
        ("Mahajanga", "Antsiranana", 800)
    ]
    
    connexions = []
    for nom_depart, nom_destination, cout in connexions_data:
        # On crée une connexion dans chaque sens pour avoir un graphe
        # non orienté tout en utilisant une représentation orientée
        connexion_aller = ConnexionVille(
            ville_depart_id=villes_par_nom[nom_depart].id,
            ville_destination_id=villes_par_nom[nom_destination].id,
            cout=cout
        )
        connexion_retour = ConnexionVille(
            ville_depart_id=villes_par_nom[nom_destination].id,
            ville_destination_id=villes_par_nom[nom_depart].id,
            cout=cout
        )
        db.add(connexion_aller)
        db.add(connexion_retour)
        connexions.extend([connexion_aller, connexion_retour])
    
    db.commit()
    print(f"  - {len(connexions)} connexions créées.")
    return connexions


def generer_utilisateurs(db):
    """
    Crée des utilisateurs de test pour chaque rôle du système.
    Les mots de passe sont hachés avec bcrypt avant stockage,
    conformément aux contraintes de sécurité du projet.
    
    Les utilisateurs créés correspondent aux quatre acteurs définis
    dans le diagramme de cas d'utilisation : agents de collecte,
    analystes, citoyens et administrateurs.
    """
    print("Génération des utilisateurs...")
    
    utilisateurs_data = [
        # Administrateurs
        {
            "nom": "Rakoto", "prenoms": "Jean",
            "email": "admin@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("admin123"),
            "role": "administrateur"
        },
        # Analystes du ministère
        {
            "nom": "Razafindrabe", "prenoms": "Marie",
            "email": "marie.analyste@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("analyste123"),
            "role": "analyste"
        },
        {
            "nom": "Andrianarisoa", "prenoms": "Paul",
            "email": "paul.analyste@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("analyste123"),
            "role": "analyste"
        },
        # Agents de collecte pour chaque ville pilote
        {
            "nom": "Rasoamanarivo", "prenoms": "Sophie",
            "email": "sophie.agent@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("agent123"),
            "role": "agent"
        },
        {
            "nom": "Ratsimba", "prenoms": "Pierre",
            "email": "pierre.agent@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("agent123"),
            "role": "agent"
        },
        {
            "nom": "Andriamanantena", "prenoms": "Claire",
            "email": "claire.agent@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("agent123"),
            "role": "agent"
        },
        # Citoyens
        {
            "nom": "Rakotonirina", "prenoms": "Tiana",
            "email": "tiana.citoyen@tsenantsika.mg",
            "mot_de_passe": hacher_mot_de_passe("citoyen123"),
            "role": "citoyen"
        }
    ]
    
    utilisateurs = []
    for data in utilisateurs_data:
        utilisateur = Utilisateur(**data)
        db.add(utilisateur)
        utilisateurs.append(utilisateur)
    
    db.commit()
    print(f"  - {len(utilisateurs)} utilisateurs créés.")
    return utilisateurs


def generer_historique_prix(db, villes, produits, utilisateurs):
    """
    Génère un historique de prix réaliste sur six semaines pour
    permettre aux algorithmes Fenwick Tree et Top-k d'avoir
    suffisamment de données à analyser.
    
    Les prix de base sont définis par produit selon les niveaux
    de prix réels observés à Madagascar, puis ils varient légèrement
    chaque jour pour simuler les fluctuations naturelles du marché.
    Quelques anomalies sont intentionnellement injectées pour démontrer
    que le système d'alertes fonctionne correctement.
    """
    print("Génération de l'historique des prix...")
    
    # Filtrage des agents pour la saisie des prix
    agents = [u for u in utilisateurs if u.role == "agent"]
    
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
        
        for ville in villes:
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
                        agent_id=random.choice(agents).id
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
    Fonction principale qui orchestre la génération complète des
    données dans le bon ordre.
    """
    print("=" * 60)
    print("Génération des données synthétiques pour Tsenan'tsika")
    print("=" * 60)
    
    # Fixation de la graine aléatoire pour reproductibilité
    random.seed(42)
    
    db = SessionLocal()
    
    try:
        vider_base_de_donnees(db)
        villes = generer_villes(db)
        produits = generer_produits(db)
        generer_connexions(db, villes)
        utilisateurs = generer_utilisateurs(db)
        generer_historique_prix(db, villes, produits, utilisateurs)
        generer_alertes(db, villes, produits)
        
        print("\n" + "=" * 60)
        print("Génération terminée avec succès !")
        print("=" * 60)
        print("\nIdentifiants de test pour la connexion :")
        print("  Administrateur : admin@tsenantsika.mg / admin123")
        print("  Analyste       : marie.analyste@tsenantsika.mg / analyste123")
        print("  Agent          : sophie.agent@tsenantsika.mg / agent123")
        print("  Citoyen        : tiana.citoyen@tsenantsika.mg / citoyen123")
        
    except Exception as e:
        print(f"\nErreur durant la génération : {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    executer_generation()