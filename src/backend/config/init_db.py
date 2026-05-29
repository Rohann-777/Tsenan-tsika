from src.backend.config.database import engine, Base
from src.backend.models import modeles


def initialiser_base_de_donnees():
    print("Création des tables dans la base de données tsenantsika_db...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès !")
    print("\nListe des tables créées :")
    for table_name in Base.metadata.tables.keys():
        print(f"  - {table_name}")


if __name__ == "__main__":
    initialiser_base_de_donnees()