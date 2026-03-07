# Usamos la versión de Python recomendada
FROM python:3.11-slim

# Evitar archivos temporales y asegurar salida de logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 1. Instalamos FFmpeg (REQUISITO para Whisper) y git
RUN apt-get update && apt-get install -y \
    ffmpeg \
    git \
    gcc \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalamos las librerías de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#---RUN pip install --upgrade pip && \
#---    pip install --no-cache-dir -r requirements.txt

# 3. Pre-descargamos el modelo Whisper "base" 
# Esto evita que el contenedor lo baje en cada reinicio
RUN python -c "import whisper; whisper.load_model('base')"

# 4. Copiamos el resto del código
COPY . .

# 5. Ejecutamos el worker (no usamos uvicorn porque no es una API)
CMD ["python", "app.py"]
