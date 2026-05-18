"""
Controller pour les endpoints liés aux itinéraires dans Tsenan'tsika.

Ce module fait le lien entre les routes HTTP et le service métier
pour le calcul des itinéraires d'approvisionnement optimaux.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.backend.services.itineraire_service import ItineraireService


class ItineraireController:
    """
    Controller pour les opérations liées aux itinéraires.
    """
    
    def __init__(self):
        """
        Initialise le controller avec une instance du service.
        """
        self.service = ItineraireService()
    
    def calculer_itineraire(
        self, db: Session, ville_depart_id: int, ville_destination_id: int
    ):
        """
        Endpoint pour calculer l'itinéraire optimal entre deux villes.
        
        Lève une exception HTTP 400 si l'une des villes n'existe pas,
        et une exception HTTP 404 si aucun chemin n'existe entre les
        deux villes dans le graphe.
        """
        resultat = self.service.calculer_itineraire(
            db, ville_depart_id, ville_destination_id
        )
        
        # Vérification de la présence d'une erreur métier
        if "erreur" in resultat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultat["erreur"]
            )
        
        # Vérification de l'atteignabilité de la destination
        if not resultat["atteignable"]:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Aucun itinéraire trouvé entre ces deux villes"
            )
        
        return resultat