"""
Routes HTTP pour l'authentification dans Tsenan'tsika.
"""

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.controllers.auth_controller import AuthController
from src.backend.schemas.auth_schemas import (
    InscriptionRequete, AuthReponse, UtilisateurReponse
)
from src.backend.auth.dependances import obtenir_utilisateur_actuel
from src.backend.models.modeles import Utilisateur


router = APIRouter(prefix="/api/auth", tags=["Authentification"])
controller = AuthController()


@router.post("/connexion", response_model=AuthReponse)
def se_connecter(
    formulaire: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Connecte un utilisateur existant avec son email et mot de passe.
    
    On utilise OAuth2PasswordRequestForm qui est le standard FastAPI
    pour les formulaires de connexion. Ce schéma utilise username
    et password comme noms de champs, mais nous traitons username
    comme l'email dans notre logique métier.
    """
    return controller.se_connecter(
        db, formulaire.username, formulaire.password
    )


@router.post("/inscription", response_model=AuthReponse)
def s_inscrire(
    requete: InscriptionRequete,
    db: Session = Depends(get_db)
):
    """
    Inscrit un nouveau citoyen dans le système.
    
    Cet endpoint est volontairement limité au rôle citoyen.
    Les autres rôles doivent être créés par un administrateur.
    """
    return controller.s_inscrire(
        db, requete.nom, requete.prenoms,
        requete.email, requete.mot_de_passe
    )


@router.get("/moi", response_model=UtilisateurReponse)
def obtenir_mon_profil(
    utilisateur: Utilisateur = Depends(obtenir_utilisateur_actuel)
):
    """
    Retourne les informations de l'utilisateur actuellement connecté.
    
    Cet endpoint est utile pour le frontend qui peut vérifier si
    l'utilisateur est toujours authentifié et récupérer ses informations
    après un rafraîchissement de page.
    """
    return utilisateur