# 1. Considera usar una versión más reciente (si tu app lo soporta)
FROM python:3.11-slim

# 2. Variables de entorno recomendadas para Python en Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Crear un usuario no-root por seguridad
RUN adduser --disabled-password --gecos "" appuser

WORKDIR /app

COPY requirements.txt .

# 4. Instalar dependencias sin guardar el caché de pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 5. Cambiar la propiedad de los archivos y cambiar al usuario seguro
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 80

CMD ["python", "app.py"]