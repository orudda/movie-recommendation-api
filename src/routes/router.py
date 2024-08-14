from fastapi import APIRouter, Depends
from src.controller.filme_controller import FilmeController
from src.db.session import get_db
from sqlalchemy.orm import Session
from src.service.filme_service import FilmeService

main_router = APIRouter()

@main_router.get("/filmes")
def get_filmes(db: Session = Depends(get_db)):
    return FilmeController.get_filmes(db)

@main_router.get("/filmes/{usuario_id}/recomendacoes")
def recommend_filmes(usuario_id: int, db: Session = Depends(get_db)):
    return FilmeService.get_recommendations(usuario_id, db)