"""
Repository pour l'accès aux données de prix dans Tsenan'tsika.

Ce module encapsule toutes les opérations de base de données liées
aux prix marché. Il sert d'unique point d'accès aux données pour
les couches supérieures, ce qui isole la logique métier des détails
d'implémentation de la persistance.

Cette séparation permet par exemple de changer de système de base
de données sans modifier la couche service, ou d'ajouter des
mécanismes de cache sans toucher au reste du code.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.backend.models.modeles import PrixMarche, Produit, Ville


class PrixRepository:
    """
    Classe d'accès aux données de prix marché.
    
    Toutes les méthodes prennent une session SQLAlchemy en paramètre
    pour permettre la gestion des transactions par les couches
    supérieures. Cette approche est plus flexible que d'instancier
    une session à chaque méthode car elle permet de regrouper
    plusieurs opérations dans une seule transaction si nécessaire.
    """
    
    def lister_tous_les_prix(self, db: Session, limite: int = 100):
        """
        Récupère les prix marché les plus récents jusqu'à une limite
        donnée. Les prix sont triés par date de saisie décroissante
        pour afficher d'abord les plus récents.
        
        Le paramètre limite permet d'éviter de surcharger le système
        en récupérant trop de données d'un coup, ce qui est important
        pour respecter la contrainte de performance temps réel.
        """
        return db.query(PrixMarche).order_by(
            PrixMarche.date_saisie.desc()
        ).limit(limite).all()
    
    def lister_prix_par_ville(self, db: Session, ville_id: int, limite: int = 50):
        """
        Récupère les prix marché pour une ville spécifique.
        Cette méthode est utilisée par le tableau de bord pour
        afficher les prix d'une zone géographique particulière.
        """
        return db.query(PrixMarche).filter(
            PrixMarche.ville_id == ville_id
        ).order_by(PrixMarche.date_saisie.desc()).limit(limite).all()
    
    def lister_prix_par_produit_et_ville(
        self, db: Session, produit_id: int, ville_id: int, jours: int = 30
    ):
        """
        Récupère l'historique des prix d'un produit dans une ville
        sur une période donnée. Cette méthode est utilisée par le
        Fenwick Tree pour calculer les moyennes mobiles.
        """
        date_limite = datetime.now() - timedelta(days=jours)
        return db.query(PrixMarche).filter(
            PrixMarche.produit_id == produit_id,
            PrixMarche.ville_id == ville_id,
            PrixMarche.date_saisie >= date_limite
        ).order_by(PrixMarche.date_saisie.asc()).all()
    
    def lister_produits(self, db: Session):
        """
        Récupère la liste de tous les produits suivis par le système.
        """
        return db.query(Produit).order_by(Produit.nom_fr).all()
    
    def lister_villes(self, db: Session):
        """
        Récupère la liste de toutes les villes pilotes du système.
        """
        return db.query(Ville).order_by(Ville.nom).all()