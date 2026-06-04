from typing import Optional
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
import uuid
import os  # ← thêm dòng này

app = FastAPI()

db = {}

AUTH_TOKEN = os.getenv("AUTH_TOKEN", "secret-token")  # ← thêm dòng này

class Reading(BaseModel):
    device_id: str
    metric: str
    value: float = Field(..., ge=-40, le=80)
    unit: str
    timestamp: str

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "iot-app"}

@app.post("/readings", status_code=status.HTTP_201_CREATED)
def create_reading(
    data: Reading,
    x_api_key: str = Header(...)
):
    if x_api_key != AUTH_TOKEN:  # ← sửa dòng này
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    reading_id = str(uuid.uuid4())
    db[reading_id] = data
    return {"reading_id": reading_id, **data.model_dump()}

@app.get("/readings/{reading_id}")
def get_reading(reading_id: str):
    if reading_id not in db:
        raise HTTPException(status_code=404, detail="Reading not found")
    return {"reading_id": reading_id, **db[reading_id].model_dump()}