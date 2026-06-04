FROM python:3.11-slim

# Cài đặt curl để phục vụ Healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Tạo user non-root
RUN useradd -m notifyuser
WORKDIR /app

# Copy requirement trước để cache layer
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ .
RUN chown -R notifyuser /app
USER notifyuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "iot_app.main:app", "--host", "0.0.0.0", "--port", "8000"]