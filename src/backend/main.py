"""
Point d'entrée principal de l'application FastAPI pour Tsenan'tsika.

Ce module initialise l'application FastAPI, configure les middlewares
nécessaires comme CORS pour permettre les requêtes depuis le frontend,
et enregistre toutes les routes de l'application.

Pour lancer l'application en mode développement, exécute depuis la
racine du projet la commande suivante avec l'environnement virtuel activé :

    uvicorn src.backend.main:app --reload

L'application sera accessible sur http://localhost:8000
La documentation interactive Swagger sera disponible sur http://localhost:8000/docs
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.routes import prix_routes


# Création de l'application FastAPI avec ses métadonnées
app = FastAPI(
    title="Tsenan'tsika API",
    description="""
    Système national de surveillance des prix alimentaires de Madagascar.
    
    Cette API permet de :
    - Consulter les prix marché en temps réel
    - Détecter automatiquement les anomalies de prix
    - Calculer les itinéraires d'approvisionnement optimaux
    - Gérer les utilisateurs et leurs permissions
    """,
    version="1.0.0"
)


# Configuration CORS pour permettre les requêtes depuis le frontend React
# En production, il faudrait restreindre les origines autorisées aux seuls
# domaines de confiance, mais pour le développement on autorise tout
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# Enregistrement des routeurs de l'application
app.include_router(prix_routes.router)


@app.get("/")
def racine():
    """
    Endpoint racine qui confirme que l'API est fonctionnelle.
    """
    return {
        "message": "Bienvenue sur l'API Tsenan'tsika",
        "version": "1.0.0",
        "documentation": "/docs"
    }