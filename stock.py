from fastapi import APIRouter, HTTPException
import redis
import requests
import json
import os
import ssl

router = APIRouter()

# Configuration Redis sécurisée pour Render.com
REDIS_HOST = os.getenv("REDIS_HOST", "oregon-keyvalue.render.com")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "ggtghykhucJrY6ydXraugdn0A7m5bmPT")  # À sécuriser en prod

# Configuration TLS avancée
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE  # Désactive la vérification du certificat (pour développement seulement)

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=True,
    ssl_cert_reqs=None,  # Ne pas vérifier le certificat
    ssl_ca_certs=None,
    decode_responses=True
)

# Test de connexion immédiat
try:
    redis_client.ping()
    print("✅ Connexion Redis établie avec succès")
except redis.exceptions.ConnectionError as e:
    print(f"❌ Échec de la connexion Redis: {e}")
    raise RuntimeError("Impossible de se connecter à Redis") from e

# Configuration API Twelve Data
TWELVE_API_KEY = os.getenv("TWELVE_API_KEY", "votre_clé_api")  # À remplacer par votre vraie clé

@router.get("/data/stock/{symbol}", tags=["Stock"])
def get_stock_by_symbol(symbol: str):
    redis_key = f"stocks:latest:{symbol.upper()}"
    
    try:
        # Vérification de la connexion Redis
        if not redis_client.ping():
            raise HTTPException(status_code=500, detail="Service Redis indisponible")

        # Tentative de récupération depuis le cache
        if redis_client.exists(redis_key):
            raw_data = redis_client.get(redis_key)
            return json.loads(raw_data)

    except redis.exceptions.RedisError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur Redis: {str(e)}"
        )

    # Appel à l'API Twelve Data si non en cache
    API_URL = "https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol.upper(),
        "interval": "1day",
        "outputsize": 30,
        "apikey": TWELVE_API_KEY
    }

    try:
        response = requests.get(API_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "values" not in data:
            raise HTTPException(
                status_code=404,
                detail=data.get("message", "Symbole non trouvé ou limite d'API atteinte")
            )

        # Stockage en cache avec gestion d'erreur
        try:
            redis_client.set(
                redis_key,
                json.dumps(data["values"]),
                ex=21600  # 6 heures en secondes
            )
        except redis.exceptions.RedisError as e:
            print(f"⚠️ Impossible de mettre en cache: {e}")

        return data["values"]

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=502,
            detail=f"Erreur lors de l'appel à l'API Twelve Data: {str(e)}"
        )