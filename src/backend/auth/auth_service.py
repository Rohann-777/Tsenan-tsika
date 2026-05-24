"""
Service métier d'authentification pour Tsenan'tsika.

Ce module contient la logique applicative liée à la connexion des
utilisateurs et à l'inscription des nouveaux citoyens. Il fait le
lien entre les routes HTTP, le service JWT, et la base de données
via le repository des utilisateurs.
"""

import bcrypt
from sqlalchemy.orm import Session
from src.backend.models.modeles import Utilisateur
from src.backend.auth.jwt_service import JwtService


class AuthService:
    """
    Service métier pour l'authentification et l'inscription.
    """
    
    def __init__(self):
        self.jwt_service = JwtService()
    
    def verifier_mot_de_passe(self, mot_de_passe_clair: str, hachage: str) -> bool:
        """
        Vérifie qu'un mot de passe en clair correspond bien à son hachage.
        
        bcrypt.checkpw effectue cette comparaison de manière sécurisée
        en utilisant le sel intégré au hachage. Cette opération est
        volontairement lente pour ralentir les tentatives d'attaque
        par force brute, ce qui correspond à l'une des exigences de
        sécurité du cahier des charges.
        """
        return bcrypt.checkpw(
            mot_de_passe_clair.encode('utf-8'),
            hachage.encode('utf-8')
        )
    
    def hacher_mot_de_passe(self, mot_de_passe_clair: str) -> str:
        """
        Hache un mot de passe avec bcrypt pour son stockage sécurisé.
        
        Le sel aléatoire généré garantit que deux utilisateurs avec
        le même mot de passe auront des hachages différents en base,
        ce qui rend impossible les attaques par tables précalculées.
        """
        sel = bcrypt.gensalt()
        hachage = bcrypt.hashpw(mot_de_passe_clair.encode('utf-8'), sel)
        return hachage.decode('utf-8')
    
    def authentifier(self, db: Session, email: str, mot_de_passe: str):
        """
        Tente d'authentifier un utilisateur avec ses identifiants.
        
        Si l'authentification réussit, cette méthode retourne un token
        JWT et les informations de l'utilisateur. Si elle échoue, elle
        retourne None pour permettre au controller de renvoyer une
        erreur appropriée au client.
        
        On utilise volontairement un message d'erreur générique en cas
        d'échec pour ne pas révéler si c'est l'email ou le mot de passe
        qui est incorrect. Cela complique les attaques par énumération
        d'emails qui chercheraient à découvrir quels emails existent en base.
        """
        utilisateur = db.query(Utilisateur).filter(
            Utilisateur.email == email
        ).first()
        
        if not utilisateur:
            return None
        
        if not self.verifier_mot_de_passe(mot_de_passe, utilisateur.mot_de_passe):
            return None
        
        # Génération du token avec les informations essentielles de l'utilisateur.
        # Ces informations seront accessibles dans chaque requête protégée
        # sans nécessiter de nouvelle requête à la base de données.
        token = self.jwt_service.creer_token({
            "sub": str(utilisateur.id),
            "email": utilisateur.email,
            "role": utilisateur.role
        })
        
        return {
            "access_token": token,
            "token_type": "Bearer",
            "utilisateur": {
                "id": utilisateur.id,
                "email": utilisateur.email,
                "nom": utilisateur.nom,
                "prenoms": utilisateur.prenoms,
                "role": utilisateur.role
            }
        }
    
    def inscrire_citoyen(
        self, db: Session, nom: str, prenoms: str,
        email: str, mot_de_passe: str
    ):
        """
        Inscrit un nouveau citoyen dans le système.
        
        Cette méthode est volontairement limitée au rôle citoyen car
        les autres rôles doivent être créés par un administrateur via
        une interface dédiée, conformément au cahier des charges.
        
        Avant l'insertion, on vérifie qu'aucun utilisateur n'existe
        déjà avec cet email pour respecter la contrainte d'unicité
        définie dans le schéma de base de données.
        """
        utilisateur_existant = db.query(Utilisateur).filter(
            Utilisateur.email == email
        ).first()
        
        if utilisateur_existant:
            return None
        
        # Hachage du mot de passe avant stockage. Le mot de passe en
        # clair ne doit jamais être stocké en base ni apparaître dans
        # les logs, conformément aux bonnes pratiques de sécurité.
        mot_de_passe_hache = self.hacher_mot_de_passe(mot_de_passe)
        
        nouveau_utilisateur = Utilisateur(
            nom=nom,
            prenoms=prenoms,
            email=email,
            mot_de_passe=mot_de_passe_hache,
            role="citoyen"
        )
        
        db.add(nouveau_utilisateur)
        db.commit()
        db.refresh(nouveau_utilisateur)
        
        # Génération automatique d'un token pour connecter immédiatement
        # le nouvel utilisateur après son inscription. Cela améliore
        # l'expérience utilisateur en évitant une étape de connexion
        # supplémentaire après l'inscription.
        token = self.jwt_service.creer_token({
            "sub": str(nouveau_utilisateur.id),
            "email": nouveau_utilisateur.email,
            "role": nouveau_utilisateur.role
        })
        
        return {
            "access_token": token,
            "token_type": "Bearer",
            "utilisateur": {
                "id": nouveau_utilisateur.id,
                "email": nouveau_utilisateur.email,
                "nom": nouveau_utilisateur.nom,
                "prenoms": nouveau_utilisateur.prenoms,
                "role": nouveau_utilisateur.role
            }
        }