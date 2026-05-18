"""
Routes HTTP pour les endpoints liés aux itinéraires dans Tsenan'tsika.

Ce module définit les URL accessibles par le frontend pour calculer
les itinéraires d'approvisionnement optimaux entre les villes du
réseau de Tsenan'tsika.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.controllers.itineraire_controller import ItineraireController
from src.backend.schemas.itineraire_schemas import (
    ItineraireRequete, ItineraireReponse
)


# Création du routeur avec un préfixe et un tag pour l'organisation
router = APIRouter(prefix="/api/itineraire", tags=["Itinéraire"])

# Instance unique du controller utilisée par toutes les routes
controller = ItineraireController()


@router.post("/calculer", response_model=ItineraireReponse)
def calculer_itineraire(
    requete: ItineraireRequete,
    db: Session = Depends(get_db)
):
    """
    Calcule l'itinéraire d'approvisionnement optimal entre deux villes
    en utilisant l'algorithme de Dijkstra sur le graphe routier malgache.
    
    Cette route est utilisée par les analystes du ministère pour
    déterminer la route la moins coûteuse permettant d'acheminer
    un produit depuis une ville productrice vers une ville en pénurie.
    """
    return controller.calculer_itineraire(
        db, requete.ville_depart_id, requete.ville_destination_id
    )