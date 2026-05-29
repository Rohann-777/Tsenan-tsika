from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.backend.models.modeles import RapportPrix, PrixMarche, Alerte


class SaisieRepository:
    
    def lister_rapports_recents(self, db: Session, heures: int = 24):
        date_limite = datetime.now() - timedelta(hours=heures)
        return db.query(RapportPrix).filter(
            RapportPrix.date_heure >= date_limite,
            RapportPrix.est_doublon == False
        ).all()
    
    def inserer_rapport(
        self, db: Session, produit_id: int, ville_id: int,
        prix: float, agent_id: int, est_doublon: bool = False
    ):
        nouveau_rapport = RapportPrix(
            produit_id=produit_id,
            ville_id=ville_id,
            prix=prix,
            date_heure=datetime.now(),
            agent_id=agent_id,
            est_doublon=est_doublon
        )
        db.add(nouveau_rapport)
        db.commit()
        db.refresh(nouveau_rapport)
        return nouveau_rapport
    
    def inserer_prix_marche(
        self, db: Session, produit_id: int, ville_id: int,
        prix: float, agent_id: int
    ):
        nouveau_prix = PrixMarche(
            produit_id=produit_id,
            ville_id=ville_id,
            prix=prix,
            date_saisie=datetime.now(),
            agent_id=agent_id
        )
        db.add(nouveau_prix)
        db.commit()
        db.refresh(nouveau_prix)
        return nouveau_prix
    
    def obtenir_prix_moyen_recent(
        self, db: Session, produit_id: int, ville_id: int, jours: int = 7
    ):
        date_limite = datetime.now() - timedelta(days=jours)
        resultat = db.query(func.avg(PrixMarche.prix)).filter(
            PrixMarche.produit_id == produit_id,
            PrixMarche.ville_id == ville_id,
            PrixMarche.date_saisie >= date_limite
        ).scalar()
        
        return float(resultat) if resultat else None
    
    def creer_alerte(self, db: Session, produit_id: int, ville_id: int):
        nouvelle_alerte = Alerte(
            produit_id=produit_id,
            ville_id=ville_id,
            date=datetime.now()
        )
        db.add(nouvelle_alerte)
        db.commit()
        db.refresh(nouvelle_alerte)
        return nouvelle_alerte