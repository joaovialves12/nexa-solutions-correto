#!/bin/sh
set -e

echo "Aguardando o banco de dados em ${POSTGRES_HOST}:${POSTGRES_PORT}..."

while ! python -c "
import os, socket, sys
host = os.environ.get('POSTGRES_HOST', 'db')
port = int(os.environ.get('POSTGRES_PORT', '5432'))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(1)
try:
    s.connect((host, port))
except OSError:
    sys.exit(1)
else:
    sys.exit(0)
finally:
    s.close()
"; do
  sleep 1
done

echo "Banco de dados disponível. Aplicando migrations..."
python manage.py migrate --noinput

echo "Iniciando servidor Django..."
exec python manage.py runserver 0.0.0.0:8000
