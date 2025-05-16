# Objectif : Récupérer les données boursières stockées dans Redis et les retourner au frontend
from fastapi import APIRouter, HTTPException
import redis
import json
import os  # Pour lire les variables d'environnement

router = APIRouter()

# Connexion à Redis via les variables d'environnement définies sur Render
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),  # fallback utile en local
    port=int(os.getenv("REDIS_PORT", 6379)),
    password=os.getenv("REDIS_PASSWORD"),
    decode_responses=True
)

@router.get("/stocks", summary="Visualiser les données boursières", tags=["Visualisation"])
def get_stocks():
    data = redis_client.get("stocks:latest")
    if data is None:
        raise HTTPException(status_code=404, detail="Aucune donnée disponible. Veuillez lancer l’ingestion.")
    return json.loads(data)
