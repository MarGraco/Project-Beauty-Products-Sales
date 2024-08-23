# Documentação do Projeto (1)

Antes de tudo, obrigado pela atenção e tentarei ser o mais sucinto. 

### 1° Etapa - Instação da Virtual Machine

- No meu caso, usei a Virtual Box da Oracle, pois é simples e funcional. Siga as instruções de instalação desse vídeo aqui: [instalacao virtualbox](https://www.youtube.com/watch?v=PaDTA4B7K4U). Agora, feito todas essas etapas, conecte a VM em uma internet.

### 2° Etapa - Instação do anaconda

- Siga as instruções desse link [instalacao anaconda](https://www.anaconda.com/download).

### 3° Etapa - Configuração de pastas e variável de ambiente

- Crie uma pasta.
- Crie um ambiente virtual com as etapas abaixo.
    - Abra o anaconda prompt no menu iniciar e digite o código. No meu caso, estou usando o python 3.11.
        
        ```bash
        conda create --name nome_do_ambiente python=3.11
        ```
        
    - Para ativar o ambiente
        
        ```bash
        conda activate nome_do_ambiente
        ```
        
    - Para desativar o ambiente
        
        ```bash
        conda deactivate
        ```
        

### 4° Etapa - Instação do Scrapy

- Com o terminal ainda aberto e com o variável de ambiente ativado, execute o código para a instalação do scrapy.
    
    ```bash
    pip install scrapy
    ```
    

### 5° Etapa - Instalação do interpretador

- Essa etapa deixarei em branco pois depende do gosto do usuário. Mas há opções como Pycharm, Visual Studio Code e por aí vai.

### 6° Etapa - Configuração do Scrapy

- Ainda com o terminal aberto ou através do terminal do seu interpretador, vamos criar um projeto usando scrapy através do código abaixo.
    
    ```bash
    scrapy startproject nome_do_projeto
    ```
    
- Entre na pasta do projeto.
    
    ```bash
    cd nome_do_project
    ```
    
- Execute o código para criar um exemplo de scrapy
    
    ```bash
    scrapy genspider example example.com
    ```
    

### 7° Etapa - Rodar o scrapy e gerando um arquivo

- Nesse caso, temos duas opções para rodar.
    - 1° Opção: criar arquivo com os dados em csv ou qualquer outra extensão da sua preferência.
        
        ```bash
        scrapy crawl -nome_do_projeto -O nome_de_sua_preferencia.csv
        ```
        

### 8° Etapa - Criação de um dockerfile (instale o docker desktop)

```
0          echo FROM python:3.11.9-slim > Dockerfile
1                    echo WORKDIR /app >> Dockerfile
2  echo COPY belezanaweb/spiders/requirements.txt...
3  echo RUN pip install --no-cache-dir -r require...
4                        echo COPY . . >> Dockerfile
5  echo CMD ["scrapy", "crawl", "scrapy4_bnw"] >>...
```

### 9. **Construir a Imagem Docker**

Navegue até o diretório onde o `Dockerfile` está localizado e execute o seguinte comando para construir a imagem Docker:

```bash
docker build -t your_username/your_repository_name:your_tag .

```

### 10. **Fazer o Push da Imagem para o Docker Hub**

Para enviar a imagem para o Docker Hub, use o comando `docker push`:

```bash
docker push your_username/your_repository_name:your_tag

```

### 11° Etapa - Criar um Novo Contêiner com Acesso ao Bash

```bash
docker run -it --name novo-nome-do-container nome-da-imagem /bin/bash

```

### 12° Etapa - Conexão Banco de Dados com docker no EC2

```bash
docker run -d --name container \
  -e DATABASE_HOST='xxxxxxxxxxxxxxxxxxxxx' \
  -e DATABASE_PORT='5432' \
  -e DATABASE_USER='xxxxxxxxxxxxx' \
  -e DATABASE_PASSWORD='xxxxxxxxxxxxxxx' \
  -e DATABASE_NAME='xxxxxxxxxxxxxxxxx' \
  your-login/projeto-belezanaweb:latest
```

### 13 - Comando crontab para configurar hora de rodar o projeto

```bash
(crontab -l ; echo "0 6 * * * docker run --rm --name container \
  -e DATABASE_HOST='xxxxxxxxxxxxxxxxxxxxx' \
  -e DATABASE_PORT='5432' \
  -e DATABASE_USER='xxxxxxxxxxxxx' \
  -e DATABASE_PASSWORD='xxxxxxxxxxxxxxx' \
  -e DATABASE_NAME='xxxxxxxxxxxxxxxxx' \
    your-login/projeto-belezanaweb:latest") | crontab -
```

### **14 - Liste os containers:**

- Para ver os containers que estão parados, use o comando:
    
    ```bash
    docker ps -a
    ```
    

### **15 - Inicie o container:**

- Para iniciar um container parado, use o seguinte comando:
    
    ```bash
    docker start <CONTAINER ID ou NAMES>
    
    ```
    

### **16 - Verifique se o container está ativo:**

- Para confirmar que o container está rodando, use:
    
    ```bash
    docker ps
    ```
    

### 17 - execução:

```bash
docker exec -it <CONTAINER ID ou NAMES> /bin/bash
```

### **18 - Pare o container (se ele estiver rodando):**

- Antes de eliminar o container, ele precisa estar parado. Se ele ainda estiver em execução, pare-o com:
    
    ```bash
    docker stop <CONTAINER ID ou NAMES>
    ```
    

### **19 - Elimine o container:**

- Para eliminar o container, use o comando:
    
    ```bash
    docker rm <CONTAINER ID ou NAMES>
    ```