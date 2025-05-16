
from fastapi import APIRouter, HTTPException
from collector import fetch_and_store_data
from redis_cache import redis_client

router = APIRouter()


@router.post("/ingest", summary="Lancer l’ingestion boursière", tags=["Data Ingestion"])

def ingest_data():
    try:
        fetch_and_store_data()
        return {"status": "success", "message": "Données collectées avec succès."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



