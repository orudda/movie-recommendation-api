import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from src.db.models import Base, Filme, Usuario, Avaliacao

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Obtém a URL do banco de dados do .env
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():        
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Inserir filmes iniciais
        if db.query(Filme).count() == 0 and db.query(Usuario).count() == 0 and db.query(Avaliacao).count() == 0:
            with open('mock_data.json', 'r') as f:
                data = json.load(f)

            for usuario_data in data['usuarios']:
                usuario = Usuario(**usuario_data)
                db.add(usuario)
            
            for filme_data in data['filmes']:
                filme = Filme(**filme_data)
                db.add(filme)
            
            for avaliacao_data in data['avaliacoes']:
                avaliacao = Avaliacao(**avaliacao_data)
                db.add(avaliacao)
    
            db.commit()
    finally:
        db.close()

init_db()
