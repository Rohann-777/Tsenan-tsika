"""
Repository pour l'accès aux données d'alertes dans Tsenan'tsika.

Ce module encapsule les opérations de lecture des alertes stockées
en base de données. Les alertes sont créées automatiquement par le
service de saisie quand le Top-k détecte une variation anormale,
et ce repository permet ensuite de les consulter pour affichage
sur le tableau de bord.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.backend.models.modeles import Alerte


class AlerteRepository:
    """
    Classe d'accès aux données pour les alertes.
    """
    
    def lister_alertes_recentes(self, db: Session, jours: int = 7, limite: int = 20):
        """
        Récupère les alertes les plus récentes sur la période spécifiée.
        
        Le paramètre jours définit la fenêtre temporelle de pertinence
        des alertes affichées, et le paramètre limite contrôle le nombre
        maximum d'alertes retournées pour éviter de surcharger le tableau
        de bord avec trop d'informations. Les alertes sont triées par
        date décroissante pour afficher d'abord les plus récentes.
        """
        date_limite = datetime.now() - timedelta(days=jours)
        return db.query(Alerte).filter(
            Alerte.date >= date_limite
        ).order_by(Alerte.date.desc()).limit(limite).all()
    
    def compter_alertes_actives(self, db: Session, jours: int = 7):
        """
        Compte le nombre total d'alertes actives sur la période donnée.
        
        Ce compteur est affiché en évidence sur le tableau de bord pour
        donner aux analystes une idée rapide du niveau d'activité du
        système d'alertes sans avoir à parcourir la liste complète.
        """
        date_limite = datetime.now() - timedelta(days=jours)
        return db.query(Alerte).filter(
            Alerte.date >= date_limite
        ).count()