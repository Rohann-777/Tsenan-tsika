"""
Controller pour les endpoints du tableau de bord dans Tsenan'tsika.

Ce module gère les requêtes HTTP de consultation du tableau de bord
qui agrège les alertes et le classement Top-k actuel du système.
"""

from sqlalchemy.orm import Session
from src.backend.services.alerte_service import AlerteService


class AlerteController:
    """
    Controller pour les opérations de consultation du tableau de bord.
    """
    
    def __init__(self):
        """
        Initialise le controller avec une instance du service.
        """
        self.service = AlerteService()
    
    def obtenir_tableau_bord(self, db: Session):
        """
        Endpoint pour récupérer toutes les informations du tableau de bord.
        
        Cette méthode retourne une vue agrégée incluant les alertes
        récentes et le classement Top-k actuel des produits avec les
        plus fortes hausses de prix.
        """
        return self.service.obtenir_tableau_bord(db)