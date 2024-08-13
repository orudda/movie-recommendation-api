from fastapi import APIRouter

main_router = APIRouter()

@main_router.get("/filmes")
def get_filmes():
    return {"filmes": ["Filme 1", "Filme 2", "Filme 3"]}

@main_router.get("/filmes/{usuario_id}/recomendacoes")
def get_recomendacoes(usuario_id: int):
    return {"usuario_id": usuario_id, "recomendacoes": ["Filme A", "Filme B"]}
1