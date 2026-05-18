"""
Repository pour l'accès aux données du graphe routier dans Tsenan'tsika.

Ce module encapsule l'accès aux informations nécessaires au calcul
des itinéraires d'approvisionnement, à savoir les villes et leurs
connexions routières avec les coûts associés.

La transformation des données relationnelles en structure de graphe
adaptée à Dijkstra est faite ici pour isoler cette logique du reste
du code et permettre une réutilisation facile.
"""

from sqlalchemy.orm import Session
from src.backend.models.modeles import Ville, ConnexionVille


class ItineraireRepository:
    """
    Classe d'accès aux données pour le calcul des itinéraires.
    """
    
    def obtenir_ville_par_id(self, db: Session, ville_id: int):
        """
        Récupère une ville depuis sa clé primaire.
        Cette méthode est utilisée pour vérifier l'existence des villes
        avant de lancer le calcul d'itinéraire.
        """
        return db.query(Ville).filter(Ville.id == ville_id).first()
    
    def construire_graphe(self, db: Session):
        """
        Construit la représentation du graphe routier sous forme de
        dictionnaire utilisable par l'algorithme de Dijkstra.
        
        Le format retourné est un dictionnaire où chaque clé est
        l'identifiant d'une ville et la valeur associée est une liste
        de tuples (id_voisin, cout) représentant les arêtes sortantes.
        
        Cette représentation correspond exactement à ce qu'attend la
        méthode calculer_chemin_optimal de la classe Dijkstra que
        nous avons implémentée précédemment.
        """
        # Récupération de toutes les villes pour initialiser le graphe
        villes = db.query(Ville).all()
        
        # Initialisation du graphe avec une liste vide pour chaque ville
        # Cela garantit que même les villes sans connexion apparaissent
        # dans le graphe, ce qui évite des erreurs dans Dijkstra
        graphe = {ville.id: [] for ville in villes}
        
        # Récupération de toutes les connexions routières
        connexions = db.query(ConnexionVille).all()
        
        # Ajout de chaque connexion comme arête sortante de sa ville de départ
        for connexion in connexions:
            graphe[connexion.ville_depart_id].append(
                (connexion.ville_destination_id, connexion.cout)
            )
        
        return graphe
    
    def obtenir_dictionnaire_villes(self, db: Session):
        """
        Construit un dictionnaire associant chaque identifiant de ville
        à son objet Ville complet, pour faciliter la reconstitution
        des informations détaillées dans la réponse de l'itinéraire.
        """
        villes = db.query(Ville).all()
        return {ville.id: ville for ville in villes}