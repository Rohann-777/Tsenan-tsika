from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.backend.models.modeles import Utilisateur, RapportPrix, Ville, Produit


class AdminRepository:
    
    def lister_utilisateurs(self, db: Session, role_filtre: str = None):
        requete = db.query(Utilisateur).filter(
            Utilisateur.role != "administrateur"
        )
        
        if role_filtre:
            requete = requete.filter(Utilisateur.role == role_filtre)
        
        return requete.order_by(Utilisateur.role, Utilisateur.nom).all()
    
    def obtenir_utilisateur_par_id(self, db: Session, utilisateur_id: int):
        return db.query(Utilisateur).filter(
            Utilisateur.id == utilisateur_id,
            Utilisateur.role != "administrateur"
        ).first()
    
    def email_existe(self, db: Session, email: str, exclure_id: int = None):
        requete = db.query(Utilisateur).filter(Utilisateur.email == email)
        if exclure_id:
            requete = requete.filter(Utilisateur.id != exclure_id)
        return requete.first() is not None
    
    def creer_utilisateur(self, db: Session, donnees: dict):
        nouvel_utilisateur = Utilisateur(**donnees)
        db.add(nouvel_utilisateur)
        db.commit()
        db.refresh(nouvel_utilisateur)
        return nouvel_utilisateur
    
    def modifier_utilisateur(self, db: Session, utilisateur: Utilisateur, modifications: dict):
        for cle, valeur in modifications.items():
            if valeur is not None:
                setattr(utilisateur, cle, valeur)
        db.commit()
        db.refresh(utilisateur)
        return utilisateur
    
    def lister_doublons(self, db: Session, jours: int = 30):
        date_limite = datetime.now() - timedelta(days=jours)
        return db.query(RapportPrix).filter(
            RapportPrix.est_doublon == True,
            RapportPrix.date_heure >= date_limite
        ).order_by(RapportPrix.date_heure.desc()).all()