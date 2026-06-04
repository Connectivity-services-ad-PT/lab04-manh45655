FROM python:3.11-slim

# Cài curl để phục vụ Healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirement và cài đặt trước để tận dụng Docker Cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Set PYTHONPATH để đảm bảo Python nhận diện được thư mục src
ENV PYTHONPATH=/app

# Lệnh chạy module chính xác
CMD ["python", "-m", "uvicorn", "src.iot_app.main:app", "--host", "0.0.0.0", "--port", "8000"]