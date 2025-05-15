
import requests
import redis
import json
import os
from datetime import timedelta

# Connexion Redis
redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)

# Clé d'API Alpha Vantage (token)
API_KEY = "DZ86OSBDT5U9QPX8"
API_URL = "https://www.alphavantage.co/query"

# Paramètres de la requête
PARAMS = {
    "function": "TIME_SERIES_DAILY",  # Choisir le type de données (ici, série temporelle quotidienne)
    "symbol": "AAPL",  # Le symbole boursier (exemple ici avec Apple, change selon le besoin)
    "apikey": API_KEY,  # La clé d'API Alpha Vantage
    "outputsize": "compact"  # Récupérer uniquement les dernières 100 points de données
}

def fetch_and_store_data():
    try:
        # Effectuer la requête à l'API Alpha Vantage
        response = requests.get(API_URL, params=PARAMS)
        response.raise_for_status()  # Vérifie les erreurs de la requête
        
        # Extraire les données JSON de la réponse
        data = response.json()
        
        # Vérifier que les données sont dans le bon format
        if "Time Series (Daily)" in data:
            daily_data = data["Time Series (Daily)"]
            
            # Stocker les données dans Redis avec une expiration de 6 heures
            redis_client.set("stocks:latest", json.dumps(daily_data), ex=timedelta(hours=6))
            print("Données boursières récupérées et stockées dans Redis.")
        else:
            print("Erreur dans la récupération des données boursières:", data)
    
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête à l'API : {e}")

if __name__ == "__main__":
    fetch_and_store_data()