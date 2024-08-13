from sqlalchemy.orm import Session
from src.db.models import Filme

def fetch_filmes(db: Session):
    return db.query(Filme).all()
