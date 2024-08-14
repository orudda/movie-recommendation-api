from src.service.filme_service import FilmeService
from sqlalchemy.orm import Session

class FilmeController:

    def get_filmes(db: Session):
        return FilmeService.fetch_filmes(db)
    
    def get_recommendations(usuario_id: int, db: Session):
        return FilmeService.get_recommendations(usuario_id, db)
