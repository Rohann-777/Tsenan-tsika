from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SaisiePrixRequete(BaseModel):
    produit_id: int = Field(..., gt=0, description="Identifiant du produit")
    ville_id: int = Field(..., gt=0, description="Identifiant de la ville")
    prix: float = Field(..., gt=0, description="Prix observé en Ariary")
    agent_id: int = Field(..., gt=0, description="Identifiant de l'agent qui soumet le prix")


class SaisiePrixReponse(BaseModel):
    succes: bool
    message: str
    rapport_id: Optional[int] = None
    prix_marche_id: Optional[int] = None
    doublon_detecte: bool = False
    alerte_declenchee: bool = False
    variation_pourcent: Optional[float] = None