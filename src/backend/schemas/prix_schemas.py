"""
Schémas Pydantic pour les données de prix dans Tsenan'tsika.

Ces schémas définissent la structure des données échangées entre
le frontend et le backend pour tout ce qui concerne les prix.
Ils servent à la fois pour la validation des données entrantes
et pour la sérialisation des données sortantes, garantissant
ainsi la cohérence des formats sur toute la chaîne de traitement.

La séparation entre les schémas d'entrée et de sortie est une bonne
pratique car elle permet de cacher certains champs internes comme
les identifiants techniques quand ils ne sont pas nécessaires côté
frontend, et d'imposer des règles de validation différentes selon
le contexte.
"""

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class ProduitReponse(BaseModel):
    """
    Schéma de sortie pour un produit. Contient toutes les informations
    qu'on souhaite exposer au frontend.
    """
    id: int
    nom_fr: str
    nom_mg: str
    unite: str
    categorie: str
    
    class Config:
        """
        Configuration qui permet à Pydantic de lire les attributs
        depuis les objets SQLAlchemy comme s'il s'agissait d'un
        dictionnaire. Sans cette configuration, on devrait convertir
        manuellement chaque modèle SQLAlchemy en dictionnaire avant
        de le passer au schéma.
        """
        from_attributes = True


class VilleReponse(BaseModel):
    """
    Schéma de sortie pour une ville avec ses coordonnées géographiques.
    """
    id: int
    nom: str
    region: str
    latitude: float
    longitude: float
    
    class Config:
        from_attributes = True


class PrixMarcheReponse(BaseModel):
    """
    Schéma de sortie pour un prix marché. Inclut les informations
    du produit et de la ville associés pour éviter au frontend de
    devoir faire plusieurs requêtes.
    """
    id: int
    prix: float
    date_saisie: datetime
    produit: ProduitReponse
    ville: VilleReponse
    
    class Config:
        from_attributes = True


class PrixMoyenReponse(BaseModel):
    """
    Schéma de sortie pour une moyenne de prix calculée par Fenwick Tree.
    Cette structure est utilisée par le tableau de bord pour afficher
    les tendances de prix.
    """
    produit_id: int
    produit_nom: str
    ville_id: int
    ville_nom: str
    prix_moyen: float
    nombre_releves: int
    periode_debut: datetime
    periode_fin: datetime