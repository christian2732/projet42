# Objectif : Utilitaire pour lire/écrire dans Redis

import redis
import json
import os

# Connexion Redis (localhost ou docker hostname si réseau Docker)
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

redis_client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

def get_cache(key: str):
    """Retourne les données du cache si disponibles"""
    value = redis_client.get(key)
    if value:
        return json.loads(value)
    return None

def set_cache(key: str, value: dict, expiration: int = 300):
    """Met en cache des données pour expiration secondes (par défaut 5 minutes)"""
    redis_client.set(key, json.dumps(value), ex=expiration)
