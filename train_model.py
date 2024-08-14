import os
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import json

def train_and_save_model():
    # Carregar dados de mock_data.json
    with open('mock_data.json', 'r') as f:
        data = json.load(f)

    # Separar avaliações e filmes
    avaliacoes = data['avaliacoes']
    filmes = data['filmes']
    
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
    
    with open('scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    # Treinar o modelo KMeans com base nos filmes (não usuários)
    n_clusters = 5  # Ajustar número de clusters
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(user_movie_matrix_scaled)  # Transpor para clusterizar filmes
    
    # Salvar o modelo treinado
    with open('kmeans_model.pkl', 'wb') as f:
        pickle.dump(kmeans, f)
    
    # Salvar o DataFrame e as informações dos filmes para uso posterior
    user_movie_matrix.to_csv('user_movie_matrix.csv')
    
    # Treinar o modelo KMeans com base nos filmes (não usuários)
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
    plt.savefig('kmeans_filmes_clusters.png')  # Salvar a visualização
    plt.show()

if __name__ == "__main__":
    train_and_save_model()
