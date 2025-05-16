
from fastapi import APIRouter, HTTPException
from collector import fetch_and_store_data
from redis_cache import redis_client

router = APIRouter()


@router.post("/ingest", summary="Lancer l’ingestion boursière", tags=["Data Ingestion"])



@router.post("/ingest/")
async def ingest_all():
    """Endpoint pour ingérer toutes les actions"""
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]  # Liste complète
    await fetch_and_store_data(symbols)
    return {"status": "success", "message": f"Ingestion lancée pour {len(symbols)} symboles"}



