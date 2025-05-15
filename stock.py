from fastapi import APIRouter
import redis
import requests
import json
import os

router = APIRouter()

# Connexion Redis (assume que le service s'appelle "redis" dans Docker)
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# Clé API Alpha Vantage (en variable d’environnement de préférence)
API_KEY = os.getenv("ALPHA_API_KEY", "TO4Y92A0HFPIZE1M")
API_URL = "https://www.alphavantage.co/query"

@router.get("/data/stock/{symbol}", tags=["Stock"])
def get_stock_by_symbol(symbol: str):
    redis_key = f"stocks:{symbol.upper()}"

    # Vérifie d'abord si les données sont déjà dans Redis
    if redis_client.exists(redis_key):
        raw_data = redis_client.get(redis_key)
        return json.loads(raw_data)

    # Sinon, appelle l'API Alpha Vantage
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol.upper(),
        "apikey": API_KEY,
        "outputsize": "compact"
    }

    response = requests.get(API_URL, params=params)

    if response.status_code != 200:
        return {"error": "Erreur lors de la récupération depuis Alpha Vantage."}

    data = response.json()

    if "Time Series (Daily)" not in data:
        return {"error": "Symbol non trouvé ou limite atteinte."}

    daily_data = data["Time Series (Daily)"]

    # Stocke les données dans Redis pour 6 heures
    redis_client.set(redis_key, json.dumps(daily_data), ex=6 * 3600)

    return daily_data
