from typing import Optional
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
import uuid

app = FastAPI()

# Database giả lập
db = {}

# Yêu cầu 1: Schema Pydantic với Validation
class Reading(BaseModel):
    device_id: str
    metric: str
    value: float = Field(..., ge=-40, le=80)
    unit: str
    timestamp: str

# Yêu cầu 2: Health Check (Để vượt qua lỗi Timed out của GitHub Actions)
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "iot-app"}

# Yêu cầu 3: POST endpoint với bảo mật API Key qua Header
@app.post("/readings", status_code=status.HTTP_201_CREATED)
def create_reading(
    data: Reading, 
    x_api_key: str = Header(...) # Bắt buộc phải có header x-api-key
):
    if x_api_key != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid API Key")
    
    reading_id = str(uuid.uuid4())
    db[reading_id] = data
    return {"reading_id": reading_id, **data.model_dump()}

# Yêu cầu 4: GET endpoint theo ID
@app.get("/readings/{reading_id}")
def get_reading(reading_id: str):
    if reading_id not in db:
        raise HTTPException(status_code=404, detail="Reading not found")
    return {"reading_id": reading_id, **db[reading_id].model_dump()}