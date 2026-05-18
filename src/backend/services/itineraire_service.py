"""
Service métier pour le calcul des itinéraires d'approvisionnement
dans Tsenan'tsika.

Ce module coordonne la récupération des données du graphe routier
depuis la base, l'exécution de l'algorithme de Dijkstra, et la
construction d'une réponse enrichie avec les informations détaillées
des villes traversées.

Le service est l'endroit où la logique métier s'exprime, à savoir
la décision d'utiliser Dijkstra pour ce type de problème, la
manière de gérer les cas où la destination n'est pas atteignable,
et l'enrichissement des résultats bruts de l'algorithme avec les
métadonnées nécessaires au frontend.
"""

from sqlalchemy.orm import Session
from src.backend.repositories.itineraire_repository import ItineraireRepository
from src.backend.algorithms.dijkstra import Dijkstra


class ItineraireService:
    """
    Service métier pour le calcul des itinéraires d'approvisionnement.
    """
    
    def __init__(self):
        """
        Initialise le service avec une instance du repository et de
        l'algorithme de Dijkstra. L'algorithme est instancié une seule
        fois et réutilisé pour tous les calculs, ce qui est efficace
        car Dijkstra n'a pas d'état interne entre les appels.
        """
        self.repository = ItineraireRepository()
        self.dijkstra = Dijkstra()
    
    def calculer_itineraire(
        self, db: Session, ville_depart_id: int, ville_destination_id: int
    ):
        """
        Calcule l'itinéraire optimal entre deux villes en utilisant
        l'algorithme de Dijkstra.
        
        Cette méthode coordonne plusieurs étapes essentielles. D'abord
        elle vérifie que les deux villes existent en base. Puis elle
        construit le graphe routier à partir des données stockées.
        Ensuite elle invoque Dijkstra pour trouver le chemin optimal.
        Et enfin elle enrichit le résultat brut de l'algorithme avec
        les informations détaillées de chaque ville traversée pour
        construire une réponse complète pour le frontend.
        """
        # Vérification de l'existence des villes
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
        
        # Construction du graphe routier à partir des données en base
        graphe = self.repository.construire_graphe(db)
        
        # Récupération des informations complètes des villes pour
        # enrichir la réponse avec les noms et régions
        dictionnaire_villes = self.repository.obtenir_dictionnaire_villes(db)
        
        # Exécution de l'algorithme de Dijkstra
        resultat = self.dijkstra.calculer_chemin_optimal(
            graphe, ville_depart_id, ville_destination_id
        )
        
        # Si la destination n'est pas atteignable, on retourne directement
        # le résultat de Dijkstra qui contient déjà l'information
        if not resultat["atteignable"]:
            return {
                "chemin": [],
                "cout_total": resultat["cout_total"],
                "atteignable": False,
                "nombre_etapes": 0
            }
        
        # Enrichissement du chemin avec les informations détaillées
        # de chaque ville traversée
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