"""
Script utilitaire pour recréer entièrement les tables de la base de données.

Ce script supprime toutes les tables existantes et les recrée avec
la structure définie dans les modèles SQLAlchemy. Toutes les données
existantes sont perdues lors de cette opération.

À utiliser uniquement en développement, jamais en production où il
faudrait préférer une vraie migration de schéma.
"""

from src.backend.config.database import engine, Base
from src.backend.models.modeles import (
    Utilisateur, Produit, Ville, ConnexionVille,
    PrixMarche, RapportPrix, Alerte
)


def recreer_toutes_les_tables():
    """
    Supprime toutes les tables et les recrée avec la nouvelle structure.
    
    L'ordre est important. On supprime d'abord car les nouvelles tables
    ne pourraient pas être créées si les anciennes existent avec une
    structure différente. La méthode drop_all gère automatiquement les
    contraintes de clés étrangères en supprimant les tables dans le
    bon ordre.
    """
    print("Suppression des tables existantes...")
    Base.metadata.drop_all(bind=engine)
    print("Tables supprimées avec succès.")
    
    print("Création des nouvelles tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès.")
    
    print("\nLa structure de la base de données est maintenant à jour.")
    print("Tu peux maintenant exécuter le script de génération de données.")


if __name__ == "__main__":
    recreer_toutes_les_tables()