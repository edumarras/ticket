FROM python:3.11-slim

# Atualizar e instalar dependências necessárias
RUN apt-get update && apt-get install -y --no-install-recommends && apt-get clean

WORKDIR /app

# Copiar os arquivos requirements.txt e main.py do host para o contêiner
COPY requirements.txt /app/requirements.txt
COPY main.py /app/main.py

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta da aplicação
EXPOSE 8000

# Comando para iniciar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
