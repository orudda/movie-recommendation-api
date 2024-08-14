import os
from dotenv import load_dotenv
load_dotenv() 
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import json

def visualizacao_PCA(user_movie_matrix_scaled, user_movie_matrix):
    KMEANS_IMAGE= os.getenv("KMEANS_IMAGE")

    # Treinar o modelo KMeans com base nos filmes (não usuários) para visualização
    n_clusters = 5  # Ajustar número de clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(user_movie_matrix_scaled.T)  # Transpor para clusterizar filmes
    
    # Visualização do KMeans para os filmes
    filmes_matrix = user_movie_matrix.T  # Transpor para ter filmes como linhas
    
    # Normalizar os dados dos filmes
    filmes_matrix_scaled = StandardScaler().fit_transform(filmes_matrix)
    
    pca = PCA(n_components=2)  # Reduzir para 2D
    reduced_data = pca.fit_transform(filmes_matrix_scaled)
    cluster_labels = kmeans.predict(filmes_matrix_scaled)  # Predizer clusters para filmes
    
    plt.figure(figsize=(12, 8))
    
    # Plotar filmes com cores diferentes para cada cluster
    scatter = plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=cluster_labels, cmap='viridis', marker='o')
    
    # Adicionar uma legenda
    legend1 = plt.legend(*scatter.legend_elements(), title="Clusters")
    plt.gca().add_artist(legend1)
    
    plt.title('Visualização dos Clusters KMeans para Filmes')
    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.colorbar(label='Cluster')
    plt.savefig(KMEANS_IMAGE)  # Salvar a visualização
    plt.show()

def train_and_save_model():

    KMEANS_MODEL_PATH = os.getenv("KMEANS_PATH")
    SCALER_PATH = os.getenv("SCALER_PATH")
    USER_MOVIE_MATRIX = os.getenv("USER_MOVIE_MATRIX_PATH")
    TRAIN_DATABASE = os.getenv("TRAIN_DATABASE")

    # Carregar dados de mock_data.json
    with open(TRAIN_DATABASE, 'r') as f:
        data = json.load(f)

    # Separar avaliações e filmes
    avaliacoes = data['avaliacoes']
    
    # Criar DataFrame de avaliações
    df = pd.DataFrame(avaliacoes)
    
    # Pivotar o DataFrame
    user_movie_matrix = df.pivot_table(index='usuario_id', columns='filme_id', values='avaliacao')
    
    # Preencher NaNs com 0
    user_movie_matrix = user_movie_matrix.fillna(0)
    
    # Garantir que todas as colunas são numéricas
    user_movie_matrix = user_movie_matrix.astype(float)
    
    # Normalizar os dados dos usuários
    scaler = StandardScaler()
    user_movie_matrix_scaled = scaler.fit_transform(user_movie_matrix)
    
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)
    
    # Treinar o modelo KMeans com base nos usuários
    n_clusters = 5  # Ajustar número de clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(user_movie_matrix_scaled)  # Transpor para clusterizar filmes
    
    # Salvar o modelo treinado
    with open(KMEANS_MODEL_PATH, 'wb') as f:
        pickle.dump(kmeans, f)
    
    # Salvar o DataFrame e as informações dos filmes para uso posterior
    user_movie_matrix.to_csv(USER_MOVIE_MATRIX)

    visualizacao_PCA(user_movie_matrix_scaled, user_movie_matrix)

if __name__ == "__main__":
    train_and_save_model()
