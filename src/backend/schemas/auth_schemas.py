"""
Schémas Pydantic pour l'authentification dans Tsenan'tsika.
"""

from pydantic import BaseModel, EmailStr, Field


class ConnexionRequete(BaseModel):
    """
    Schéma de requête pour la connexion d'un utilisateur existant.
    
    EmailStr fournit une validation automatique du format de l'email
    qui vérifie qu'il contient bien un arobase et un domaine valide.
    """
    email: EmailStr
    mot_de_passe: str = Field(..., min_length=6)


class InscriptionRequete(BaseModel):
    """
    Schéma de requête pour l'inscription d'un nouveau citoyen.
    
    Les contraintes de validation imposent un nom et un prénom non
    vides, un email valide, et un mot de passe d'au moins 8 caractères
    pour respecter les bonnes pratiques de sécurité.
    """
    nom: str = Field(..., min_length=2, max_length=100)
    prenoms: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    mot_de_passe: str = Field(..., min_length=8)


class UtilisateurReponse(BaseModel):
    """
    Schéma de réponse contenant les informations d'un utilisateur
    après une connexion ou une inscription réussie.
    """
    id: int
    email: str
    nom: str
    prenoms: str
    role: str
    
    class Config:
        from_attributes = True


class AuthReponse(BaseModel):
    """
    Schéma de réponse pour une opération d'authentification.
    
    Les noms de champs access_token et token_type suivent le standard
    OAuth2 pour assurer la compatibilité avec les outils standards
    comme Swagger UI qui s'attendent à trouver le token dans le
    champ access_token de la réponse.
    """
    access_token: str
    token_type: str = "Bearer"
    utilisateur: UtilisateurReponse