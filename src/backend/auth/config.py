"""
Configuration du système d'authentification JWT pour Tsenan'tsika.

Ce module centralise tous les paramètres techniques du système
d'authentification, ce qui facilite leur modification éventuelle
sans avoir à parcourir tout le code à la recherche de constantes
dispersées.
"""

import os
from datetime import timedelta

# Clé secrète utilisée pour signer les tokens JWT.
# En production, cette clé devrait être stockée dans une variable
# d'environnement et jamais commitée dans le dépôt Git car sa
# divulgation permettrait à un attaquant de forger de faux tokens.
# Pour notre prototype, nous la mettons directement dans le code
# avec une note expliquant cette limitation.
SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "tsenantsika_secret_key_a_changer_en_production_2026"
)

# Algorithme de signature utilisé pour les tokens.
# HS256 est l'algorithme HMAC SHA-256 qui est le standard pour
# les applications de taille moyenne. Il offre un bon équilibre
# entre sécurité et performance.
ALGORITHM = "HS256"

# Durée de validité d'un token avant son expiration.
# 24 heures est un bon compromis entre sécurité et confort utilisateur.
# Un token plus court demanderait à l'utilisateur de se reconnecter
# trop fréquemment, tandis qu'un token trop long augmenterait le
# risque en cas de vol du token.
DUREE_TOKEN = timedelta(hours=24)

# Préfixe utilisé dans l'en-tête HTTP Authorization.
# Le format standard est "Bearer suivi du token", où Bearer signifie
# que celui qui présente le token est considéré comme son porteur
# légitime, sans vérification supplémentaire d'identité.
PREFIXE_TOKEN = "Bearer"