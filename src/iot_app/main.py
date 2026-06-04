from fastapi import FastAPI, Header, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Optional
import uuid
import os

app = FastAPI()

db = {}

AUTH_TOKEN = os.getenv("AUTH_TOKEN", "secret-token")

# Fix: thêm type field vào validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "type": "validation_error",
            "detail": exc.errors()
        }
    )

# Fix: thêm type field vào auth errors  
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": "http_error",
            "detail": exc.detail
        }
    )

class Reading(BaseModel):
    device_id: str
    metric: str
    value: float = Field(..., ge=-40, le=80)
    unit: str
    timestamp: str

@app.api_route("/health", methods=["GET", "HEAD"])
def health_check():
    return {"status": "ok", "service": "iot-app", "version": os.getenv("SERVICE_VERSION", "0.4.0")}

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

    if data.value >= 80:
        response.headers["X-Warning"] = "High temperature detected"

    return {"reading_id": reading_id, **data.model_dump()}

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