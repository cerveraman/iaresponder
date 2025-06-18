FROM mysql:8.0

# Copiar archivos
WORKDIR /app
COPY query.sql entrypoint.sh ./

# Hacer ejecutable el script
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
