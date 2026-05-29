from sqlalchemy.orm import Session
from src.backend.repositories.admin_repository import AdminRepository
from src.backend.auth.auth_service import AuthService
from src.backend.repositories.prix_repository import PrixRepository


class AdminService:
    
    def __init__(self):
        self.repository = AdminRepository()
        self.auth_service = AuthService()
        self.prix_repository = PrixRepository()
    
    def lister_utilisateurs(self, db: Session, role_filtre: str = None):
        utilisateurs = self.repository.lister_utilisateurs(db, role_filtre)
        villes = self.prix_repository.lister_villes(db)
        dictionnaire_villes = {v.id: v for v in villes}
        
        resultat = []
        for u in utilisateurs:
            ville_nom = None
            if u.ville_assignee_id:
                ville = dictionnaire_villes.get(u.ville_assignee_id)
                if ville:
                    ville_nom = ville.nom
            
            resultat.append({
                "id": u.id,
                "nom": u.nom,
                "prenoms": u.prenoms,
                "email": u.email,
                "role": u.role,
                "statut_compte": u.statut_compte,
                "ville_assignee_id": u.ville_assignee_id,
                "ville_assignee_nom": ville_nom
            })
        
        return resultat
    
    def creer_utilisateur(
        self, db: Session, nom: str, prenoms: str, email: str,
        mot_de_passe: str, role: str, ville_assignee_id: int = None
    ):
        if self.repository.email_existe(db, email):
            return {"erreur": "Un utilisateur avec cet email existe déjà"}
        
        if ville_assignee_id and role != "agent":
            return {"erreur": "L'assignation à une ville n'est pertinente que pour les agents"}
        
        if role == "agent" and not ville_assignee_id:
            return {"erreur": "Un agent doit obligatoirement être assigné à une ville"}
        
        mot_de_passe_hache = self.auth_service.hacher_mot_de_passe(mot_de_passe)
        
        donnees = {
            "nom": nom,
            "prenoms": prenoms,
            "email": email,
            "mot_de_passe": mot_de_passe_hache,
            "role": role,
            "statut_compte": True,
            "ville_assignee_id": ville_assignee_id
        }
        
        utilisateur = self.repository.creer_utilisateur(db, donnees)
        
        ville_nom = None
        if utilisateur.ville_assignee_id:
            villes = self.prix_repository.lister_villes(db)
            ville = next((v for v in villes if v.id == utilisateur.ville_assignee_id), None)
            if ville:
                ville_nom = ville.nom
        
        utilisateur_enrichi = {
            "id": utilisateur.id,
            "nom": utilisateur.nom,
            "prenoms": utilisateur.prenoms,
            "email": utilisateur.email,
            "role": utilisateur.role,
            "statut_compte": utilisateur.statut_compte,
            "ville_assignee_id": utilisateur.ville_assignee_id,
            "ville_assignee_nom": ville_nom
        }
        
        return {"succes": True, "utilisateur": utilisateur_enrichi}
    
    def modifier_utilisateur(self, db: Session, utilisateur_id: int, modifications: dict):
        utilisateur = self.repository.obtenir_utilisateur_par_id(db, utilisateur_id)
        if not utilisateur:
            return {"erreur": "Utilisateur introuvable"}
        
        if "email" in modifications and modifications["email"]:
            if self.repository.email_existe(db, modifications["email"], exclure_id=utilisateur_id):
                return {"erreur": "Un autre utilisateur utilise déjà cet email"}
        
        if "mot_de_passe" in modifications and modifications["mot_de_passe"]:
            modifications["mot_de_passe"] = self.auth_service.hacher_mot_de_passe(
                modifications["mot_de_passe"]
            )
        
        utilisateur_modifie = self.repository.modifier_utilisateur(db, utilisateur, modifications)
        
        ville_nom = None
        if utilisateur_modifie.ville_assignee_id:
            villes = self.prix_repository.lister_villes(db)
            ville = next((v for v in villes if v.id == utilisateur_modifie.ville_assignee_id), None)
            if ville:
                ville_nom = ville.nom
    
        utilisateur_enrichi = {
            "id": utilisateur_modifie.id,
            "nom": utilisateur_modifie.nom,
            "prenoms": utilisateur_modifie.prenoms,
            "email": utilisateur_modifie.email,
            "role": utilisateur_modifie.role,
            "statut_compte": utilisateur_modifie.statut_compte,
            "ville_assignee_id": utilisateur_modifie.ville_assignee_id,
            "ville_assignee_nom": ville_nom
        }
    
        return {"succes": True, "utilisateur": utilisateur_enrichi}
    
    def basculer_statut_compte(self, db: Session, utilisateur_id: int):
        utilisateur = self.repository.obtenir_utilisateur_par_id(db, utilisateur_id)
        if not utilisateur:
            return {"erreur": "Utilisateur introuvable"}
        
        nouveau_statut = not utilisateur.statut_compte
        self.repository.modifier_utilisateur(
            db, utilisateur, {"statut_compte": nouveau_statut}
        )
        
        action = "activé" if nouveau_statut else "désactivé"
        return {
            "succes": True,
            "message": f"Le compte de {utilisateur.prenoms} {utilisateur.nom} a été {action}",
            "nouveau_statut": nouveau_statut
        }
    
    def lister_doublons(self, db: Session, jours: int = 30):
        doublons = self.repository.lister_doublons(db, jours)
        produits = self.prix_repository.lister_produits(db)
        villes = self.prix_repository.lister_villes(db)
        utilisateurs = self.repository.lister_utilisateurs(db)
        
        dictionnaire_produits = {p.id: p for p in produits}
        dictionnaire_villes = {v.id: v for v in villes}
        dictionnaire_agents = {u.id: u for u in utilisateurs if u.role == "agent"}
        
        resultat = []
        for rapport in doublons:
            produit = dictionnaire_produits.get(rapport.produit_id)
            ville = dictionnaire_villes.get(rapport.ville_id)
            agent = dictionnaire_agents.get(rapport.agent_id)
            
            if produit and ville:
                resultat.append({
                    "id": rapport.id,
                    "produit_nom": produit.nom_fr,
                    "ville_nom": ville.nom,
                    "prix": rapport.prix,
                    "date_heure": rapport.date_heure,
                    "agent_id": rapport.agent_id,
                    "agent_nom": f"{agent.prenoms} {agent.nom}" if agent else "Agent inconnu"
                })
        
        return resultat