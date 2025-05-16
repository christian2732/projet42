import os
import redis

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))
redis_password = os.getenv("REDIS_PASSWORD", None)
use_tls = os.getenv("REDIS_USE_TLS", "false").lower() == "true"

redis_client = redis.Redis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    decode_responses=True,
    ssl=use_tls
)

def test_redis_connection():
    try:
        redis_client.ping()
        print("✅ Connexion Redis TLS réussie !")
    except redis.exceptions.AuthenticationError:
        print("❌ Erreur : mot de passe Redis incorrect ou authentification requise.")
    except redis.exceptions.ConnectionError:
        print("❌ Erreur : impossible de se connecter à Redis.")

if __name__ == "__main__":
    test_redis_connection()
