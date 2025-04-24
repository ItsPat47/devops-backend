from fastapi import FastAPI, Request
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from prometheus_client import REGISTRY
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
import json
import os
app = FastAPI()

API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", 8000))



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {
        "message": "Hello World",
        }

@app.get("/api/data")
async def get_data():
    return {"message": "vous êtes sur api/data"}

web_vitals_counter = Counter(
    'frontend_web_vitals_total',
    'Total des métriques web-vitals reçues',
    ['name']
)

@app.post("/metrics/client")
async def receive_metrics(request: Request):
    body = await request.body()
    try:
        data = json.loads(body)
        if 'name' in data:
            web_vitals_counter.labels(name=data['name']).inc()
            print(f"[✔] Reçu: {data['name']}")
    except Exception as e:
        print(f"[!] Erreur parsing JSON : {e}")
    return {"status": "ok"}

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(REGISTRY), media_type=CONTENT_TYPE_LATEST)