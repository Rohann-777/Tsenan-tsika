"""
Repository pour les opérations d'administration dans Tsenan'tsika.

Ce module encapsule toutes les opérations de base de données liées
à la gestion des utilisateurs et à la consultation des doublons
détectés par le système.
"""

from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.backend.models.modeles import Utilisateur, RapportPrix, Ville, Produit


class AdminRepository:
    """
    Classe d'accès aux données pour les fonctionnalités administrateur.
    """
    
    def lister_utilisateurs(self, db: Session, role_filtre: str = None):
        """
        Récupère la liste de tous les utilisateurs du système avec
        possibilité de filtrer par rôle. Les administrateurs sont
        toujours exclus de la liste conformément à notre décision
        architecturale qui les exclut du périmètre de gestion F5.
        """
        requete = db.query(Utilisateur).filter(
            Utilisateur.role != "administrateur"
        )
        
        if role_filtre:
            requete = requete.filter(Utilisateur.role == role_filtre)
        
        return requete.order_by(Utilisateur.role, Utilisateur.nom).all()
    
    def obtenir_utilisateur_par_id(self, db: Session, utilisateur_id: int):
        """
        Récupère un utilisateur spécifique par son identifiant.
        Cette méthode est utilisée pour les opérations de modification
        et de désactivation.
        """
        return db.query(Utilisateur).filter(
            Utilisateur.id == utilisateur_id,
            Utilisateur.role != "administrateur"
        ).first()
    
    def email_existe(self, db: Session, email: str, exclure_id: int = None):
        """
        Vérifie si un email est déjà utilisé par un autre utilisateur.
        Le paramètre exclure_id permet de vérifier l'unicité lors d'une
        modification sans considérer l'utilisateur en cours de modification.
        """
        requete = db.query(Utilisateur).filter(Utilisateur.email == email)
        if exclure_id:
            requete = requete.filter(Utilisateur.id != exclure_id)
        return requete.first() is not None
    
    def creer_utilisateur(self, db: Session, donnees: dict):
        """
        Crée un nouvel utilisateur en base avec les données fournies.
        Le mot de passe doit déjà être haché avant l'appel à cette méthode.
        """
        nouvel_utilisateur = Utilisateur(**donnees)
        db.add(nouvel_utilisateur)
        db.commit()
        db.refresh(nouvel_utilisateur)
        return nouvel_utilisateur
    
    def modifier_utilisateur(self, db: Session, utilisateur: Utilisateur, modifications: dict):
        """
        Applique les modifications fournies à un utilisateur existant.
        Seuls les champs présents dans le dictionnaire de modifications
        sont mis à jour, les autres restent inchangés.
        """
        for cle, valeur in modifications.items():
            if valeur is not None:
                setattr(utilisateur, cle, valeur)
        db.commit()
        db.refresh(utilisateur)
        return utilisateur
    
    def lister_doublons(self, db: Session, jours: int = 30):
        """
        Récupère les rapports marqués comme doublons sur la période
        spécifiée. Cette liste permet à l'administrateur de surveiller
        les tentatives répétées de soumission.
        """
        date_limite = datetime.now() - timedelta(days=jours)
        return db.query(RapportPrix).filter(
            RapportPrix.est_doublon == True,
            RapportPrix.date_heure >= date_limite
        ).order_by(RapportPrix.date_heure.desc()).all()