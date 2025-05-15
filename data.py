from fastapi import APIRouter, HTTPException
import redis
import json
import os

router = APIRouter()

# Connexion à Redis (nom du service dans Docker Compose)
redis_host = os.getenv("REDIS_HOST", "redis_cache")
r = redis.Redis(host=redis_host, port=6379, decode_responses=True)

@router.get("/data/{ticker}", summary="Lire les données d’un titre depuis Redis", tags=["Data Visualization"])
def get_stock_data(ticker: str):
    key = f"stock:{ticker.upper()}"
    data = r.get(key)
    if data is None:
        raise HTTPException(status_code=404, detail="Données introuvables pour ce ticker.")
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Erreur de décodage des données.")
