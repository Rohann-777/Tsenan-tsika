"""
Routes HTTP pour les endpoints liés aux prix dans Tsenan'tsika.

Ce module définit les URL accessibles par les clients HTTP comme
le frontend React. Chaque route est associée à un controller qui
traite la logique de la requête.

Les routes utilisent les annotations de type Python pour bénéficier
de la validation automatique des paramètres et de la génération
de la documentation Swagger.
"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.backend.config.database import get_db
from src.backend.controllers.prix_controller import PrixController
from src.backend.schemas.prix_schemas import (
    PrixMarcheReponse, PrixMoyenReponse, ProduitReponse, VilleReponse
)


# Création du routeur avec un préfixe et un tag pour l'organisation
router = APIRouter(prefix="/api/prix", tags=["Prix"])

# Instance unique du controller utilisée par toutes les routes
controller = PrixController()


@router.get("/recents", response_model=List[PrixMarcheReponse])
def lister_prix_recents(
    limite: int = Query(100, ge=1, le=500, description="Nombre maximum de prix à retourner"),
    db: Session = Depends(get_db)
):
    """
    Récupère les prix marché les plus récents enregistrés dans le système.
    
    Cette route est accessible publiquement sans authentification car
    elle permet aux citoyens de consulter les prix actuels du marché.
    """
    return controller.lister_prix_recents(db, limite)


@router.get("/ville/{ville_id}", response_model=List[PrixMarcheReponse])
def lister_prix_par_ville(
    ville_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère les prix marché pour une ville spécifique identifiée
    par son identifiant unique.
    """
    return controller.lister_prix_par_ville(db, ville_id)


@router.get("/moyenne", response_model=PrixMoyenReponse)
def calculer_prix_moyen(
    produit_id: int = Query(..., description="Identifiant du produit"),
    ville_id: int = Query(..., description="Identifiant de la ville"),
    jours: int = Query(7, ge=1, le=90, description="Nombre de jours à analyser"),
    db: Session = Depends(get_db)
):
    """
    Calcule le prix moyen d'un produit dans une ville sur une période
    donnée en utilisant l'algorithme Fenwick Tree pour des calculs
    rapides sur intervalles.
    """
    return controller.calculer_moyenne(db, produit_id, ville_id, jours)


@router.get("/produits", response_model=List[ProduitReponse])
def lister_produits(db: Session = Depends(get_db)):
    """
    Liste tous les produits de première nécessité suivis par le système.
    """
    return controller.lister_produits(db)


@router.get("/villes", response_model=List[VilleReponse])
def lister_villes(db: Session = Depends(get_db)):
    """
    Liste toutes les villes pilotes couvertes par le système.
    """
    return controller.lister_villes(db)