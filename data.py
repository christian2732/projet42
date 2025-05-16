from fastapi import APIRouter, HTTPException
import redis
import json
import os

router = APIRouter()

# Connexion à Redis (nom du service dans Docker Compose ou localhost par défaut)
redis_host = os.getenv("REDIS_HOST", "redis_cache")  # ajuste selon ton environnement
redis_port = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

@router.get("/data/{ticker}", summary="Lire les données d’un titre depuis Redis", tags=["Data Visualization"])
def get_stock_data(ticker: str):
    key = f"stocks:latest:{ticker.upper()}"
    data = r.get(key)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Données introuvables pour le ticker '{ticker}'.")
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Erreur de décodage des données stockées.")
