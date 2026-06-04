from typing import Optional, List
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
import uuid

app = FastAPI()

# Model cho dữ liệu
class Reading(BaseModel):
    device_id: str
    metric: str
    value: float = Field(..., ge=-40, le=80)
    unit: str
    timestamp: str

# Database giả lập
db = {}

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "team-notify", "version": "v0.1.0"}

@app.post("/readings", status_code=status.HTTP_201_CREATED)
def create_reading(
    data: Reading, 
    x_api_key: Optional[str] = Header(None, alias="x-api-key")
):
    if not x_api_key or x_api_key != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    reading_id = str(uuid.uuid4())
    db[reading_id] = data
    return {"reading_id": reading_id, **data.model_dump()}

@app.get("/readings/latest")
def get_latest(device_id: str, limit: int = 5):
    return {"items": []}

@app.get("/readings/{reading_id}")
def get_reading(reading_id: str):
    if reading_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    return {"reading_id": reading_id, **db[reading_id].model_dump()}