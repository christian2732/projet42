from fastapi import APIRouter, HTTPException
import redis
import json
import os
import logging

router = APIRouter()

# Configuration du logger
logger = logging.getLogger(__name__)

# Connexion Redis (même configuration que dans ingest.py)
redis_host = os.getenv("REDIS_HOST", "redis_cache")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_password = os.getenv("REDIS_PASSWORD")
use_tls = os.getenv("REDIS_USE_TLS", "false").lower() == "true"

r = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True,
    ssl=use_tls
)

# Test de connexion au démarrage
try:
    r.ping()
    logger.info("✅ Connexion Redis établie dans visualization")
except Exception as e:
    logger.error(f"❌ Échec de la connexion Redis: {e}")

@router.get("/data/{ticker}")
def get_stock_data(ticker: str):
    # Utilisez la même clé que dans ingest.py
    key = f"stocks:latest:{ticker.upper()}"
    logger.info(f"Recherche des données pour la clé: {key}")
    
    data = r.get(key)
    if data is None:
        logger.warning(f"Aucune donnée trouvée pour la clé: {key}")
        raise HTTPException(
            status_code=404,
            detail="Aucune donnée disponible. Veuillez lancer l'ingestion."
        )
    
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de décodage pour la clé {key}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur de décodage des données stockées."
        )