import requests
import redis
import json
import os
from datetime import timedelta

# Connexion Redis (host et port à adapter selon ton environnement)
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# Récupérer la clé API depuis une variable d'environnement (plus sûr)
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "JRZ0NOET0V2NLA4S")  # valeur par défaut en cas d'absence
API_URL = "https://www.alphavantage.co/query"

PARAMS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "AAPL",
    "apikey": API_KEY,
    "outputsize": "compact"
}

def fetch_and_store_data():
    try:
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()

        data = response.json()

        # Cas limite API dépassée (message dans la clé 'Information')
        if "Information" in data:
            print("Limite API dépassée ou autre erreur :", data["Information"])
            # On ne remplace pas les données dans Redis pour garder l'ancien cache
            return False

        if "Time Series (Daily)" in data:
            daily_data = data["Time Series (Daily)"]
            # Stocker dans Redis avec expiration de 6h
            redis_client.set("stocks:latest", json.dumps(daily_data), ex=timedelta(hours=6))
            print("Données boursières récupérées et stockées dans Redis.")
            return True
        else:
            print("Erreur inattendue dans la réponse API :", data)
            return False

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête à l'API : {e}")
        return False

if __name__ == "__main__":
    fetch_and_store_data()
