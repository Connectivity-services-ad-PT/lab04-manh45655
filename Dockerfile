FROM python:3.11-slim

# Cài đặt curl để GitHub Actions có thể kiểm tra sức khỏe
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào /app
COPY . .

# THIẾT LẬP ĐƯỜNG DẪN ĐỂ PYTHON TÌM THẤY 'src'
ENV PYTHONPATH=/app

# Khởi chạy FastAPI thông qua module path (sử dụng dấu chấm)
CMD ["python", "-m", "uvicorn", "src.iot_app.main:app", "--host", "0.0.0.0", "--port", "8000"]