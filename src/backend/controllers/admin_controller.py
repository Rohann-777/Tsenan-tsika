from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from src.backend.services.admin_service import AdminService

class AdminController:
    
    def __init__(self):
        self.service = AdminService()
    
    def lister_utilisateurs(self, db: Session, role: str = None):
        return self.service.lister_utilisateurs(db, role)
    
    def creer_utilisateur(self, db: Session, donnees: dict):
        resultat = self.service.creer_utilisateur(
            db,
            donnees["nom"],
            donnees["prenoms"],
            donnees["email"],
            donnees["mot_de_passe"],
            donnees["role"],
            donnees.get("ville_assignee_id")
        )
        
        if "erreur" in resultat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultat["erreur"]
            )
        
        return resultat["utilisateur"]
    
    def modifier_utilisateur(self, db: Session, utilisateur_id: int, donnees: dict):
        resultat = self.service.modifier_utilisateur(db, utilisateur_id, donnees)
        
        if "erreur" in resultat:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultat["erreur"]
            )
        
        return resultat["utilisateur"]
    
    def basculer_statut(self, db: Session, utilisateur_id: int):
        resultat = self.service.basculer_statut_compte(db, utilisateur_id)
        
        if "erreur" in resultat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=resultat["erreur"]
            )
        
        return resultat
    
    def lister_doublons(self, db: Session, jours: int = 30):
        """
        Endpoint pour récupérer les rapports doublons.
        """
        return self.service.lister_doublons(db, jours)