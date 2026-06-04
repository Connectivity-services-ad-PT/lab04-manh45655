FROM python:3.11-slim

# Cài đặt curl để kiểm tra healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirement và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào /app
COPY . .

# Phân quyền cho user non-root
RUN useradd -m notifyuser && chown -R notifyuser /app
USER notifyuser

# Quan trọng: Đường dẫn này phải khớp với cấu trúc thư mục của bạn
# Đảm bảo app được khởi chạy từ thư mục gốc /app
CMD ["python", "-m", "uvicorn", "src.iot_app.main:app", "--host", "0.0.0.0", "--port", "8000"]