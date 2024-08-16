FROM python:3.12-slim

# Definir o diretório de trabalho no contêiner
WORKDIR /app

# Copiar os arquivos do projeto para o diretório de trabalho
COPY . .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Definir a variável de ambiente
ENV PYTHONUNBUFFERED=1

# Porta em que o Django vai rodar
EXPOSE 8000

# Comando para rodar a aplicação Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
