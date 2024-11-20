# syntax=docker/dockerfile:1.4

FROM python:3.11-slim

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Actualizar sistema y preparar dependencias
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Actualizar 'requests' y 'urllib3' a sus versiones más recientes
RUN pip install --upgrade requests urllib3

# Añadir código fuente
COPY . /app/

CMD ["python", "webscraper.py"]
