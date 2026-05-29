from sqlalchemy.orm import Session
from src.backend.services.alerte_service import AlerteService


class AlerteController:
    
    def __init__(self):
        self.service = AlerteService()
    
    def obtenir_tableau_bord(self, db: Session):
        return self.service.obtenir_tableau_bord(db)