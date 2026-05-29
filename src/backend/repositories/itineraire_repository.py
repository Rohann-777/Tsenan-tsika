from sqlalchemy.orm import Session
from src.backend.models.modeles import Ville, ConnexionVille


class ItineraireRepository:
    def obtenir_ville_par_id(self, db: Session, ville_id: int):
        return db.query(Ville).filter(Ville.id == ville_id).first()
    
    def construire_graphe(self, db: Session):
        villes = db.query(Ville).all()
        
        graphe = {ville.id: [] for ville in villes}
        
        connexions = db.query(ConnexionVille).all()
        
        for connexion in connexions:
            graphe[connexion.ville_depart_id].append(
                (connexion.ville_destination_id, connexion.cout)
            )
        
        return graphe
    
    def obtenir_dictionnaire_villes(self, db: Session):
        villes = db.query(Ville).all()
        return {ville.id: ville for ville in villes}