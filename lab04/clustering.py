import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.cluster import KMeans, MiniBatchKMeans, DBSCAN
from scipy.cluster.hierarchy import dendrogram, ward
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate


# Строим график elbow-метода, чтобы увидеть оптимальное k. В моём случае k = 3 / 5
def plot_elbow_method(data):
    squared_dst = list()
    # Смотрим, где сумма квадрата расстояний на графике «ломается»
    k_range = range(2, 10)
    for k in k_range:
        model = KMeans(n_clusters=k, max_iter=200, n_init=10).fit(data)
        squared_dst.append(model.inertia_)

    plt.plot(k_range, squared_dst, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum of squared distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()


# Кластеризация k-средних
def get_kmeans(data, names):
    k = 3  # k = 5
    model = KMeans(n_clusters=k, init='k-means++', max_iter=200, n_init=10).fit(data)
    labels = model.labels_
    wiki_cl = pd.DataFrame(list(zip(names, labels)), columns=['title', 'cluster'])
    print("KMeans".center(43) + "\n" +
          tabulate(wiki_cl.sort_values(by=['cluster']), showindex=False, tablefmt="psql"))


# Кластеризация k-средних по мини-пакетам
def get_minibatch(data, names):
    true_k = 5
    model = MiniBatchKMeans(n_clusters=true_k, batch_size=6, max_iter=200, n_init=10).fit(data)
    labels = model.labels_
    wiki_cl = pd.DataFrame(list(zip(names, labels)), columns=['title', 'cluster'])
    print("MiniBatchKMeans".center(44) + "\n" +
          tabulate(wiki_cl.sort_values(by=['cluster']), showindex=False, tablefmt="psql"))


# Кластеризация DBSCAN (так и не заработало)
def get_dbscan(data, names):
    model = DBSCAN(eps=0.68, min_samples=5).fit(data)
    labels = model.labels_
    wiki_cl = pd.DataFrame(list(zip(names, labels)), columns=['title', 'cluster'])
    print("DBSCAN".center(42) + "\n" +
          tabulate(wiki_cl.sort_values(by=['cluster']), showindex=False, tablefmt="psql"))

    # Пытался починить DBSCAN, для этого подбирал различные эпсилон.
    # Для этого строим график расстояний от каждой точки до её ближайшего соседа, смотрим на «резкие» изломы
    # Eps = максимальное расстояние между двумя точками
    def estimate_eps():
        # Расстояние от каждой точки до её ближайшего соседа
        neigh = NearestNeighbors(n_neighbors=2)
        nb = neigh.fit(data)

        # Возвращает 2 списка:
        # distances:    расстояние до ближайших n-соседей
        # indices:      индекс каждой из таких точек
        distances, indices = nb.kneighbors(data)

        distances = np.sort(distances, axis=0)
        distances = distances[:, 1]
        plt.ylabel("Eps")
        plt.xlabel("Data")
        plt.title("Choosing optimal epsilon")
        plt.plot(distances)
        plt.show()

    estimate_eps()


# Иерархическая кластеризация
def get_hierarchy(data, names):
    # расстояние = 1 - коэффициент Отиаи (схожесть) для каждой статьи
    dist = 1 - cosine_similarity(data)

    # Используем минимизацию Ворда
    linkage_matrix = ward(dist)
    plt.figure(figsize=(50, 50))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('sample index')
    plt.ylabel('distance')
    # Рисуем дендограмму
    dendrogram(
        linkage_matrix,
        orientation="right",
        labels=names
    )
    plt.show()
