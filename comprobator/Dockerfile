FROM python:3.10-slim

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el script principal
COPY gmail_auto_reply.py .

# Usar ENTRYPOINT para permitir pasar argumentos
ENTRYPOINT ["python", "gmail_auto_reply.py"]

