"""
Modèles SQLAlchemy pour Tsenan'tsika.

Ce module définit toutes les classes qui représentent les tables
de la base de données PostgreSQL. Chaque classe correspond à une
table et chaque attribut de classe correspond à une colonne.

Les modèles utilisent les types de SQLAlchemy plutôt que les types
Python natifs car SQLAlchemy doit savoir comment générer le SQL
correct pour PostgreSQL. Par exemple, on utilise String au lieu
de str et Integer au lieu de int.

Les relations entre tables sont définies via ForeignKey et
relationship, ce qui permet à SQLAlchemy de gérer automatiquement
les jointures et de naviguer entre les objets liés.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.backend.config.database import Base


class Utilisateur(Base):
    """
    Modèle représentant un utilisateur du système Tsenan'tsika.
    """
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
    """
    Modèle pour la table produit qui stocke les sept produits de
    première nécessité suivis par le système.
    
    Le double nommage en français et en malgache permet de respecter
    la contrainte multilingue du cahier des charges, même si nous
    avons décidé de mettre cette fonctionnalité de côté pour le
    prototype, la structure est prête à l'accueillir.
    """
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
    """
    Modèle pour la table ville qui stocke les sept villes pilotes
    de Tsenan'tsika.
    
    Les coordonnées géographiques latitude et longitude sont stockées
    pour permettre le calcul des distances entre villes et l'affichage
    sur des cartes dans le frontend si on l'ajoute plus tard.
    """
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
    """
    Modèle pour la table connexion_ville qui stocke les arêtes
    du graphe routier utilisé par Dijkstra.
    
    Chaque connexion représente une route directe entre deux villes
    avec un coût de transport calculé comme distance multipliée
    par l'indice carburant en vigueur.
    """
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
    """
    Modèle pour la table rapport_prix qui stocke les soumissions
    brutes des agents avant validation par Rabin-Karp.
    
    L'attribut est_doublon est marqué automatiquement par le système
    quand Rabin-Karp détecte qu'un rapport identique existe déjà
    dans les dernières 24 heures.
    """
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
    """
    Modèle pour la table prix_marche qui stocke les prix validés
    après vérification de non-doublon.
    
    Ces prix sont ceux utilisés par le Fenwick Tree pour calculer
    les moyennes et par le Top-k pour détecter les hausses anormales.
    """
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
    """
    Modèle pour la table alerte qui stocke les alertes déclenchées
    automatiquement par le système quand le Top-k détecte une
    hausse anormale de prix.
    
    Les alertes sont affichées sur le tableau de bord des analystes
    et peuvent être consultées par les citoyens en lecture seule.
    """
    __tablename__ = "alerte"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    produit_id = Column(Integer, ForeignKey("produit.id"), nullable=False)
    ville_id = Column(Integer, ForeignKey("ville.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    
    # Relations vers les entités liées
    produit = relationship("Produit", back_populates="alertes")
    ville = relationship("Ville", back_populates="alertes")