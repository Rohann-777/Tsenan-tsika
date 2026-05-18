"""
Service métier pour la gestion des prix dans Tsenan'tsika.

Ce module contient la logique applicative qui orchestre les
interactions entre les algorithmes, le repository et les données
brutes. C'est ici que les règles métier sont appliquées et que
les résultats sont préparés pour l'envoi au frontend.

Le service ne sait rien de HTTP ni de SQL. Il manipule uniquement
des objets Python et des structures de données, ce qui le rend
facilement testable indépendamment du reste de l'application.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.backend.repositories.prix_repository import PrixRepository
from src.backend.algorithms.fenwick_tree import FenwickTree


class PrixService:
    """
    Service métier pour les opérations liées aux prix.
    
    Cette classe coordonne les interactions entre le repository qui
    accède aux données et le Fenwick Tree qui effectue les calculs
    statistiques sur ces données.
    """
    
    def __init__(self):
        """
        Initialise le service avec une instance du repository.
        """
        self.repository = PrixRepository()
    
    def obtenir_prix_recents(self, db: Session, limite: int = 100):
        """
        Récupère les prix marché les plus récents pour affichage
        sur le tableau de bord public consultable par les citoyens.
        """
        return self.repository.lister_tous_les_prix(db, limite)
    
    def obtenir_prix_par_ville(self, db: Session, ville_id: int):
        """
        Récupère les prix pour une ville spécifique avec un nombre
        limité d'entrées pour les performances.
        """
        return self.repository.lister_prix_par_ville(db, ville_id, limite=50)
    
    def calculer_prix_moyen(
        self, db: Session, produit_id: int, ville_id: int, jours: int = 7
    ):
        """
        Calcule le prix moyen d'un produit dans une ville sur une
        période donnée en utilisant le Fenwick Tree.
        
        Cette méthode démontre l'intégration concrète du Fenwick Tree
        dans la logique métier. Les prix sont d'abord récupérés depuis
        la base, puis insérés dans un Fenwick Tree pour permettre
        le calcul efficace de la moyenne sur l'intervalle.
        
        Pour une utilisation en production avec beaucoup de requêtes,
        le Fenwick Tree pourrait être maintenu en mémoire de manière
        persistante au lieu d'être reconstruit à chaque appel, mais
        pour notre prototype cette approche reste acceptable.
        """
        # Récupération de l'historique depuis la base
        historique = self.repository.lister_prix_par_produit_et_ville(
            db, produit_id, ville_id, jours
        )
        
        if not historique:
            return None
        
        # Construction du Fenwick Tree avec les prix de l'historique
        fenwick = FenwickTree(len(historique))
        for index, prix_marche in enumerate(historique):
            fenwick.mettre_a_jour(index, prix_marche.prix)
        
        # Calcul de la moyenne sur tout l'intervalle disponible
        prix_moyen = fenwick.calculer_moyenne(0, len(historique) - 1)
        
        # Récupération des informations associées pour la réponse
        premier_prix = historique[0]
        return {
            "produit_id": produit_id,
            "produit_nom": premier_prix.produit.nom_fr,
            "ville_id": ville_id,
            "ville_nom": premier_prix.ville.nom,
            "prix_moyen": round(prix_moyen, 2),
            "nombre_releves": len(historique),
            "periode_debut": historique[0].date_saisie,
            "periode_fin": historique[-1].date_saisie
        }
    
    def obtenir_produits(self, db: Session):
        """
        Récupère la liste des produits disponibles.
        """
        return self.repository.lister_produits(db)
    
    def obtenir_villes(self, db: Session):
        """
        Récupère la liste des villes pilotes.
        """
        return self.repository.lister_villes(db)