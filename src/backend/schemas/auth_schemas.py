from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class ConnexionRequete(BaseModel):
    email: EmailStr
    mot_de_passe: str = Field(..., min_length=6)


class InscriptionRequete(BaseModel):
    nom: str = Field(..., min_length=2, max_length=100)
    prenoms: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    mot_de_passe: str = Field(..., min_length=8)


class UtilisateurReponse(BaseModel):
    id: int
    email: str
    nom: str
    prenoms: str
    role: str
    ville_assignee_id: Optional[int] = None
    ville_assignee_nom: Optional[str] = None
    
    class Config:
        from_attributes = True


class AuthReponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    utilisateur: UtilisateurReponse