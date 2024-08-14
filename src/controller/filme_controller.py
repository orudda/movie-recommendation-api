from fastapi import HTTPException
from src.service.filme_service import FilmeService
from sqlalchemy.orm import Session

class FilmeController:

    def get_filmes(db: Session):

        try:
            return FilmeService.fetch_filmes(db)
        except ValueError as e:
            raise HTTPException(status_code=204, detail=str(e))
        
    
    def get_recommendations(usuario_id: int, db: Session):
        
        try:
            FilmeService.verify_user(usuario_id, db)
            return FilmeService.get_recommendations(usuario_id, db)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
