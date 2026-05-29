from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.backend.repositories.prix_repository import PrixRepository
from src.backend.algorithms.fenwick_tree import FenwickTree


class PrixService:
    
    def __init__(self):
        self.repository = PrixRepository()
    
    def obtenir_prix_recents(self, db: Session, limite: int = 100):
        return self.repository.lister_tous_les_prix(db, limite)
    
    def obtenir_prix_par_ville(self, db: Session, ville_id: int):
        return self.repository.lister_prix_par_ville(db, ville_id, limite=50)
    
    def calculer_prix_moyen(
        self, db: Session, produit_id: int, ville_id: int, jours: int = 7
    ):
        historique = self.repository.lister_prix_par_produit_et_ville(
            db, produit_id, ville_id, jours
        )
        
        if not historique:
            return None
        
        fenwick = FenwickTree(len(historique))
        for index, prix_marche in enumerate(historique):
            fenwick.mettre_a_jour(index, prix_marche.prix)
        
        prix_moyen = fenwick.calculer_moyenne(0, len(historique) - 1)
        
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