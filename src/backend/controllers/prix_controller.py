from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.backend.services.prix_service import PrixService


class PrixController:
    
    def __init__(self):
        self.service = PrixService()
    
    def lister_prix_recents(self, db: Session, limite: int = 100):
        prix = self.service.obtenir_prix_recents(db, limite)
        return prix
    
    def lister_prix_par_ville(self, db: Session, ville_id: int):
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
        return self.service.obtenir_produits(db)
    
    def lister_villes(self, db: Session):
        return self.service.obtenir_villes(db)