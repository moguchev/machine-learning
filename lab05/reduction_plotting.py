import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from random import random as r
from loader import get_features_and_labels
from sklearn.cluster import KMeans


def plot_lab_3():
    # Имена покемонов
    names = ["Squirtle", "Wartortle", "Blastoise", "Pidgey", "Pidgeotto", "Pidgeot"]
    # Извлекаем фичи и лейблы соответствующей лабы
    features, labels = get_features_and_labels(lab_number=3)
    # Применяем фит-трансформ
    scaled_features = StandardScaler().fit_transform(features)
    x_tsne = TSNE(n_components=2).fit_transform(scaled_features)
    x_pca = PCA().fit_transform(scaled_features)

    # Визуализируем результат
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    for index, label in enumerate(names):
        # Выбираем из массива лейблов только те, которые относятся к нужному нам индексу (0-5)
        # Соответственно, поочерёдно получаем все точки для каждого из индексов
        ax1.scatter(x=x_tsne[labels == index, 0],
                    y=x_tsne[labels == index, 1], color=(r(), r(), r()), label=label)
        ax1.title.set_text("TSNE")
        ax1.legend(loc="best")

        ax2.scatter(x=x_pca[labels == index, 0],
                    y=x_pca[labels == index, 1], color=(r(), r(), r()), label=label)
        ax2.title.set_text("PCA")
        ax2.legend(loc="best")

    plt.legend()
    plt.show()
    plt.savefig("./src/results/lab_3.png")


def plot_lab_4():
    # Темы для статей
    theme_list = ("Ancient history", "English literature", "Diseases")
    # Извлекаем фичи и лейблы соответствующей лабы
    features, labels = get_features_and_labels(lab_number=4)

    # Кластеризуем наши статьи, чтобы получить список кластеризированных лейблов
    model = KMeans(n_clusters=3, init='k-means++', max_iter=200, n_init=10).fit(features)

    # Применяем фит-трансформ
    x_tsne = TSNE(n_components=2).fit_transform(features)
    x_pca = PCA().fit_transform(features.toarray())

    # Визуализируем результат
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    for index, label in enumerate(theme_list):
        # В качестве лейблов используем полученный выше результат кластеризации
        # (таким образом, сами точки на графике кластеризованы только цветом – лейблами)

        # Выбираем из массива лейблов только те, которые относятся к нужному нам индексу (0-2)
        # Соответственно, поочерёдно получаем все точки для каждого из индексов
        ax1.scatter(x=x_tsne[model.labels_ == index, 0],
                    y=x_tsne[model.labels_ == index, 1], color=(r(), r(), r()), label=label)
        ax1.title.set_text("TSNE")
        ax1.legend(loc="best")

        ax2.scatter(x=x_pca[model.labels_ == index, 0],
                    y=x_pca[model.labels_ == index, 1], color=(r(), r(), r()), label=label)
        ax2.title.set_text("PCA")
        ax2.legend(loc="best")

    plt.legend()
    plt.show()
    plt.savefig("./src/results/lab_4.png")
