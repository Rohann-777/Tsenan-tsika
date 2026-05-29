from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class ProduitReponse(BaseModel):
    id: int
    nom_fr: str
    nom_mg: str
    unite: str
    categorie: str
    
    class Config:
        from_attributes = True


class VilleReponse(BaseModel):
    id: int
    nom: str
    region: str
    latitude: float
    longitude: float
    
    class Config:
        from_attributes = True


class PrixMarcheReponse(BaseModel):
    id: int
    prix: float
    date_saisie: datetime
    produit: ProduitReponse
    ville: VilleReponse
    
    class Config:
        from_attributes = True


class PrixMoyenReponse(BaseModel):
    produit_id: int
    produit_nom: str
    ville_id: int
    ville_nom: str
    prix_moyen: float
    nombre_releves: int
    periode_debut: datetime
    periode_fin: datetime