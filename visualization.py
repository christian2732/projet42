# Objectif : Récupérer les données boursières stockées dans Redis et les retourner au frontend
from fastapi import APIRouter, HTTPException
import redis
import json
# from app.security.jwt import get_current_user  # Authentification supprimée

router = APIRouter()
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

@router.get("/stocks", summary="Visualiser les données boursières", tags=["Visualisation"])
def get_stocks():
    data = redis_client.get("stocks:latest")
    if data is None:
        raise HTTPException(status_code=404, detail="Aucune donnée disponible. Veuillez lancer l’ingestion.")
    return json.loads(data)
