
from fastapi import APIRouter, HTTPException
from collector import fetch_and_store_data
from redis_cache import redis_client

router = APIRouter()


@router.post("/ingest", summary="Lancer l’ingestion boursière", tags=["Data Ingestion"])



@router.post("/ingest/")
async def ingest_all():
    """Endpoint pour ingérer toutes les actions"""
    symbols = ["0xBTC/BTC", "0xBTC/ETH", "0xBTC/USD", "1000SATS/USD", "1INCH/BTC", "1INCH/INR", "1INCH/USD"]  # Liste complète
    await fetch_and_store_data(symbols)
    return {"status": "success", "message": f"Ingestion lancée pour {len(symbols)} symboles"}



