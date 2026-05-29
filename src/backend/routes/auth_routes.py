from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.controllers.auth_controller import AuthController
from src.backend.schemas.auth_schemas import (
    InscriptionRequete, AuthReponse, UtilisateurReponse
)
from src.backend.auth.dependances import obtenir_utilisateur_actuel
from src.backend.models.modeles import Utilisateur, Ville


router = APIRouter(prefix="/api/auth", tags=["Authentification"])
controller = AuthController()


@router.post("/connexion", response_model=AuthReponse)
def se_connecter(
    formulaire: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return controller.se_connecter(
        db, formulaire.username, formulaire.password
    )


@router.post("/inscription", response_model=AuthReponse)
def s_inscrire(
    requete: InscriptionRequete,
    db: Session = Depends(get_db)
):
    return controller.s_inscrire(
        db, requete.nom, requete.prenoms,
        requete.email, requete.mot_de_passe
    )


@router.get("/moi")
def obtenir_moi(utilisateur: Utilisateur = Depends(obtenir_utilisateur_actuel), db: Session = Depends(get_db)):
    ville_assignee_nom = None
    if utilisateur.ville_assignee_id:
        ville = db.query(Ville).filter(
            Ville.id == utilisateur.ville_assignee_id
        ).first()
        if ville:
            ville_assignee_nom = ville.nom
    
    return {
        "id": utilisateur.id,
        "nom": utilisateur.nom,
        "prenoms": utilisateur.prenoms,
        "email": utilisateur.email,
        "role": utilisateur.role,
        "ville_assignee_id": utilisateur.ville_assignee_id,
        "ville_assignee_nom": ville_assignee_nom
    }