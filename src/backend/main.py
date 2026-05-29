from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.backend.routes import (
    prix_routes, itineraire_routes, saisie_routes,
    alerte_routes, auth_routes, admin_routes, export_routes
)


app = FastAPI(
    title="Tsenan'tsika API",
    description="""
    Système national de surveillance des prix alimentaires de Madagascar.
    """,
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(auth_routes.router)
app.include_router(prix_routes.router)
app.include_router(itineraire_routes.router)
app.include_router(saisie_routes.router)
app.include_router(alerte_routes.router)
app.include_router(admin_routes.router)
app.include_router(export_routes.router)


@app.get("/")
def racine():
    return {
        "message": "Bienvenue sur l'API Tsenan'tsika",
        "version": "1.0.0",
        "documentation": "/docs"
    }