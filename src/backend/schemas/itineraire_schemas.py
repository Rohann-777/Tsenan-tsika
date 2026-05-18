"""
Schémas Pydantic pour les calculs d'itinéraires dans Tsenan'tsika.

Ces schémas définissent la structure des données échangées entre
le frontend et le backend pour la fonctionnalité de calcul du
chemin d'approvisionnement optimal entre deux villes via Dijkstra.

La séparation entre schéma de requête et schéma de réponse permet
de valider précisément les données entrantes tout en contrôlant
le format des données sortantes pour le frontend.
"""

from typing import List
from pydantic import BaseModel, Field


class ItineraireRequete(BaseModel):
    """
    Schéma de requête pour le calcul d'itinéraire.
    
    Le frontend envoie les identifiants des villes de départ et de
    destination, et le backend retourne le chemin optimal calculé
    par Dijkstra. Les identifiants sont validés pour s'assurer qu'ils
    correspondent à des villes existantes en base.
    """
    ville_depart_id: int = Field(..., description="Identifiant de la ville de départ")
    ville_destination_id: int = Field(..., description="Identifiant de la ville de destination")


class EtapeItineraire(BaseModel):
    """
    Schéma représentant une étape du chemin optimal.
    
    Chaque étape contient les informations de la ville traversée,
    ce qui permet au frontend d'afficher l'itinéraire de manière
    lisible avec les noms des villes plutôt que leurs identifiants.
    """
    ville_id: int
    nom: str
    region: str


class ItineraireReponse(BaseModel):
    """
    Schéma de réponse pour un itinéraire calculé.
    
    La réponse contient le chemin complet avec toutes les étapes
    intermédiaires, le coût total du trajet, et un indicateur
    permettant de savoir si la destination est atteignable depuis
    le point de départ dans le graphe.
    """
    chemin: List[EtapeItineraire]
    cout_total: float
    atteignable: bool
    nombre_etapes: int