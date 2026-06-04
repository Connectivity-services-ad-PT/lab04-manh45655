# Sử dụng base image nhẹ
FROM python:3.11-slim

# Cài đặt curl để kiểm tra service health (tránh lỗi Timed out)
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy các file cần thiết và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Thiết lập đường dẫn để Python nhận diện thư mục 'src' là gốc của các package
ENV PYTHONPATH=/app

# Khởi chạy FastAPI
# Lệnh này gọi file main.py thông qua gói src.iot_app
CMD ["python", "-m", "uvicorn", "src.iot_app.main:app", "--host", "0.0.0.0", "--port", "8000"]