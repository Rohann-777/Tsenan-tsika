from datetime import datetime
from sqlalchemy.orm import Session
from src.backend.models.modeles import Utilisateur
from src.backend.repositories.saisie_repository import SaisieRepository
from src.backend.repositories.prix_repository import PrixRepository
from src.backend.algorithms.rabin_karp import RabinKarp
from src.backend.algorithms.top_k import TopK


top_k_global = TopK(k=5)


class SaisieService:
    SEUIL_ALERTE_POURCENT = 20.0
    
    def __init__(self):
        self.repository = SaisieRepository()
        self.prix_repository = PrixRepository()
        self.rabin_karp = RabinKarp()
    
    def saisir_prix(
        self, db: Session, produit_id: int, ville_id: int,
        prix: float, agent_id: int
    ):
        agent = db.query(Utilisateur).filter(Utilisateur.id == agent_id).first()
        if not agent:
            return {"succes": False, "message": "Agent introuvable"}
        
        if agent.role == "agent" and agent.ville_assignee_id != ville_id:
            return {
                "succes": False,
                "message": "Vous ne pouvez saisir des prix que pour votre ville d'affectation."
            }

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
        
        rapports_recents = self.repository.lister_rapports_recents(db, heures=24)
        
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
        doublon_detecte = self.rabin_karp.verifier_doublon(
            nouveau_rapport_donnees, rapports_pour_comparaison
        )
        
        rapport_insere = self.repository.inserer_rapport(
            db, produit_id, ville_id, prix, agent_id, est_doublon=doublon_detecte
        )
        
        if doublon_detecte:
            return {
                "succes": False,
                "message": "Doublon détecté : ce rapport existe déjà dans les dernières 24 heures",
                "rapport_id": rapport_insere.id,
                "doublon_detecte": True,
                "alerte_declenchee": False
            }
        
        prix_marche = self.repository.inserer_prix_marche(
            db, produit_id, ville_id, prix, agent_id
        )
        
        prix_moyen_recent = self.repository.obtenir_prix_moyen_recent(
            db, produit_id, ville_id, jours=7
        )
        
        variation_pourcent = None
        alerte_declenchee = False
        
        if prix_moyen_recent and prix_moyen_recent > 0:
            variation_pourcent = ((prix - prix_moyen_recent) / prix_moyen_recent) * 100
            
            if variation_pourcent > 0:
                top_k_global.mettre_a_jour(produit_id, variation_pourcent)
                
                if variation_pourcent >= self.SEUIL_ALERTE_POURCENT:
                    self.repository.creer_alerte(db, produit_id, ville_id)
                    alerte_declenchee = True
            
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