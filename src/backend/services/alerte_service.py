"""
Service métier pour le tableau de bord des alertes dans Tsenan'tsika.

Ce module orchestre la récupération et l'agrégation de toutes les
informations affichées sur le tableau de bord, en combinant les
données persistantes des alertes en base et l'état en mémoire du
classement Top-k qui est maintenu par le service de saisie.

L'agrégation centralisée permet de présenter une vue cohérente du
système aux analystes et aux citoyens, en évitant que le frontend
ait à coordonner plusieurs sources de données différentes.
"""

from sqlalchemy.orm import Session
from src.backend.repositories.alerte_repository import AlerteRepository
from src.backend.repositories.prix_repository import PrixRepository
from src.backend.services.saisie_service import top_k_global


class AlerteService:
    """
    Service métier pour la consultation du tableau de bord.
    """
    
    def __init__(self):
        """
        Initialise le service avec ses dépendances.
        """
        self.repository = AlerteRepository()
        self.prix_repository = PrixRepository()
    
    def obtenir_tableau_bord(self, db: Session):
        """
        Construit la vue complète du tableau de bord en agrégeant les
        alertes récentes et le classement Top-k actuel.
        
        Cette méthode démontre l'intégration de plusieurs sources de
        données pour produire une réponse cohérente. Les alertes sont
        enrichies avec les noms du produit et de la ville pour faciliter
        l'affichage, et le Top-k est récupéré directement depuis la
        mémoire vive du service de saisie.
        """
        # Récupération des alertes brutes depuis la base de données
        alertes_brutes = self.repository.lister_alertes_recentes(db, jours=7, limite=20)
        nombre_alertes = self.repository.compter_alertes_actives(db, jours=7)
        
        # Récupération des produits et villes pour l'enrichissement
        produits = self.prix_repository.lister_produits(db)
        villes = self.prix_repository.lister_villes(db)
        
        # Construction de dictionnaires pour la recherche rapide
        # Cette approche évite de faire une requête par alerte ce qui
        # serait inefficace en cas de grand nombre d'alertes à afficher
        dictionnaire_produits = {p.id: p for p in produits}
        dictionnaire_villes = {v.id: v for v in villes}
        
        # Enrichissement des alertes avec les noms du produit et de la ville
        alertes_enrichies = []
        for alerte in alertes_brutes:
            produit = dictionnaire_produits.get(alerte.produit_id)
            ville = dictionnaire_villes.get(alerte.ville_id)
            
            if produit and ville:
                alertes_enrichies.append({
                    "id": alerte.id,
                    "date": alerte.date,
                    "produit_id": alerte.produit_id,
                    "produit_nom": produit.nom_fr,
                    "ville_id": alerte.ville_id,
                    "ville_nom": ville.nom
                })
        
        # Récupération du classement Top-k depuis l'instance globale
        # maintenue par le service de saisie
        top_5_brut = top_k_global.get_top_5_hausses()
        
        # Enrichissement du Top-k avec les noms des produits
        top_5_enrichi = []
        for rang, (variation, produit_id) in enumerate(top_5_brut, start=1):
            produit = dictionnaire_produits.get(produit_id)
            if produit:
                top_5_enrichi.append({
                    "produit_id": produit_id,
                    "produit_nom": produit.nom_fr,
                    "variation_pourcent": round(variation, 2),
                    "rang": rang
                })
        
        return {
            "nombre_alertes_actives": nombre_alertes,
            "alertes_recentes": alertes_enrichies,
            "top_5_hausses": top_5_enrichi
        }