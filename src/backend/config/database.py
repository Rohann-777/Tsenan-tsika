"""
Configuration de la connexion à la base de données PostgreSQL pour Tsenan'tsika.

Ce module établit la connexion à la base de données et fournit les
outils nécessaires pour interagir avec elle de manière sécurisée et
performante via SQLAlchemy. Il sert de point central pour la gestion
des sessions de base de données utilisées par tous les repositories.

L'approche utilisée suit les bonnes pratiques de FastAPI avec
SQLAlchemy, à savoir l'injection de dépendance des sessions et
la fermeture automatique des connexions après chaque requête.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

# URL de connexion à la base de données PostgreSQL
# Le format est postgresql://utilisateur:motdepasse@hote:port/nom_base
# Pour le développement local, on utilise les paramètres par défaut de PostgreSQL
# avec l'utilisateur postgres et le mot de passe défini lors de l'installation
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/tsenantsika_db")


# L'engine est l'interface de bas niveau de SQLAlchemy avec la base de données
# Il gère le pool de connexions et la communication avec PostgreSQL
# Le paramètre echo permet d'afficher les requêtes SQL générées dans la console,
# ce qui est très utile pendant le développement pour comprendre ce qui se passe
engine = create_engine(DATABASE_URL, echo=True)


# SessionLocal est une factory qui crée des sessions de base de données
# Une session est un espace de travail temporaire qui contient les objets
# que tu manipules et qui gère les transactions avec la base
# autocommit=False signifie que les changements ne sont sauvegardés qu'après un commit explicite
# autoflush=False signifie que les requêtes en attente ne sont pas envoyées automatiquement
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base est la classe parente de tous les modèles SQLAlchemy
# Chaque modèle qui hérite de Base sera automatiquement enregistré
# dans le système de mapping ORM
Base = declarative_base()


def get_db():
    """
    Fonction utilitaire qui fournit une session de base de données
    aux endpoints FastAPI via le système d'injection de dépendances.
    
    Cette fonction utilise un générateur Python avec yield pour
    s'assurer que la session est toujours fermée proprement après
    utilisation, même si une erreur survient pendant le traitement
    de la requête. C'est le pattern recommandé par FastAPI pour
    gérer les ressources de base de données.
    
    L'utilisation typique dans un endpoint est la suivante :
    
        @app.get("/items")
        def lire_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    
    FastAPI appellera automatiquement get_db pour chaque requête,
    fournira la session au endpoint, puis fermera la session
    quand le endpoint termine son exécution.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()