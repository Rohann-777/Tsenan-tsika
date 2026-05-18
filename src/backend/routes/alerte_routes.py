"""
Routes HTTP pour le tableau de bord des alertes dans Tsenan'tsika.

Ce module définit les URL accessibles depuis le frontend pour consulter
les alertes et le classement Top-k actuel. Ces endpoints sont accessibles
publiquement car ils correspondent au tableau de bord consultable en
lecture seule par les citoyens, conformément aux exigences du cahier
des charges.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.controllers.alerte_controller import AlerteController
from src.backend.schemas.alerte_schemas import TableauBordReponse


router = APIRouter(prefix="/api/alertes", tags=["Alertes"])

controller = AlerteController()


@router.get("/tableau-bord", response_model=TableauBordReponse)
def obtenir_tableau_bord(db: Session = Depends(get_db)):
    """
    Récupère la vue complète du tableau de bord incluant les alertes
    récentes et le classement Top-k des produits avec les plus fortes
    hausses de prix.
    
    Cette route est consultable publiquement par les citoyens en lecture
    seule, conformément aux fonctionnalités F2 du cahier des charges.
    """
    return controller.obtenir_tableau_bord(db)