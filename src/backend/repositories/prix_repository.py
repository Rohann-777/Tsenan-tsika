from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from src.backend.models.modeles import PrixMarche, Produit, Ville


class PrixRepository:
    
    def lister_tous_les_prix(self, db: Session, limite: int = 100):
        return db.query(PrixMarche).order_by(
            PrixMarche.date_saisie.desc()
        ).limit(limite).all()
    
    def lister_prix_par_ville(self, db: Session, ville_id: int, limite: int = 50):
        return db.query(PrixMarche).filter(
            PrixMarche.ville_id == ville_id
        ).order_by(PrixMarche.date_saisie.desc()).limit(limite).all()
    
    def lister_prix_par_produit_et_ville(
        self, db: Session, produit_id: int, ville_id: int, jours: int = 30
    ):
        date_limite = datetime.now() - timedelta(days=jours)
        return db.query(PrixMarche).filter(
            PrixMarche.produit_id == produit_id,
            PrixMarche.ville_id == ville_id,
            PrixMarche.date_saisie >= date_limite
        ).order_by(PrixMarche.date_saisie.asc()).all()
    
    def lister_produits(self, db: Session):
        return db.query(Produit).order_by(Produit.nom_fr).all()
    
    def lister_villes(self, db: Session):
        return db.query(Ville).order_by(Ville.nom).all()
    
    def calculer_prix_moyens_recents(self, db: Session, jours: int = 30):
        date_limite = datetime.now() - timedelta(days=jours)
        produits = db.query(Produit).order_by(Produit.nom_fr).all()

        resultats = []
        for produit in produits:
            prix = db.query(PrixMarche).filter(
                PrixMarche.produit_id == produit.id,
                PrixMarche.date_saisie >= date_limite
            ).all()

            moyenne = None
            if prix:
                moyenne = round(sum(p.prix for p in prix) / len(prix), 2)

            resultats.append({
                "produit_id": produit.id,
                "produit_nom": produit.nom_fr,
                "unite": produit.unite,
                "prix_moyen": moyenne
            })
        return resultats