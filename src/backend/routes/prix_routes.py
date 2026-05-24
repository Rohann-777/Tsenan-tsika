"""
Routes HTTP pour les prix dans Tsenan'tsika.
"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.controllers.prix_controller import PrixController
from src.backend.schemas.prix_schemas import (
    PrixMarcheReponse, PrixMoyenReponse, ProduitReponse, VilleReponse
)
from src.backend.auth.dependances import obtenir_utilisateur_actuel
from src.backend.models.modeles import Utilisateur


router = APIRouter(prefix="/api/prix", tags=["Prix"])
controller = PrixController()


@router.get("/recents", response_model=List[PrixMarcheReponse])
def lister_prix_recents(
    limite: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(obtenir_utilisateur_actuel)
):
    return controller.lister_prix_recents(db, limite)


@router.get("/ville/{ville_id}", response_model=List[PrixMarcheReponse])
def lister_prix_par_ville(
    ville_id: int,
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(obtenir_utilisateur_actuel)
):
    return controller.lister_prix_par_ville(db, ville_id)


@router.get("/moyenne", response_model=PrixMoyenReponse)
def calculer_prix_moyen(
    produit_id: int = Query(...),
    ville_id: int = Query(...),
    jours: int = Query(7, ge=1, le=90),
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(obtenir_utilisateur_actuel)
):
    return controller.calculer_moyenne(db, produit_id, ville_id, jours)


@router.get("/produits", response_model=List[ProduitReponse])
def lister_produits(
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(obtenir_utilisateur_actuel)
):
    return controller.lister_produits(db)


@router.get("/villes", response_model=List[VilleReponse])
def lister_villes(
    db: Session = Depends(get_db),
    utilisateur: Utilisateur = Depends(obtenir_utilisateur_actuel)
):
    return controller.lister_villes(db)