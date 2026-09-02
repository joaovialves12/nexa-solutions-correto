FROM python:3.12-slim

WORKDIR /app

# Copia os requisitos e instala as dependências do Django/Postgres
COPY backend/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código da aplicação
COPY backend/ /app/