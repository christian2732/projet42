from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import os
from dotenv import load_dotenv
from redis_cache import redis_client


# Importer directement les fichiers Python situés à la racine
import ingest
import visualization
import stock  # ⚠️ Assurez-vous que ce fichier contient un APIRouter nommé `router`

# ─── Création de l'application FastAPI ─────────────────────────────────────────
app = FastAPI(
    title="Bourse API 🚀",
    description="API de collecte et visualisation des indices boursiers",
    version="1.0.0",
)

# ─── Chargement des variables d’environnement ──────────────────────────────────
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

# ─── Métriques Prometheus ──────────────────────────────────────────────────────
REQUEST_COUNT = Counter("request_count", "Nombre de requêtes HTTP", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Latence des requêtes", ["method", "endpoint"])

@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    REQUEST_COUNT.labels(request.method, request.url.path).inc()
    REQUEST_LATENCY.labels(request.method, request.url.path).observe(process_time)
    return response

@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    """Exposer les métriques Prometheus à /metrics"""
    return PlainTextResponse(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/")
def root():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API Bourse 🚀. Rendez-vous sur /docs pour explorer les endpoints."
    }

# ─── Inclusion des routes ──────────────────────────────────────────────────────
app.include_router(ingest.router, prefix="/ingest", tags=["Data Ingestion"])
app.include_router(visualization.router, prefix="/visualization", tags=["Data Visualization"])
app.include_router(stock.router, tags=["Stock"])
