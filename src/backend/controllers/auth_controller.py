from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.backend.auth.auth_service import AuthService


class AuthController:
    
    def __init__(self):
        self.service = AuthService()
    
    def se_connecter(self, db: Session, email: str, mot_de_passe: str):
        resultat = self.service.authentifier(db, email, mot_de_passe)
        
        if resultat is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect"
            )
        
        if resultat.get("compte_desactive"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Ce compte a été désactivé. Veuillez contacter l'administrateur du système."
            )
        
        return resultat
    
    def s_inscrire(
        self, db: Session, nom: str, prenoms: str,
        email: str, mot_de_passe: str
    ):
        resultat = self.service.inscrire_citoyen(
            db, nom, prenoms, email, mot_de_passe
        )
        
        if resultat is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un utilisateur avec cet email existe déjà"
            )
        
        return resultat