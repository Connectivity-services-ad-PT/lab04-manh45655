from typing import Optional, List
from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
import uuid

app = FastAPI()

# Model kiểm tra dữ liệu đầu vào
class Reading(BaseModel):
    device_id: str
    metric: str
    value: float = Field(..., ge=-40, le=80) # Ràng buộc dữ liệu từ -40 đến 80
    unit: str
    timestamp: str

# Database giả lập trong bộ nhớ
db = {}

# Endpoint bắt buộc cho Health Check (Để GitHub Actions không bị timeout)
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "team-notify", "version": "v0.1.0"}

# Endpoint tạo reading
@app.post("/readings", status_code=status.HTTP_201_CREATED)
def create_reading(
    data: Reading, 
    x_api_key: Optional[str] = Header(None, alias="x-api-key")
):
    # Kiểm tra API Key (Yêu cầu bảo mật cơ bản)
    if not x_api_key or x_api_key != "secret-token":
        raise HTTPException(status_code=401, detail="Invalid or missing token")
    
    reading_id = str(uuid.uuid4())
    db[reading_id] = data
    return {"reading_id": reading_id, **data.model_dump()}

# Endpoint lấy các reading gần nhất
@app.get("/readings/latest")
def get_latest(device_id: str, limit: int = 5):
    # Trả về danh sách rỗng hoặc filter theo logic của bạn
    return {"items": []}

# Endpoint lấy reading theo ID
@app.get("/readings/{reading_id}")
def get_reading(reading_id: str):
    if reading_id not in db:
        raise HTTPException(status_code=404, detail="Not found")
    return {"reading_id": reading_id, **db[reading_id].model_dump()}