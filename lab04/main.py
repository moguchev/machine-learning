import pickle
import wikipedia
from clustering import plot_elbow_method, get_kmeans, get_minibatch, get_dbscan, get_hierarchy
from extraction import extract_tfid_features_and_save


# Темы статей (1 Вариант)
THEMES = ("Ancient history", "English literature", "Diseases")
ARTICLES_NUM = 20
CONTENT_PLK = "data.plk"
TITLES_PLK = "titles.plk"


# Скачиваем статьи по каждой теме
def download_articles(themes: list, articles_per_theme: int):
    articles = list()
    article_names = list()

    for theme in themes:
        for article in wikipedia.search(theme, results=articles_per_theme):
            print(f"Downloaded article: {article}")
            try:
                articles.append(wikipedia.page(article).content)
            except wikipedia.exceptions.PageError:
                print(f"SKIP Downloaded article: {article} - PageError")
                continue
            except wikipedia.exceptions.DisambiguationError:
                print(f"SKIP Downloaded article: {article} - DisambiguationError")
                continue
            article_names.append(article)

    # Возвращаем список названий статей и список статей
    return article_names, articles


if __name__ == '__main__':
    # скачиваем статьи
    # titles, contents = download_articles(THEMES, ARTICLES_NUM)
    # выделение фичей и сохранение
    # extract_tfid_features_and_save(titles, contents, TITLES_PLK, CONTENT_PLK)
    # Открываем сохраненные данные
    data = pickle.load(open(CONTENT_PLK, "rb"))
    names = pickle.load(open(TITLES_PLK, "rb"))
    # Строим elbow-метод
    plot_elbow_method(data)

    # Разные варианты кластеризации
    get_kmeans(data, names)
    get_minibatch(data, names)
    get_dbscan(data, names)
    get_hierarchy(data, names)
