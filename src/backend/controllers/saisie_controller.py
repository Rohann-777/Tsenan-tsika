"""
Controller pour les endpoints de saisie de prix dans Tsenan'tsika.

Ce module gère les requêtes HTTP liées à la soumission de nouveaux
prix par les agents de collecte.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.backend.services.saisie_service import SaisieService


class SaisieController:
    """
    Controller pour les opérations de saisie de prix.
    """
    
    def __init__(self):
        """
        Initialise le controller avec une instance du service.
        """
        self.service = SaisieService()
    
    def saisir_prix(
        self, db: Session, produit_id: int, ville_id: int,
        prix: float, agent_id: int
    ):
        """
        Endpoint pour la saisie d'un nouveau prix par un agent.
        
        Cette méthode coordonne le traitement complet incluant la
        détection de doublons par Rabin-Karp, l'insertion en base,
        la mise à jour du Top-k et le déclenchement éventuel d'alerte.
        """
        resultat = self.service.saisir_prix(
            db, produit_id, ville_id, prix, agent_id
        )
        
        # Si le produit ou la ville n'existe pas, on retourne une erreur HTTP
        if not resultat["succes"] and "inexistant" in resultat["message"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultat["message"]
            )
        
        # Si un doublon est détecté, on retourne le résultat avec un code 200
        # car ce n'est pas une erreur technique mais un état métier valide
        return resultat