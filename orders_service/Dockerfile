# Usar a imagem oficial do Python como base
FROM python:3.12-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho
COPY . .

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Definir a variável de ambiente
ENV PYTHONUNBUFFERED=1

# Expor a porta em que o Django vai rodar
EXPOSE 8000

# Comando para iniciar o servidor Django automaticamente
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
