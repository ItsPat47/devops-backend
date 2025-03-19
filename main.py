from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
app = FastAPI()

API_HOST = os.getenv("API_HOST", "localhost")
API_PORT = int(os.getenv("API_PORT", 8000))



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
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