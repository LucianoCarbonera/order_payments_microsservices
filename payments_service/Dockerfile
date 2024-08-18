# Usar a imagem oficial do Python como base
FROM python:3.12-slim

# Instalar dependências necessárias
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho
COPY . .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Definir a variável de ambiente
ENV PYTHONUNBUFFERED=1

# Expor a porta em que o Django vai rodar
EXPOSE 8001

# Comando para iniciar o serviço Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
