FROM python:3.11-slim

# Cài đặt curl để GitHub Actions có thể kiểm tra sức khỏe container
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Cài đặt các thư viện cần thiết
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn
COPY . .

# Phân quyền
RUN useradd -m notifyuser && chown -R notifyuser /app
USER notifyuser

# LỆNH QUAN TRỌNG: Phải trỏ đúng vào đường dẫn module `src.iot_app.main`
CMD ["python", "-m", "uvicorn", "src.iot_app.main:app", "--host", "0.0.0.0", "--port", "8000"]