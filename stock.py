import redis
import ssl

# Configuration pour Redis Cloud
REDIS_HOST = "redis-17982.c277.us-east-1-3.ec2.redns.redis-cloud.com"
REDIS_PORT = 17982
REDIS_PASSWORD = "ggtghykhucJrY6ydXraugdn0A7m5bmPT"  # Remplacez par votre vrai mot de passe

# Configuration SSL personnalisée
ssl_context = ssl.SSLContext()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE  # Désactive la vérification du certificat (pour développement)

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    ssl=True,
    ssl_cert_reqs=None,  # Pas de vérification de certificat
    ssl_ca_certs=None,
    decode_responses=True
)

# Test de connexion avec gestion d'erreur améliorée
try:
    if redis_client.ping():
        print("✅ Connexion Redis établie avec succès")
    else:
        raise RuntimeError("La commande PING a échoué")
except Exception as e:
    print(f"❌ Échec de la connexion Redis: {str(e)}")
    # Ne pas arrêter l'application ici, mais logger l'erreur