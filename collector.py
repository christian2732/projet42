import requests
import json
import os
from datetime import timedelta
from redis_cache import redis_client  # Import du client Redis configuré avec TLS et password
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


API_KEY = os.getenv("API_TOKEN", "fa3e77e6afe249bdbaddc937a5f6489e")
API_URL = "https://api.twelvedata.com/time_series"


async def fetch_and_store_data(symbols: list = ["0xBTC/BTC", "0xBTC/ETH", "0xBTC/USD", "1000SATS/USD", "1INCH/BTC", "1INCH/INR", "1INCH/USD"]):
    
    for symbol in symbols:
        cache_key = f"stocks:latest:{symbol.upper()}"
        
        params = {
            "symbol": symbol,
            "interval": "1day",
            "outputsize": 30,
            "apikey": os.getenv("API_TOKEN")
        }

        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "values" in data:
                redis_client.set(cache_key, json.dumps(data["values"]), ex=timedelta(hours=6))
                logger.info(f"✅ Données stockées pour {symbol}")
            else:
                logger.error(f"❌ Format invalide pour {symbol}: {data}")

        except Exception as e:
            logger.error(f"❌ Erreur pour {symbol}: {str(e)}")

if __name__ == "__main__":
    fetch_and_store_data()
