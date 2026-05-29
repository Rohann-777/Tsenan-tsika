from sqlalchemy.orm import Session
from src.backend.services.export_service import ExportService


class ExportController:

    def __init__(self):
        self.service = ExportService()

    def generer_rapport_hebdomadaire(self, db: Session) -> bytes:
        return self.service.generer_rapport_hebdomadaire(db)