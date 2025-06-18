#!/bin/sh
set -e

while true; do
    echo "📥 Ejecutando query.sql..."

    # Ejecutar el query y guardar el resultado como CSV
    mysql -h "$MYSQL_HOST" -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" \
        --batch --raw --silent < /app/query.sql > /app/Downloads/archivo.csv

    echo "✅ Consulta ejecutada y guardada en Downloads/archivo.csv."

    sleep 300  # 300 segundos = 5 minutos
done
