"""
Script d'initialisation de la base de données PostgreSQL pour Tsenan'tsika.

Ce script crée toutes les tables définies dans les modèles SQLAlchemy
en se connectant à la base de données configurée. Il est conçu pour
être exécuté manuellement avant le premier lancement de l'application
ou après toute modification du schéma.

Pour exécuter ce script depuis la racine du projet :
    python -m src.backend.config.init_db
"""

from src.backend.config.database import engine, Base
# L'import des modèles est nécessaire pour que SQLAlchemy connaisse
# toutes les tables à créer. Sans cet import, Base.metadata.create_all
# ne créerait rien car il ne saurait pas quelles tables existent.
from src.backend.models import modeles


def initialiser_base_de_donnees():
    """
    Crée toutes les tables définies dans les modèles SQLAlchemy.
    
    Si les tables existent déjà, SQLAlchemy ne les recrée pas et
    n'altère pas leur structure existante. Pour faire une mise à
    jour de schéma en production, il faudrait utiliser un outil
    de migration comme Alembic, mais pour notre prototype, la
    création initiale suffit.
    """
    print("Création des tables dans la base de données tsenantsika_db...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès !")
    print("\nListe des tables créées :")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")


if __name__ == "__main__":
    initialiser_base_de_donnees()