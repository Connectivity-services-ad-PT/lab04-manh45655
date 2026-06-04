from fastapi import FastAPI, Header, HTTPException, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
import os

app = FastAPI()

db = {}

AUTH_TOKEN = os.getenv("AUTH_TOKEN", "secret-token")

class Reading(BaseModel):
    device_id: str
    metric: str
    value: float = Field(..., ge=-40, le=80)
    unit: str
    timestamp: str

# Fix 1: thêm version
@app.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    return {"status": "ok", "service": "iot-app", "version": os.getenv("SERVICE_VERSION", "0.4.0")}

# Fix 2: x_api_key Optional để validate auth trước, Fix 5: warning header
@app.post("/readings", status_code=status.HTTP_201_CREATED)
def create_reading(
    data: Reading,
    response: Response,
    x_api_key: Optional[str] = Header(default=None)
):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="Missing API Key")
    if x_api_key != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    reading_id = str(uuid.uuid4())
    db[reading_id] = data

    # Fix 5: thêm warning header khi value = 80
    if data.value >= 80:
        response.headers["X-Warning"] = "High temperature detected"

    return {"reading_id": reading_id, **data.model_dump()}

# Fix 3: thêm endpoint GET /readings/latest
@app.get("/readings/latest")
def get_latest_readings(device_id: str, limit: int = 5):
    items = [
        {"reading_id": rid, **r.model_dump()}
        for rid, r in db.items()
        if r.device_id == device_id
    ]
    return {"items": items[-limit:]}

@app.get("/readings/{reading_id}")
def get_reading(reading_id: str):
    if reading_id not in db:
        raise HTTPException(status_code=404, detail="Reading not found")
    return {"reading_id": reading_id, **db[reading_id].model_dump()}