"""
Service métier pour la saisie de prix dans Tsenan'tsika.

Ce module orchestre le pipeline complet de traitement d'une nouvelle
saisie de prix, depuis la vérification de doublon par Rabin-Karp
jusqu'à la mise à jour potentielle du Top-k qui peut déclencher
une alerte. Ce service est le cœur de la logique métier du système
et correspond précisément au flux modélisé dans le diagramme de
séquence F1.

Le service maintient une instance persistante du Top-k qui accumule
les variations de prix dans une session d'exécution. En production,
cet état serait persisté entre les redémarrages du serveur via un
mécanisme de cache ou de stockage dédié.
"""

from datetime import datetime
from sqlalchemy.orm import Session
from src.backend.repositories.saisie_repository import SaisieRepository
from src.backend.repositories.prix_repository import PrixRepository
from src.backend.algorithms.rabin_karp import RabinKarp
from src.backend.algorithms.top_k import TopK


# Instance globale du Top-k partagée entre les requêtes
# Cette approche simple convient pour notre prototype mais nécessiterait
# un mécanisme plus sophistiqué en production avec plusieurs serveurs
top_k_global = TopK(k=5)


class SaisieService:
    """
    Service métier pour le pipeline de saisie de prix.
    """
    
    # Seuil de variation en pourcentage au-delà duquel une alerte est déclenchée
    # Une variation de plus de vingt pour cent par rapport à la moyenne récente
    # est considérée comme anormale et mérite d'être signalée aux analystes
    SEUIL_ALERTE_POURCENT = 20.0
    
    def __init__(self):
        """
        Initialise le service avec ses dépendances.
        """
        self.repository = SaisieRepository()
        self.prix_repository = PrixRepository()
        self.rabin_karp = RabinKarp()
    
    def saisir_prix(
        self, db: Session, produit_id: int, ville_id: int,
        prix: float, agent_id: int
    ):
        """
        Traite une nouvelle saisie de prix en exécutant tout le pipeline
        de validation et de mise à jour.
        
        Cette méthode implémente exactement le flux du diagramme de
        séquence F1, à savoir vérification de doublon par Rabin-Karp,
        insertion en base si valide, et mise à jour du Top-k qui peut
        déclencher une alerte.
        """
        # Étape 1 : Préparer les données du nouveau rapport pour Rabin-Karp
        # On récupère d'abord les noms du produit et de la ville pour
        # construire la chaîne normalisée comparable avec les rapports existants
        produits = self.prix_repository.lister_produits(db)
        villes = self.prix_repository.lister_villes(db)
        
        produit = next((p for p in produits if p.id == produit_id), None)
        ville = next((v for v in villes if v.id == ville_id), None)
        
        if not produit or not ville:
            return {
                "succes": False,
                "message": "Produit ou ville inexistant",
                "doublon_detecte": False,
                "alerte_declenchee": False
            }
        
        nouveau_rapport_donnees = {
            "produit": produit.nom_fr,
            "ville": ville.nom,
            "prix": prix,
            "date_heure": datetime.now()
        }
        
        # Étape 2 : Récupérer les rapports récents pour la comparaison
        rapports_recents = self.repository.lister_rapports_recents(db, heures=24)
        
        # Transformation des rapports en format compatible avec Rabin-Karp
        rapports_pour_comparaison = []
        for rapport in rapports_recents:
            produit_rapport = next(
                (p for p in produits if p.id == rapport.produit_id), None
            )
            ville_rapport = next(
                (v for v in villes if v.id == rapport.ville_id), None
            )
            if produit_rapport and ville_rapport:
                rapports_pour_comparaison.append({
                    "produit": produit_rapport.nom_fr,
                    "ville": ville_rapport.nom,
                    "prix": rapport.prix,
                    "date_heure": rapport.date_heure
                })
        
        # Étape 3 : Détection de doublon par Rabin-Karp
        doublon_detecte = self.rabin_karp.verifier_doublon(
            nouveau_rapport_donnees, rapports_pour_comparaison
        )
        
        # Étape 4 : Insertion du rapport (avec ou sans flag doublon)
        rapport_insere = self.repository.inserer_rapport(
            db, produit_id, ville_id, prix, agent_id, est_doublon=doublon_detecte
        )
        
        # Si doublon, on s'arrête là sans créer de PrixMarche
        if doublon_detecte:
            return {
                "succes": False,
                "message": "Doublon détecté : ce rapport existe déjà dans les dernières 24 heures",
                "rapport_id": rapport_insere.id,
                "doublon_detecte": True,
                "alerte_declenchee": False
            }
        
        # Étape 5 : Insertion du PrixMarche validé
        prix_marche = self.repository.inserer_prix_marche(
            db, produit_id, ville_id, prix, agent_id
        )
        
        # Étape 6 : Calcul de la variation par rapport à la moyenne récente
        prix_moyen_recent = self.repository.obtenir_prix_moyen_recent(
            db, produit_id, ville_id, jours=7
        )
        
        variation_pourcent = None
        alerte_declenchee = False
        
        if prix_moyen_recent and prix_moyen_recent > 0:
            variation_pourcent = ((prix - prix_moyen_recent) / prix_moyen_recent) * 100
            
            # Mise à jour du Top-k uniquement si la variation est positive
            # car le Top-k a pour vocation de classer les hausses de prix anormales.
            # Les baisses de prix ne représentent pas des anomalies à signaler dans
            # le contexte de surveillance contre la spéculation et les pénuries.
            if variation_pourcent > 0:
                top_k_global.mettre_a_jour(produit_id, variation_pourcent)
                
                # Déclenchement d'alerte uniquement pour les hausses dépassant le seuil
                if variation_pourcent >= self.SEUIL_ALERTE_POURCENT:
                    self.repository.creer_alerte(db, produit_id, ville_id)
                    alerte_declenchee = True
            
            # Étape 8 : Déclenchement d'alerte si la variation dépasse le seuil
            if variation_pourcent >= self.SEUIL_ALERTE_POURCENT:
                self.repository.creer_alerte(db, produit_id, ville_id)
                alerte_declenchee = True
        
        return {
            "succes": True,
            "message": "Prix saisi avec succès",
            "rapport_id": rapport_insere.id,
            "prix_marche_id": prix_marche.id,
            "doublon_detecte": False,
            "alerte_declenchee": alerte_declenchee,
            "variation_pourcent": round(variation_pourcent, 2) if variation_pourcent else None
        }