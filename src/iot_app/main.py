from fastapi import FastAPI, Header, HTTPException, status, Response, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field
from typing import Optional
import uuid
import os
from datetime import datetime

app = FastAPI()

db = {}

AUTH_TOKEN = os.getenv("AUTH_TOKEN", "secret-token")

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "type": "validation_error",
            "title": "Validation Error",
            "status": 422,
            "detail": exc.errors()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": "http_error",
            "title": "HTTP Error",
            "status": exc.status_code,
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
    authorization: Optional[str] = Header(default=None)
):
    # Kiểm tra Authorization: Bearer <token>
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing API Key")
    
    token = authorization.replace("Bearer ", "")
    if token != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # Format reading_id: R-YYYYMMDD-XXXX
    date_str = datetime.now().strftime("%Y%m%d")
    short_id = str(uuid.uuid4().int)[:4]
    reading_id = f"R-{date_str}-{short_id}"

    db[reading_id] = data

    if data.value >= 80:
        response.headers["X-Warning"] = "High temperature detected"

    return {
        "reading_id": reading_id,
        "accepted": True,
        **data.model_dump()
    }

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