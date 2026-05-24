"""
Service de gestion des tokens JWT pour Tsenan'tsika.

Ce module encapsule toute la logique cryptographique liée aux tokens
JWT, à savoir leur création lors de la connexion d'un utilisateur,
leur vérification lors de chaque requête protégée, et l'extraction
des informations qu'ils contiennent.

L'utilisation de la bibliothèque python-jose suit les standards
établis pour la manipulation de JWT en Python et offre toutes les
garanties de sécurité nécessaires pour une application réelle.
"""

from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from src.backend.auth.config import SECRET_KEY, ALGORITHM, DUREE_TOKEN


class JwtService:
    """
    Service de manipulation des tokens JWT.
    
    Cette classe regroupe les opérations de création et de vérification
    des tokens d'authentification. Elle est utilisée par le service
    d'authentification principal et par le middleware de protection
    des endpoints.
    """
    
    def creer_token(self, donnees: dict) -> str:
        """
        Génère un nouveau token JWT contenant les données fournies.
        
        Les données passées en paramètre seront encodées dans le token
        et pourront être récupérées lors de sa vérification. On y stocke
        typiquement l'identifiant de l'utilisateur, son email, et son
        rôle pour pouvoir appliquer les contrôles d'accès sans avoir
        à interroger la base de données à chaque requête.
        
        La date d'expiration est automatiquement ajoutée pour limiter
        la durée de validité du token. Si quelqu'un volait un token,
        il ne pourrait l'utiliser que jusqu'à cette date d'expiration.
        """
        donnees_a_encoder = donnees.copy()
        
        # Ajout de la date d'expiration calculée à partir de la durée
        # configurée. Le champ "exp" est un nom standard reconnu par
        # les bibliothèques JWT pour la date d'expiration.
        expiration = datetime.utcnow() + DUREE_TOKEN
        donnees_a_encoder.update({"exp": expiration})
        
        # Génération du token signé cryptographiquement avec notre clé
        # secrète. Sans cette clé, personne ne peut créer de tokens valides.
        token = jwt.encode(donnees_a_encoder, SECRET_KEY, algorithm=ALGORITHM)
        return token
    
    def verifier_token(self, token: str) -> Optional[dict]:
        """
        Vérifie la validité d'un token et retourne les données qu'il contient.
        
        Cette méthode effectue plusieurs vérifications cruciales.
        Premièrement elle vérifie que la signature du token est correcte,
        ce qui prouve qu'il a bien été émis par notre serveur et qu'il
        n'a pas été modifié. Deuxièmement elle vérifie que le token n'a
        pas expiré. Si l'une de ces vérifications échoue, la méthode
        retourne None pour indiquer que le token est invalide.
        """
        try:
            donnees = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return donnees
        except JWTError:
            # La bibliothèque python-jose lève une JWTError pour toutes
            # les erreurs liées au token, qu'il s'agisse d'une signature
            # invalide, d'une expiration dépassée, ou d'un format incorrect.
            return None