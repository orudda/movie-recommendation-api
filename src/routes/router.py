from fastapi import APIRouter, Depends
from src.controller.filme_controller import FilmeController
from src.db.session import get_db
from sqlalchemy.orm import Session



main_router = APIRouter()

@main_router.get("/filmes")
def get_filmes(db: Session = Depends(get_db)):
    return FilmeController.get_filmes(db)

@main_router.get("/filmes/{usuario_id}/recomendacoes")
def get_recomendacoes(usuario_id: int):
    return {"usuario_id": usuario_id, "recomendacoes": ["Filme A", "Filme B"]}
1