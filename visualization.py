from fastapi import APIRouter, HTTPException, Query
import redis
import json
import os
import logging
from typing import List, Dict, Union

router = APIRouter()

# Configuration du logger
logger = logging.getLogger(__name__)

# Connexion Redis (configuration inchangée)
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

# Test de connexion (inchangé)
try:
    r.ping()
    logger.info("✅ Connexion Redis établie dans visualization")
except Exception as e:
    logger.error(f"❌ Échec de la connexion Redis: {e}")

def get_single_stock(ticker: str) -> Dict[str, Union[dict, str]]:
    """Helper function to get data for a single ticker"""
    key = f"stocks:latest:{ticker.upper()}"
    logger.info(f"Recherche des données pour la clé: {key}")
    
    data = r.get(key)
    if data is None:
        logger.warning(f"Aucune donnée trouvée pour la clé: {key}")
        return {"ticker": ticker, "error": "Données non disponibles"}
    
    try:
        return {"ticker": ticker, "data": json.loads(data)}
    except json.JSONDecodeError as e:
        logger.error(f"Erreur de décodage pour la clé {key}: {e}")
        return {"ticker": ticker, "error": "Données corrompues"}

@router.get("/data/{ticker}")
def get_stock_data(ticker: str):
    """Endpoint pour un seul ticker (compatibilité ascendante)"""
    result = get_single_stock(ticker)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result["data"]

@router.get("/data/")
def get_multiple_stocks(
    tickers: str = Query(..., description="Liste de symboles séparés par des virgules (ex: AAPL,MSFT,GOOGL)")
) -> Dict[str, Dict[str, Union[dict, str]]]:
    """Nouvel endpoint pour plusieurs tickers"""
    ticker_list = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    
    if not ticker_list:
        raise HTTPException(status_code=400, detail="Aucun ticker fourni")
    
    # Limiter le nombre de tickers pour éviter les abus
    if len(ticker_list) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 tickers par requête")
    
    results = {}
    for ticker in ticker_list:
        results[ticker] = get_single_stock(ticker)
    
    return {"results": results}