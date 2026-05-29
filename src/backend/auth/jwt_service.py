from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from src.backend.auth.config import SECRET_KEY, ALGORITHM, DUREE_TOKEN


class JwtService:
    
    def creer_token(self, donnees: dict) -> str:
        donnees_a_encoder = donnees.copy()
        
        expiration = datetime.utcnow() + DUREE_TOKEN
        donnees_a_encoder.update({"exp": expiration})
        
        token = jwt.encode(donnees_a_encoder, SECRET_KEY, algorithm=ALGORITHM)
        return token
    
    def verifier_token(self, token: str) -> Optional[dict]:
        try:
            donnees = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return donnees
        except JWTError:
            return None