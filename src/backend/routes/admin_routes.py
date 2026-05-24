"""
Routes HTTP pour les endpoints d'administration de Tsenan'tsika.

Toutes ces routes sont protégées par la dépendance verifier_role qui
n'autorise leur accès qu'aux utilisateurs ayant le rôle administrateur.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.controllers.admin_controller import AdminController
from src.backend.schemas.admin_schemas import (
    UtilisateurCreer, UtilisateurModifier, UtilisateurAdmin, RapportDoublon
)
from src.backend.auth.dependances import verifier_role
from src.backend.models.modeles import Utilisateur


router = APIRouter(prefix="/api/admin", tags=["Administration"])
controller = AdminController()


@router.get("/utilisateurs", response_model=List[UtilisateurAdmin])
def lister_utilisateurs(
    role: Optional[str] = Query(None, description="Filtrer par rôle"),
    db: Session = Depends(get_db),
    admin: Utilisateur = Depends(verifier_role(["administrateur"]))
):
    """
    Récupère la liste des utilisateurs gérables par l'administrateur.
    """
    return controller.lister_utilisateurs(db, role)


@router.post("/utilisateurs", response_model=UtilisateurAdmin)
def creer_utilisateur(
    requete: UtilisateurCreer,
    db: Session = Depends(get_db),
    admin: Utilisateur = Depends(verifier_role(["administrateur"]))
):
    """
    Crée un nouveau compte utilisateur de type agent, analyste ou citoyen.
    """
    return controller.creer_utilisateur(db, requete.dict())


@router.put("/utilisateurs/{utilisateur_id}", response_model=UtilisateurAdmin)
def modifier_utilisateur(
    utilisateur_id: int,
    requete: UtilisateurModifier,
    db: Session = Depends(get_db),
    admin: Utilisateur = Depends(verifier_role(["administrateur"]))
):
    """
    Modifie les informations d'un utilisateur existant.
    """
    return controller.modifier_utilisateur(db, utilisateur_id, requete.dict(exclude_unset=True))


@router.patch("/utilisateurs/{utilisateur_id}/statut")
def basculer_statut_compte(
    utilisateur_id: int,
    db: Session = Depends(get_db),
    admin: Utilisateur = Depends(verifier_role(["administrateur"]))
):
    """
    Active ou désactive un compte utilisateur selon son état actuel.
    """
    return controller.basculer_statut(db, utilisateur_id)


@router.get("/doublons", response_model=List[RapportDoublon])
def lister_doublons(
    jours: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    admin: Utilisateur = Depends(verifier_role(["administrateur"]))
):
    """
    Récupère la liste des rapports détectés comme doublons sur la période.
    """
    return controller.lister_doublons(db, jours)