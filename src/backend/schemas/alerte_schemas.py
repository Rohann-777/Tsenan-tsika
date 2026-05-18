"""
Schémas Pydantic pour le tableau de bord des alertes dans Tsenan'tsika.

Ces schémas définissent la structure des données affichées sur le
tableau de bord destiné aux analystes du ministère et aux citoyens
en consultation libre. Ils agrègent les informations provenant des
alertes stockées en base et du classement Top-k maintenu en mémoire
par le service de saisie.

La structuration en plusieurs schémas distincts permet une grande
flexibilité dans la composition des données affichées et facilite
l'évolution future du système sans casser la compatibilité avec
les clients existants.
"""

from datetime import datetime
from typing import List
from pydantic import BaseModel


class AlerteDetaillee(BaseModel):
    """
    Schéma de représentation d'une alerte avec toutes les informations
    contextuelles nécessaires à son affichage sur le tableau de bord.
    
    Les informations du produit et de la ville sont incluses directement
    pour éviter au frontend de devoir effectuer des requêtes supplémentaires,
    ce qui améliore les performances et la simplicité du code client.
    """
    id: int
    date: datetime
    produit_id: int
    produit_nom: str
    ville_id: int
    ville_nom: str
    
    class Config:
        from_attributes = True


class EntreeTopK(BaseModel):
    """
    Schéma de représentation d'une entrée dans le classement Top-k
    des produits avec la plus forte hausse de prix.
    
    Chaque entrée combine l'identifiant et le nom du produit avec la
    variation en pourcentage qui a justifié son entrée dans le classement.
    Cette structure permet au frontend d'afficher facilement un classement
    visuellement parlant.
    """
    produit_id: int
    produit_nom: str
    variation_pourcent: float
    rang: int


class TableauBordReponse(BaseModel):
    """
    Schéma global du tableau de bord qui agrège toutes les informations
    affichées à l'analyste ou au citoyen consultant le système.
    
    Cette structure consolidée permet au frontend de récupérer toutes
    les informations nécessaires en une seule requête, ce qui simplifie
    le code client et améliore l'expérience utilisateur en évitant les
    multiples requêtes successives.
    """
    nombre_alertes_actives: int
    alertes_recentes: List[AlerteDetaillee]
    top_5_hausses: List[EntreeTopK]