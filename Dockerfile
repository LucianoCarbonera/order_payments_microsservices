# Use uma imagem base do Python
FROM python:3.10-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
COPY orders_service/requirements.txt /app/

# Instale as dependências necessárias
RUN pip install --no-cache-dir -r /app/requirements.txt

# Instale o Locust
RUN pip install locust

# Copie o arquivo locustfile.py para o diretório de trabalho
COPY locustfile.py /app/

# Exponha a porta que o Locust irá usar
EXPOSE 8089

# Comando para rodar o Locust
CMD ["locust", "-f", "locustfile.py"]
