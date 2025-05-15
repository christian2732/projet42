import jwt
from datetime import datetime, timedelta
from typing import Dict

# Clé secrète utilisée pour signer le JWT
SECRET_KEY = "ma_clé_secrète"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expirant après 30 minutes

def create_access_token(data: Dict):
    """
    Crée un token JWT avec une durée d'expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
