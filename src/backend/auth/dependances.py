"""
Dépendances FastAPI pour la protection des endpoints de Tsenan'tsika.

Ce module fournit les fonctions qui peuvent être utilisées comme
dépendances FastAPI pour protéger les endpoints. Ces fonctions
vérifient automatiquement la présence et la validité du token JWT,
puis elles vérifient que l'utilisateur a bien le rôle requis pour
accéder à l'endpoint.

L'utilisation du système de dépendances de FastAPI rend cette
protection déclarative et très lisible dans le code des routes.
"""

from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.auth.jwt_service import JwtService
from src.backend.models.modeles import Utilisateur


# Schéma d'authentification OAuth2 qui définit comment le token doit
# être présenté dans les requêtes HTTP. Le tokenUrl pointe vers
# l'endpoint de connexion où les clients peuvent obtenir un token.
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
    
    return utilisateur


def verifier_role(roles_autorises: List[str]):
    """
    Factory de dépendance qui crée un vérificateur de rôle spécifique.
    
    Cette fonction retourne une autre fonction qui peut être utilisée
    comme dépendance FastAPI. La fonction retournée vérifie que
    l'utilisateur connecté possède l'un des rôles autorisés. Si ce
    n'est pas le cas, elle lève une exception HTTP 403 qui indique
    que l'utilisateur est authentifié mais n'a pas les permissions
    nécessaires pour cette action.
    
    Cette approche par factory permet de définir des dépendances
    spécifiques pour chaque endpoint selon ses exigences de rôles.
    Par exemple, un endpoint de saisie de prix utilisera verifier_role
    avec la liste contenant uniquement "agent", tandis qu'un endpoint
    de gestion des utilisateurs utilisera la liste contenant uniquement
    "administrateur".
    """
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