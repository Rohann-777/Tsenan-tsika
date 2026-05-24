"""
Schémas Pydantic pour les fonctionnalités d'administration de Tsenan'tsika.

Ce module définit les structures de données utilisées par l'administrateur
pour gérer les comptes utilisateurs et surveiller les rapports dupliqués.
La séparation entre schémas d'entrée et de sortie garantit que les
informations sensibles comme les mots de passe ne fuient jamais vers
le frontend, et que les données entrantes sont rigoureusement validées
avant d'être traitées.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UtilisateurCreer(BaseModel):
    """
    Schéma de requête pour la création d'un nouvel utilisateur par
    l'administrateur. Le rôle est restreint aux types que l'administrateur
    peut créer, à savoir agent, analyste et citoyen. Les administrateurs
    ne peuvent pas être créés via cette interface conformément à notre
    décision architecturale.
    """
    nom: str = Field(..., min_length=2, max_length=100)
    prenoms: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    mot_de_passe: str = Field(..., min_length=8)
    role: str = Field(..., pattern="^(agent|analyste|citoyen)$")
    ville_assignee_id: Optional[int] = Field(None, gt=0)


class UtilisateurModifier(BaseModel):
    """
    Schéma de requête pour la modification d'un utilisateur existant.
    
    Tous les champs sont optionnels car l'administrateur peut choisir
    de ne modifier qu'une partie des informations. Le mot de passe est
    également optionnel pour permettre de modifier d'autres informations
    sans avoir à le réinitialiser systématiquement.
    """
    nom: Optional[str] = Field(None, min_length=2, max_length=100)
    prenoms: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    mot_de_passe: Optional[str] = Field(None, min_length=8)
    role: Optional[str] = Field(None, pattern="^(agent|analyste|citoyen)$")
    ville_assignee_id: Optional[int] = Field(None, gt=0)
    statut_compte: Optional[bool] = None


class UtilisateurAdmin(BaseModel):
    """
    Schéma de réponse pour l'affichage d'un utilisateur dans l'interface
    d'administration. Ne contient jamais le mot de passe haché qui ne
    doit jamais sortir du backend, même hashé.
    """
    id: int
    nom: str
    prenoms: str
    email: str
    role: str
    statut_compte: bool
    ville_assignee_id: Optional[int]
    ville_assignee_nom: Optional[str]
    
    class Config:
        from_attributes = True


class RapportDoublon(BaseModel):
    """
    Schéma de réponse pour l'affichage d'un rapport identifié comme
    doublon par Rabin-Karp. Inclut toutes les informations nécessaires
    à l'administrateur pour analyser la situation et identifier
    d'éventuels comportements problématiques.
    """
    id: int
    produit_nom: str
    ville_nom: str
    prix: float
    date_heure: datetime
    agent_id: int
    agent_nom: str
    
    class Config:
        from_attributes = True