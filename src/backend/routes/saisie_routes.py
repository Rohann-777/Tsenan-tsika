"""
Routes HTTP pour la saisie de prix dans Tsenan'tsika.

Ce module définit les URL accessibles par les agents de collecte
depuis leur application mobile pour soumettre de nouveaux prix
au système central.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.controllers.saisie_controller import SaisieController
from src.backend.schemas.saisie_schemas import (
    SaisiePrixRequete, SaisiePrixReponse
)


router = APIRouter(prefix="/api/saisie", tags=["Saisie"])

controller = SaisieController()


@router.post("/prix", response_model=SaisiePrixReponse)
def saisir_prix(
    requete: SaisiePrixRequete,
    db: Session = Depends(get_db)
):
    """
    Soumet un nouveau prix observé sur un marché par un agent de collecte.
    
    Le pipeline de traitement effectue automatiquement les opérations
    suivantes en cascade. D'abord la vérification de doublon par Rabin-Karp
    sur les rapports des dernières vingt-quatre heures. Ensuite l'insertion
    du rapport en base avec un flag indiquant s'il s'agit d'un doublon.
    Puis si le rapport est valide, l'insertion d'un prix marché correspondant.
    Et enfin la mise à jour du Top-k qui peut déclencher une alerte si la
    variation par rapport à la moyenne récente dépasse vingt pour cent.
    
    La réponse indique précisément ce qui s'est passé pendant le traitement,
    ce qui permet au frontend d'afficher un message approprié à l'agent.
    """
    return controller.saisir_prix(
        db,
        requete.produit_id,
        requete.ville_id,
        requete.prix,
        requete.agent_id
    )