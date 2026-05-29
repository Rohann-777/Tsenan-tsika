from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.backend.config.database import Base


class Utilisateur(Base):
    __tablename__ = "utilisateur"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    prenoms = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)
    statut_compte = Column(Boolean, nullable=False, default=True)
    ville_assignee_id = Column(Integer, ForeignKey("ville.id"), nullable=True)
    
    # Relation simple vers la ville assignée pour les agents
    ville_assignee = relationship("Ville", foreign_keys=[ville_assignee_id])


class Produit(Base):
    __tablename__ = "produit"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom_fr = Column(String(100), nullable=False)
    nom_mg = Column(String(100), nullable=False)
    unite = Column(String(30), nullable=False)
    categorie = Column(String(50), nullable=False)
    
    # Relations inverses vers les entités qui référencent ce produit
    rapports = relationship("RapportPrix", back_populates="produit")
    prix_marche = relationship("PrixMarche", back_populates="produit")
    alertes = relationship("Alerte", back_populates="produit")


class Ville(Base):
    __tablename__ = "ville"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    
    # Relations inverses
    rapports = relationship("RapportPrix", back_populates="ville")
    prix_marche = relationship("PrixMarche", back_populates="ville")
    alertes = relationship("Alerte", back_populates="ville")
    
    # Les connexions où cette ville est la ville de départ
    connexions_depart = relationship(
        "ConnexionVille",
        foreign_keys="ConnexionVille.ville_depart_id",
        back_populates="ville_depart"
    )
    
    # Les connexions où cette ville est la ville de destination
    connexions_destination = relationship(
        "ConnexionVille",
        foreign_keys="ConnexionVille.ville_destination_id",
        back_populates="ville_destination"
    )


class ConnexionVille(Base):
    __tablename__ = "connexion_ville"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ville_depart_id = Column(Integer, ForeignKey("ville.id"), nullable=False)
    ville_destination_id = Column(Integer, ForeignKey("ville.id"), nullable=False)
    cout = Column(Float, nullable=False)
    
    # Relations vers les objets Ville aux deux extrémités de la connexion
    ville_depart = relationship(
        "Ville",
        foreign_keys=[ville_depart_id],
        back_populates="connexions_depart"
    )
    ville_destination = relationship(
        "Ville",
        foreign_keys=[ville_destination_id],
        back_populates="connexions_destination"
    )


class RapportPrix(Base):
    __tablename__ = "rapport_prix"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    produit_id = Column(Integer, ForeignKey("produit.id"), nullable=False)
    ville_id = Column(Integer, ForeignKey("ville.id"), nullable=False)
    prix = Column(Float, nullable=False)
    date_heure = Column(DateTime, nullable=False)
    agent_id = Column(Integer, ForeignKey("utilisateur.id"), nullable=False)
    est_doublon = Column(Boolean, default=False)
    
    # Relations vers les entités liées
    produit = relationship("Produit", back_populates="rapports")
    ville = relationship("Ville", back_populates="rapports")
    agent = relationship("Utilisateur")


class PrixMarche(Base):
    __tablename__ = "prix_marche"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    produit_id = Column(Integer, ForeignKey("produit.id"), nullable=False)
    ville_id = Column(Integer, ForeignKey("ville.id"), nullable=False)
    prix = Column(Float, nullable=False)
    date_saisie = Column(DateTime, nullable=False)
    agent_id = Column(Integer, ForeignKey("utilisateur.id"), nullable=False)
    
    # Relations vers les entités liées
    produit = relationship("Produit", back_populates="prix_marche")
    ville = relationship("Ville", back_populates="prix_marche")
    agent = relationship("Utilisateur")


class Alerte(Base):
    __tablename__ = "alerte"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    produit_id = Column(Integer, ForeignKey("produit.id"), nullable=False)
    ville_id = Column(Integer, ForeignKey("ville.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    
    # Relations vers les entités liées
    produit = relationship("Produit", back_populates="alertes")
    ville = relationship("Ville", back_populates="alertes")