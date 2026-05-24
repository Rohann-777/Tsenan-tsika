"""
Routes HTTP pour les alertes dans Tsenan'tsika.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.controllers.alerte_controller import AlerteController
from src.backend.schemas.alerte_schemas import TableauBordReponse
from src.backend.auth.dependances import obtenir_utilisateur_actuel
from src.backend.models.modeles import Utilisateur


router = APIRouter(prefix="/api/alertes", tags=["Alertes"])
controller = AlerteController()


@router.get("/tableau-bord", response_model=TableauBordReponse)
def obtenir_tableau_bord(
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(obtenir_utilisateur_actuel)
):
    return controller.obtenir_tableau_bord(db)