from fastapi import APIRouter
from jwt_handler import create_access_token  # ✅ Chemin corrigé

router = APIRouter()

@router.post("/login", summary="Connexion simple pour obtenir un token")
def login(username: str, password: str):
    # ⚠️ Authentification simplifiée — à sécuriser dans un vrai projet
    if username == "admin" and password == "secret":
        token = create_access_token({"user": username})
        return {"access_token": token}
    return {"error": "Invalid credentials"}
