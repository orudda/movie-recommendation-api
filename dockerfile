# Usar a imagem base do Python
FROM python:3.9

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código da aplicação para o diretório de trabalho
COPY . .

# Treinar o modelo antes de iniciar a API
RUN python train_model.py

# Copiar o script de testes para o container
# COPY run_tests.sh .

# Conceder permissão de execução para o script de testes
# RUN chmod +x run_tests.sh

# Definir a variável de ambiente PORT
ENV PORT=8000

# Expor a porta em que a aplicação Flask vai rodar
EXPOSE 8000

# Definir o comando padrão para executar a aplicação
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
