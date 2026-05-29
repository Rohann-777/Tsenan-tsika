from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.controllers.itineraire_controller import ItineraireController
from src.backend.schemas.itineraire_schemas import (
    ItineraireRequete, ItineraireReponse
)
from src.backend.auth.dependances import verifier_role
from src.backend.models.modeles import Utilisateur


router = APIRouter(prefix="/api/itineraire", tags=["Itinéraire"])
controller = ItineraireController()


@router.post("/calculer", response_model=ItineraireReponse)
def calculer_itineraire(
    requete: ItineraireRequete,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(verifier_role(["analyste", "administrateur"]))
):
    return controller.calculer_itineraire(
        db, requete.ville_depart_id, requete.ville_destination_id
    )