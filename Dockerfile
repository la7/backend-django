# Imagen base Python 3.11 (slim para reducir tamaño)
FROM python:3.11-slim

# Directorio de trabajo en el contenedor
WORKDIR /app

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copiar dependencias
COPY requirements.txt .

# Instalar dependencias del sistema necesarias para bcrypt
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y gcc \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Copiar código de la aplicación
COPY . .

# Puerto expuesto (Django/Gunicorn)
EXPOSE 8000

# Comando de arranque
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
