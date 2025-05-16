from fastapi import APIRouter, Depends
from index_service import get_mock_indices
from redis_cache import get_cache, set_cache
from redis_cache import redis_client

#from app.auth.auth_bearer import JWTBearer

router = APIRouter()

@router.get("/indices", dependencies=[Depends(JWTBearer())], tags=["Indices"])
def read_indices():
    # Tenter d’obtenir les données depuis Redis
    cache_key = "stock_indices"
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    # Sinon on appelle le service et on met en cache
    indices = get_mock_indices()
    serialized = [index.dict() for index in indices]
    set_cache(cache_key, serialized, expiration=300)
    return serialized
