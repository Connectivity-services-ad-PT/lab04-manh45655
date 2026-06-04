FROM python:3.11-slim

# Cài đặt curl để kiểm tra sức khỏe container
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Thiết lập đường dẫn để Python nhận diện thư mục 'src' là gốc
ENV PYTHONPATH=/app

# Khởi chạy bằng module path thay vì đường dẫn file vật lý
# Dấu chấm (.) giúp tránh lỗi gạch chéo của Windows
CMD ["python", "-m", "uvicorn", "src.iot_app.main:app", "--host", "0.0.0.0", "--port", "8000"]