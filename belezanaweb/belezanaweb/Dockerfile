FROM python:3.11.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos para o contêiner
COPY belezanaweb/spiders/requirements.txt .

# Instala as dependências listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o contêiner
COPY . .

# Comando para iniciar o Scrapy com o spider específico
CMD ["scrapy", "crawl", "scrapy4_bnw"]