from typing import List
from pydantic import BaseModel, Field


class ItineraireRequete(BaseModel):
    ville_depart_id: int = Field(..., description="Identifiant de la ville de départ")
    ville_destination_id: int = Field(..., description="Identifiant de la ville de destination")


class EtapeItineraire(BaseModel):
    ville_id: int
    nom: str
    region: str


class ItineraireReponse(BaseModel):
    chemin: List[EtapeItineraire]
    cout_total: float
    atteignable: bool
    nombre_etapes: int