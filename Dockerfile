FROM python:3.11-slim

# Cài đặt curl để phục vụ Healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirement và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Thiết lập PYTHONPATH để Python nhận diện thư mục src/ là gốc
ENV PYTHONPATH=/app

# Khởi chạy bằng module path chính xác
CMD ["python", "-m", "uvicorn", "src.iot_app.main:app", "--host", "0.0.0.0", "--port", "8000"]