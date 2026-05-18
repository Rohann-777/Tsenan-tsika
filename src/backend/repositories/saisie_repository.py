"""
Repository pour la saisie de prix dans Tsenan'tsika.

Ce module encapsule toutes les opérations de base de données liées
à l'insertion de nouveaux rapports et prix marchés, ainsi que la
récupération des données nécessaires aux algorithmes Rabin-Karp
et Top-k qui interviennent dans le pipeline de traitement.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from src.backend.models.modeles import RapportPrix, PrixMarche, Alerte


class SaisieRepository:
    """
    Classe d'accès aux données pour la saisie de prix.
    """
    
    def lister_rapports_recents(self, db: Session, heures: int = 24):
        """
        Récupère les rapports soumis dans la fenêtre temporelle récente
        définie par le paramètre heures. Ces rapports serviront à
        Rabin-Karp pour la détection de doublons.
        
        Pour optimiser les performances, on ne récupère que les rapports
        qui ne sont pas déjà marqués comme doublons, ce qui évite de
        comparer un nouveau rapport avec des doublons déjà identifiés.
        """
        date_limite = datetime.now() - timedelta(hours=heures)
        return db.query(RapportPrix).filter(
            RapportPrix.date_heure >= date_limite,
            RapportPrix.est_doublon == False
        ).all()
    
    def inserer_rapport(
        self, db: Session, produit_id: int, ville_id: int,
        prix: float, agent_id: int, est_doublon: bool = False
    ):
        """
        Insère un nouveau rapport de prix dans la base de données.
        
        Tous les rapports sont enregistrés même ceux marqués comme
        doublons, pour permettre l'audit et le suivi des tentatives
        de soumission. Le flag est_doublon distingue les rapports
        valides des doublons détectés.
        """
        nouveau_rapport = RapportPrix(
            produit_id=produit_id,
            ville_id=ville_id,
            prix=prix,
            date_heure=datetime.now(),
            agent_id=agent_id,
            est_doublon=est_doublon
        )
        db.add(nouveau_rapport)
        db.commit()
        db.refresh(nouveau_rapport)
        return nouveau_rapport
    
    def inserer_prix_marche(
        self, db: Session, produit_id: int, ville_id: int,
        prix: float, agent_id: int
    ):
        """
        Insère un nouveau prix marché validé dans la base de données.
        
        Cette table ne reçoit que les rapports validés sans doublon,
        contrairement à la table rapport_prix qui conserve l'historique
        complet des soumissions incluant les doublons.
        """
        nouveau_prix = PrixMarche(
            produit_id=produit_id,
            ville_id=ville_id,
            prix=prix,
            date_saisie=datetime.now(),
            agent_id=agent_id
        )
        db.add(nouveau_prix)
        db.commit()
        db.refresh(nouveau_prix)
        return nouveau_prix
    
    def obtenir_prix_moyen_recent(
        self, db: Session, produit_id: int, ville_id: int, jours: int = 7
    ):
        """
        Calcule la moyenne récente des prix d'un produit dans une ville
        sur les derniers jours spécifiés. Cette moyenne servira de
        référence pour calculer la variation du nouveau prix soumis,
        ce qui alimentera ensuite le Top-k.
        
        Cette méthode utilise directement une fonction d'agrégation
        SQL pour des raisons de performance, car nous voulons une
        valeur unique et non le détail des prix.
        """
        date_limite = datetime.now() - timedelta(days=jours)
        resultat = db.query(func.avg(PrixMarche.prix)).filter(
            PrixMarche.produit_id == produit_id,
            PrixMarche.ville_id == ville_id,
            PrixMarche.date_saisie >= date_limite
        ).scalar()
        
        return float(resultat) if resultat else None
    
    def creer_alerte(self, db: Session, produit_id: int, ville_id: int):
        """
        Crée une nouvelle alerte quand le Top-k détecte qu'une variation
        de prix mérite d'être signalée aux analystes.
        """
        nouvelle_alerte = Alerte(
            produit_id=produit_id,
            ville_id=ville_id,
            date=datetime.now()
        )
        db.add(nouvelle_alerte)
        db.commit()
        db.refresh(nouvelle_alerte)
        return nouvelle_alerte