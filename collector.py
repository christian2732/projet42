import requests
import redis
import json
import os
from datetime import timedelta

# Connexion à Redis (adaptée pour Docker Compose : nom de service Redis = "redis")
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# Clé API Alpha Vantage depuis une variable d’environnement
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "JRZ0NOET0V2NLA4S")
API_URL = "https://www.alphavantage.co/query"

PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "AAPL",
    "apikey": API_KEY,
    "outputsize": "compact"
}

def fetch_and_store_data():
    cache_key = "stocks:latest"

    # Vérifie si les données sont déjà présentes dans Redis
    cached_data = redis_client.get(cache_key)
    if cached_data:
        print("✅ Données récupérées depuis le cache Redis.")
        return {
            "success": True,
            "source": "cache",
            "data": json.loads(cached_data)
        }

    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()
        data = response.json()

        # Cas limite atteinte ou erreur connue
        if "Information" in data or "Note" in data:
            error_msg = data.get("Information") or data.get("Note")
            print(f"⚠️ Limite API atteinte ou autre problème : {error_msg}")
            return {
                "success": False,
                "error": error_msg
            }

        # Si les données sont valides
        if "Time Series (Daily)" in data:
            daily_data = data["Time Series (Daily)"]
            redis_client.set(cache_key, json.dumps(daily_data), ex=timedelta(hours=6))
            print("✅ Données boursières récupérées et stockées dans Redis.")
            return {
                "success": True,
                "source": "api",
                "data": daily_data
            }

        # Réponse inattendue
        print("❌ Erreur inattendue dans la réponse de l'API :", data)
        return {
            "success": False,
            "error": "Structure de réponse inattendue"
        }

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur de requête API : {e}")
        return {
            "success": False,
            "error": str(e)
        }

if __name__ == "__main__":
    result = fetch_and_store_data()
    if result["success"]:
        print(f"✅ Succès (données depuis : {result['source']})")
    else:
        print(f"❌ Échec : {result['error']}")
