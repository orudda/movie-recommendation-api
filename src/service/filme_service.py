import os
import pickle
import pandas as pd
from sqlalchemy.orm import Session
from src.db.models import Avaliacao, Filme, Usuario

KMEANS_MODEL_PATH = os.getenv("KMEANS_PATH")
SCALER_PATH = os.getenv("SCALER_PATH")
USER_MOVIE_MATRIX = os.getenv("USER_MOVIE_MATRIX_PATH")

class ServiceError(ValueError):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code

class FilmeService:
    def verify_user(usuario_id: int, db: Session):
        usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if usuario is None:
            raise ServiceError(f"Usuário com ID {usuario_id} não encontrado.", 404)
        return usuario

    def fetch_filmes(db: Session):
        filmes = db.query(Filme).all()
        if not filmes:
            raise ServiceError("Nenhum filme encontrado.", 204)
        return filmes

    def get_recommendations(usuario_id: int, db: Session):

        # Carregar o modelo treinado, o scaler, e a matriz de usuário-filme para formato
        with open(KMEANS_MODEL_PATH, 'rb') as f:
            kmeans = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        
        user_movie_matrix = pd.read_csv(USER_MOVIE_MATRIX, index_col=0)
        
        # Obter as avaliações do usuário
        avaliacoes = db.query(Avaliacao).filter(Avaliacao.usuario_id == usuario_id).all()
        avaliacoes_df = pd.DataFrame([{
            'usuario_id': a.usuario_id,
            'filme_id': a.filme_id,
            'avaliacao': a.avaliacao
        } for a in avaliacoes])
        
        if avaliacoes_df.empty:
            raise ServiceError(f"Nenhuma avaliação encontrada para o usuário {usuario_id}.", 204)

        # Criar um DataFrame para a avaliação do usuário
        user_evaluation = pd.DataFrame({
            'usuario_id': [usuario_id] * len(avaliacoes_df),
            'filme_id': avaliacoes_df['filme_id'],
            'avaliacao': avaliacoes_df['avaliacao']
        }).pivot_table(index='usuario_id', columns='filme_id', values='avaliacao', fill_value=0)

        for i in user_movie_matrix.columns.astype(int):
            if i not in user_evaluation.columns:
                user_evaluation[i] = 0
        
        # Usar o scaler treinado para normalizar os dados do usuário
        user_evaluation_scaled = scaler.transform(user_evaluation)

        # Predizer o cluster do usuário
        cluster = kmeans.predict(user_evaluation_scaled)[0]

        # Obter filmes recomendados no cluster
        cluster_centers = kmeans.cluster_centers_
        cluster_center = cluster_centers[cluster]
        cluster_center_df = pd.DataFrame(cluster_center, index=user_movie_matrix.columns).T

        #carregar filmes
        filmes = FilmeService.fetch_filmes(db)
        filmes_data = [{
            'id': filme.id,
            'titulo': filme.titulo,
            'genero': filme.genero,
            'diretor': filme.diretor,
            'atores': filme.atores
        } for filme in filmes]
        filmes_df = pd.DataFrame(filmes_data)

        # Ordenar filmes por relevância
        recommended_movies = cluster_center_df.T.sort_values(by=0, ascending=False).head(5)
        recommended_movies_ids = recommended_movies.index
        filmes_df['id'] = filmes_df['id'].astype(str)
        
        # Filtrar os filmes recomendados
        recommended_movies_df = filmes_df[filmes_df['id'].isin(recommended_movies_ids)]
        
        return recommended_movies_df.to_dict(orient='records')