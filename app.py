from fastapi import FastAPI
from dotenv import load_dotenv
import os
from src.routes.router import main_router

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI()

# Incluindo as rotas principais
app.include_router(main_router)

# Exemplo de uso da variável de ambiente
database_url = os.getenv("DATABASE_URL")
