from datetime import datetime
from typing import List
from pydantic import BaseModel


class AlerteDetaillee(BaseModel):
    id: int
    date: datetime
    produit_id: int
    produit_nom: str
    ville_id: int
    ville_nom: str
    
    class Config:
        from_attributes = True


class EntreeTopK(BaseModel):
    produit_id: int
    produit_nom: str
    variation_pourcent: float
    rang: int


class TableauBordReponse(BaseModel):
    nombre_alertes_actives: int
    alertes_recentes: List[AlerteDetaillee]
    top_5_hausses: List[EntreeTopK]