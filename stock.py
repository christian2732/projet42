from fastapi import APIRouter
import redis
import requests
import json
import os

router = APIRouter()

# Configuration Redis avec TLS (Render.com)
REDIS_HOST = os.getenv("REDIS_HOST", "oregon-keyvalue.render.com")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "ggtghykhucJrY6ydXraugdn0A7m5bmPT")
REDIS_USE_TLS = os.getenv("REDIS_USE_TLS", "true").lower() == "true"

# Connexion Redis
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=REDIS_USE_TLS,
    ssl_cert_reqs=None  # Ne pas vérifier les certificats TLS (à éviter en prod)
)

# Clé API Twelve Data
API_KEY = os.getenv("TWELVE_API_KEY", "your_twelve_data_api_key")  # À définir correctement !

@router.get("/data/stock/{symbol}", tags=["Stock"])
def get_stock_by_symbol(symbol: str):
    redis_key = f"stocks:latest:{symbol.upper()}"

    # Vérifie si les données sont en cache Redis
    if redis_client.exists(redis_key):
        raw_data = redis_client.get(redis_key)
        return json.loads(raw_data)

    # Construire l'URL API avec le symbol
    API_URL = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol.upper(),
        "interval": "1day",
        "outputsize": 30,
        "apikey": API_KEY
    }

    response = requests.get(API_URL, params=params)

    if response.status_code != 200:
        return {"error": f"Erreur API: {response.status_code}", "details": response.json()}

    data = response.json()

    if "values" not in data:
        return {"error": data.get("message", "Symbol non trouvé ou erreur API.")}

    # Mise en cache des données pour 6 heures
    redis_client.set(redis_key, json.dumps(data["values"]), ex=6 * 3600)

    return data["values"]
