from src.service.filme_service import fetch_filmes
from sqlalchemy.orm import Session

class FilmeController:

    def get_filmes(db: Session):
        return fetch_filmes(db)
