"""
Schémas Pydantic pour la saisie de prix dans Tsenan'tsika.

Ces schémas définissent la structure des données utilisées par
les agents de collecte pour soumettre de nouveaux prix au système,
ainsi que la structure des réponses retournées après traitement
par le pipeline complet incluant Rabin-Karp et le Top-k.

La validation automatique fournie par Pydantic garantit que les
données entrantes sont conformes au format attendu, ce qui prévient
les erreurs de saisie et les tentatives d'injection de données
malveillantes.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SaisiePrixRequete(BaseModel):
    """
    Schéma de requête pour la soumission d'un nouveau prix.
    
    Les contraintes de validation imposent que le prix soit strictement
    positif car un prix nul ou négatif n'aurait aucun sens dans le
    contexte des produits alimentaires. L'agent_id permet de tracer
    quel utilisateur a soumis le rapport, ce qui est essentiel pour
    l'auditabilité du système.
    """
    produit_id: int = Field(..., gt=0, description="Identifiant du produit")
    ville_id: int = Field(..., gt=0, description="Identifiant de la ville")
    prix: float = Field(..., gt=0, description="Prix observé en Ariary")
    agent_id: int = Field(..., gt=0, description="Identifiant de l'agent qui soumet le prix")


class SaisiePrixReponse(BaseModel):
    """
    Schéma de réponse après tentative de saisie d'un prix.
    
    Cette structure communique au frontend le résultat complet du
    traitement, incluant si l'insertion a réussi, si un doublon a été
    détecté, et si une alerte a éventuellement été déclenchée suite
    à la mise à jour du Top-k.
    """
    succes: bool
    message: str
    rapport_id: Optional[int] = None
    prix_marche_id: Optional[int] = None
    doublon_detecte: bool = False
    alerte_declenchee: bool = False
    variation_pourcent: Optional[float] = None