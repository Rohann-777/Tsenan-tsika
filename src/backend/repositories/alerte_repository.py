from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.backend.models.modeles import Alerte


class AlerteRepository:
    
    def lister_alertes_recentes(self, db: Session, jours: int = 7, limite: int = 20):
        date_limite = datetime.now() - timedelta(days=jours)
        return db.query(Alerte).filter(
            Alerte.date >= date_limite
        ).order_by(Alerte.date.desc()).limit(limite).all()
    
    def compter_alertes_actives(self, db: Session, jours: int = 7):
        date_limite = datetime.now() - timedelta(days=jours)
        return db.query(Alerte).filter(
            Alerte.date >= date_limite
        ).count()