# syntax=docker/dockerfile:1.4
FROM python:3.11-slim

# Configuraciones de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Actualizar certificados raíz
RUN update-ca-certificates

# Instalar dependencias de Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Actualizar bibliotecas críticas
RUN pip install --upgrade --no-cache-dir requests urllib3

# Copiar el código fuente
COPY . /app/

# Comando para ejecutar el scraper
CMD ["python", "webscraper.py"]
