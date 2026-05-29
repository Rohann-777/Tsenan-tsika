from sqlalchemy.orm import Session
from src.backend.repositories.itineraire_repository import ItineraireRepository
from src.backend.algorithms.dijkstra import Dijkstra


class ItineraireService:
    
    def __init__(self):
        self.repository = ItineraireRepository()
        self.dijkstra = Dijkstra()
    
    def calculer_itineraire(
        self, db: Session, ville_depart_id: int, ville_destination_id: int
    ):
        ville_depart = self.repository.obtenir_ville_par_id(db, ville_depart_id)
        if not ville_depart:
            return {
                "erreur": f"La ville de départ {ville_depart_id} n'existe pas",
                "atteignable": False
            }
        
        ville_destination = self.repository.obtenir_ville_par_id(db, ville_destination_id)
        if not ville_destination:
            return {
                "erreur": f"La ville de destination {ville_destination_id} n'existe pas",
                "atteignable": False
            }
        
        graphe = self.repository.construire_graphe(db)
        
        dictionnaire_villes = self.repository.obtenir_dictionnaire_villes(db)
        
        resultat = self.dijkstra.calculer_chemin_optimal(
            graphe, ville_depart_id, ville_destination_id
        )
        
        if not resultat["atteignable"]:
            return {
                "chemin": [],
                "cout_total": resultat["cout_total"],
                "atteignable": False,
                "nombre_etapes": 0
            }
        
        chemin_detaille = []
        for ville_id in resultat["chemin"]:
            ville = dictionnaire_villes[ville_id]
            chemin_detaille.append({
                "ville_id": ville.id,
                "nom": ville.nom,
                "region": ville.region
            })
        
        return {
            "chemin": chemin_detaille,
            "cout_total": resultat["cout_total"],
            "atteignable": True,
            "nombre_etapes": len(chemin_detaille)
        }