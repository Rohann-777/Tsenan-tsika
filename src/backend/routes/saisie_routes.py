from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.controllers.saisie_controller import SaisieController
from src.backend.schemas.saisie_schemas import (
    SaisiePrixRequete, SaisiePrixReponse
)
from src.backend.auth.dependances import verifier_role
from src.backend.models.modeles import Utilisateur


router = APIRouter(prefix="/api/saisie", tags=["Saisie"])
controller = SaisieController()


@router.post("/prix", response_model=SaisiePrixReponse)
def saisir_prix(
    requete: SaisiePrixRequete,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(verifier_role(["agent"]))
):
    if requete.agent_id != utilisateur.id:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez soumettre des prix qu'en votre propre nom"
        )
    
    return controller.saisir_prix(
        db,
        requete.produit_id,
        requete.ville_id,
        requete.prix,
        requete.agent_id
    )