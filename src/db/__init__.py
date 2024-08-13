import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from src.db.models import Base, Filme

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
        if db.query(Filme).count() == 0:
            filmes = [
                Filme(titulo="Inception", genero="Sci-Fi", diretor="Christopher Nolan", ano=2010),
                Filme(titulo="The Matrix", genero="Action", diretor="Wachowski Brothers", ano=1999),
                Filme(titulo="Interstellar", genero="Sci-Fi", diretor="Christopher Nolan", ano=2014),
            ]
            db.add_all(filmes)
            db.commit()
    finally:
        db.close()

init_db()
