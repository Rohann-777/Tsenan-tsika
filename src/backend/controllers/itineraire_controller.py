from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.backend.services.itineraire_service import ItineraireService


class ItineraireController:
    
    def __init__(self):
        self.service = ItineraireService()
    
    def calculer_itineraire(
        self, db: Session, ville_depart_id: int, ville_destination_id: int
    ):
        resultat = self.service.calculer_itineraire(
            db, ville_depart_id, ville_destination_id
        )
        
        if "erreur" in resultat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultat["erreur"]
            )
        
        if not resultat["atteignable"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aucun itinéraire trouvé entre ces deux villes"
            )
        
        return resultat