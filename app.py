from fastapi import FastAPI
from dotenv import load_dotenv
from src.routes.router import main_router

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

app = FastAPI()

# Incluindo as rotas principais
app.include_router(main_router)
