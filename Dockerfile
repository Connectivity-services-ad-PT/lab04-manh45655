FROM python:3.11-slim

# Cài đặt curl để hỗ trợ kiểm tra sức khỏe container
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy và cài đặt thư viện
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ source code
COPY . .

# ĐẶT BIẾN MÔI TRƯỜNG ĐỂ PYTHON NHẬN DIỆN THƯ MỤC 'src' LÀ GỐC
ENV PYTHONPATH=/app

# LỆNH KHỞI CHẠY (Sửa đúng đường dẫn đến file main.py của bạn)
CMD ["python", "-m", "uvicorn", "src.iot_app.main:app", "--host", "0.0.0.0", "--port", "8000"]