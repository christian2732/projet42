import requests
import json
import os
from datetime import timedelta
from redis_cache import redis_client  # Import du client Redis configuré avec TLS et password

API_KEY = os.getenv("API_TOKEN", "fa3e77e6afe249bdbaddc937a5f6489e")
API_URL = "https://api.twelvedata.com/time_series"

def fetch_and_store_data(symbol="AAPL"):
    cache_key = f"stocks:latest:{symbol}"
    
    if redis_client.exists(cache_key):
        print("✅ Données chargées depuis Redis.")
        return json.loads(redis_client.get(cache_key))

    params = {
        "symbol": symbol,
        "interval": "1day",
        "outputsize": 30,
        "apikey": API_KEY
    }

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if "values" in data:
            redis_client.set(cache_key, json.dumps(data["values"]), ex=timedelta(hours=6))
            print("✅ Données récupérées depuis Twelve Data et stockées dans Redis.")
            return data["values"]
        else:
            print("❌ Erreur dans la réponse Twelve Data :", data)
            return None

    except requests.RequestException as e:
        print(f"❌ Erreur requête Twelve Data : {e}")
        return None

if __name__ == "__main__":
    fetch_and_store_data()
