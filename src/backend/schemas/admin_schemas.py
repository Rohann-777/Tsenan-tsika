from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UtilisateurCreer(BaseModel):
    nom: str = Field(..., min_length=2, max_length=100)
    prenoms: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    mot_de_passe: str = Field(..., min_length=8)
    role: str = Field(..., pattern="^(agent|analyste|citoyen)$")
    ville_assignee_id: Optional[int] = Field(None, gt=0)


class UtilisateurModifier(BaseModel):
    nom: Optional[str] = Field(None, min_length=2, max_length=100)
    prenoms: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    mot_de_passe: Optional[str] = Field(None, min_length=8)
    role: Optional[str] = Field(None, pattern="^(agent|analyste|citoyen)$")
    ville_assignee_id: Optional[int] = Field(None, gt=0)
    statut_compte: Optional[bool] = None


class UtilisateurAdmin(BaseModel):
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
    id: int
    produit_nom: str
    ville_nom: str
    prix: float
    date_heure: datetime
    agent_id: int
    agent_nom: str
    
    class Config:
        from_attributes = True