from fastapi import HTTPException
from fastapi.responses import JSONResponse
from src.service.filme_service import FilmeService, ServiceError
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
        except ServiceError as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=e.status_code
            )
        
        
