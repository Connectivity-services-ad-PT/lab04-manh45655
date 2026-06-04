FROM python:3.11-slim

# Cài đặt curl để GitHub Actions có thể kiểm tra sức khỏe
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirement và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# THIẾT LẬP ĐƯỜNG DẪN ĐỂ PYTHON TÌM THẤY THƯ MỤC 'src'
ENV PYTHONPATH=/app

# KHỞI CHẠY APP BẰNG MÔ-ĐUN (Cực kỳ quan trọng để đúng đường dẫn)
CMD ["python", "-m", "uvicorn", "src.iot_app.main:app", "--host", "0.0.0.0", "--port", "8000"]