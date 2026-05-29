from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.auth.jwt_service import JwtService
from src.backend.models.modeles import Utilisateur


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/connexion")

jwt_service = JwtService()


def obtenir_utilisateur_actuel(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Utilisateur:
    
    exception_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants invalides ou token expiré",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    donnees_token = jwt_service.verifier_token(token)
    
    if donnees_token is None:
        raise exception_credentials
    
    utilisateur_id = donnees_token.get("sub")
    
    if utilisateur_id is None:
        raise exception_credentials
    
    utilisateur = db.query(Utilisateur).filter(
        Utilisateur.id == int(utilisateur_id)
    ).first()
    
    if utilisateur is None:
        print("DEBUG: Aucun utilisateur trouvé avec cet ID")
        raise exception_credentials
    
    if not utilisateur.statut_compte:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Votre compte a été désactivé. Veuillez vous déconnecter et contacter l'administrateur."
        )
    
    return utilisateur


def verifier_role(roles_autorises: List[str]):
    def verificateur(
        utilisateur: Utilisateur = Depends(obtenir_utilisateur_actuel)
    ) -> Utilisateur:
        if utilisateur.role not in roles_autorises:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Accès refusé. Cette action requiert l'un des rôles suivants : {', '.join(roles_autorises)}"
            )
        return utilisateur
    
    return verificateur