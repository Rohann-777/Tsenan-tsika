from sqlalchemy.orm import Session
from src.backend.repositories.alerte_repository import AlerteRepository
from src.backend.repositories.prix_repository import PrixRepository
from src.backend.services.saisie_service import top_k_global


class AlerteService:
    
    def __init__(self):
        self.repository = AlerteRepository()
        self.prix_repository = PrixRepository()
    
    def obtenir_tableau_bord(self, db: Session):
        alertes_brutes = self.repository.lister_alertes_recentes(db, jours=7, limite=20)

        produits = self.prix_repository.lister_produits(db)
        villes = self.prix_repository.lister_villes(db)

        dictionnaire_produits = {p.id: p for p in produits}
        dictionnaire_villes = {v.id: v for v in villes}

        alertes_uniques = {}
        for alerte in alertes_brutes:
            cle = (alerte.produit_id, alerte.ville_id)
            if cle not in alertes_uniques or alerte.date > alertes_uniques[cle].date:
                alertes_uniques[cle] = alerte

        alertes_triees = sorted(
            alertes_uniques.values(),
            key=lambda a: a.date,
            reverse=True
        )

        nombre_alertes = len(alertes_triees)

        alertes_enrichies = []
        for alerte in alertes_triees:
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

        top_5_brut = top_k_global.get_top_5_hausses()

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