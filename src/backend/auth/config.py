import os
from datetime import timedelta

SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "tsenantsika_secret_key_a_changer_en_production_2026"
)

ALGORITHM = "HS256"

DUREE_TOKEN = timedelta(hours=24)

PREFIXE_TOKEN = "Bearer"