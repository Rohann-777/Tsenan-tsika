import bcrypt
from sqlalchemy.orm import Session
from src.backend.models.modeles import Utilisateur, Ville
from src.backend.auth.jwt_service import JwtService


class AuthService:
    def __init__(self):
        self.jwt_service = JwtService()
    
    def verifier_mot_de_passe(self, mot_de_passe_clair: str, hachage: str) -> bool:
        return bcrypt.checkpw(
            mot_de_passe_clair.encode('utf-8'),
            hachage.encode('utf-8')
        )
    
    def hacher_mot_de_passe(self, mot_de_passe_clair: str) -> str:
        sel = bcrypt.gensalt()
        hachage = bcrypt.hashpw(mot_de_passe_clair.encode('utf-8'), sel)
        return hachage.decode('utf-8')
    
    def authentifier(self, db: Session, email: str, mot_de_passe: str):
        utilisateur = db.query(Utilisateur).filter(
            Utilisateur.email == email
        ).first()
        
        if not utilisateur:
            return None
        
        if not self.verifier_mot_de_passe(mot_de_passe, utilisateur.mot_de_passe):
            return None
        
        if not utilisateur.statut_compte:
            return {"compte_desactive": True}
        
        token = self.jwt_service.creer_token({
            "sub": str(utilisateur.id),
            "email": utilisateur.email,
            "role": utilisateur.role
        })
        
        ville_assignee_nom = None
        if utilisateur.ville_assignee_id:
            ville = db.query(Ville).filter(
                Ville.id == utilisateur.ville_assignee_id
            ).first()
            if ville:
                ville_assignee_nom = ville.nom
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "utilisateur": {
                "id": utilisateur.id,
                "email": utilisateur.email,
                "nom": utilisateur.nom,
                "prenoms": utilisateur.prenoms,
                "role": utilisateur.role,
                "ville_assignee_id": utilisateur.ville_assignee_id,
                "ville_assignee_nom": ville_assignee_nom
            }
        }
    
    def inscrire_citoyen(
        self, db: Session, nom: str, prenoms: str,
        email: str, mot_de_passe: str
    ):
        utilisateur_existant = db.query(Utilisateur).filter(
            Utilisateur.email == email
        ).first()
        
        if utilisateur_existant:
            return None
        
        mot_de_passe_hache = self.hacher_mot_de_passe(mot_de_passe)
        
        nouveau_utilisateur = Utilisateur(
            nom=nom,
            prenoms=prenoms,
            email=email,
            mot_de_passe=mot_de_passe_hache,
            role="citoyen"
        )
        
        db.add(nouveau_utilisateur)
        db.commit()
        db.refresh(nouveau_utilisateur)
        
        token = self.jwt_service.creer_token({
            "sub": str(nouveau_utilisateur.id),
            "email": nouveau_utilisateur.email,
            "role": nouveau_utilisateur.role
        })
        
        return {
            "access_token": token,
            "token_type": "Bearer",
            "utilisateur": {
                "id": nouveau_utilisateur.id,
                "email": nouveau_utilisateur.email,
                "nom": nouveau_utilisateur.nom,
                "prenoms": nouveau_utilisateur.prenoms,
                "role": nouveau_utilisateur.role
            }
        }