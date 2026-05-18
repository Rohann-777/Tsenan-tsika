"""
Controller pour les endpoints liés aux prix dans Tsenan'tsika.

Ce module orchestre le traitement des requêtes HTTP en faisant le
lien entre les routes définies par FastAPI et le service métier
qui contient la logique applicative.

Le controller est responsable de l'extraction des paramètres de
la requête, de la délégation au service approprié, et de la
construction de la réponse HTTP avec les bons codes de statut.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.backend.services.prix_service import PrixService


class PrixController:
    """
    Controller pour les opérations liées aux prix marché.
    """
    
    def __init__(self):
        """
        Initialise le controller avec une instance du service.
        """
        self.service = PrixService()
    
    def lister_prix_recents(self, db: Session, limite: int = 100):
        """
        Endpoint pour récupérer les prix les plus récents.
        """
        prix = self.service.obtenir_prix_recents(db, limite)
        return prix
    
    def lister_prix_par_ville(self, db: Session, ville_id: int):
        """
        Endpoint pour récupérer les prix d'une ville spécifique.
        Lève une exception HTTP 404 si la ville n'existe pas.
        """
        prix = self.service.obtenir_prix_par_ville(db, ville_id)
        if not prix:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Aucun prix trouvé pour la ville {ville_id}"
            )
        return prix
    
    def calculer_moyenne(
        self, db: Session, produit_id: int, ville_id: int, jours: int = 7
    ):
        """
        Endpoint pour calculer le prix moyen d'un produit dans une
        ville sur une période donnée via le Fenwick Tree.
        """
        resultat = self.service.calculer_prix_moyen(
            db, produit_id, ville_id, jours
        )
        if resultat is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aucune donnée disponible pour ce produit et cette ville"
            )
        return resultat
    
    def lister_produits(self, db: Session):
        """
        Endpoint pour lister tous les produits suivis.
        """
        return self.service.obtenir_produits(db)
    
    def lister_villes(self, db: Session):
        """
        Endpoint pour lister toutes les villes pilotes.
        """
        return self.service.obtenir_villes(db)