FROM python:3.11-slim

# Cài đặt curl để phục vụ Healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Tạo user non-root
RUN useradd -m notifyuser
WORKDIR /app

# Copy requirement
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code
COPY . .

# Phân quyền
RUN chown -R notifyuser /app
USER notifyuser

# LỆNH CMD QUAN TRỌNG: 
# Dùng "python -m uvicorn" giúp nhận diện đúng cấu trúc thư mục src/
CMD ["python", "-m", "uvicorn", "src.iot_app.main:app", "--host", "0.0.0.0", "--port", "8000"]