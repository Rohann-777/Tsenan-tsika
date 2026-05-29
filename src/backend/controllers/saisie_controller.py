from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.backend.services.saisie_service import SaisieService


class SaisieController:
    
    def __init__(self):
        self.service = SaisieService()
    
    def saisir_prix(
        self, db: Session, produit_id: int, ville_id: int,
        prix: float, agent_id: int
    ):
        resultat = self.service.saisir_prix(
            db, produit_id, ville_id, prix, agent_id
        )
        
        if not resultat["succes"] and "inexistant" in resultat["message"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultat["message"]
            )
        
        return resultat