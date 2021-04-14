import pickle
from sklearn.feature_extraction.text import TfidfVectorizer


# Конвертируем содержимое в матрицу TF-IDF фичей
def extract_tfid_features_and_save(
    article_names: list,
    article_contents: list,
    article_names_plk: str,
    article_contents_plk: str
):
    # Извлечь фичи из текстов на английском языке с помощью TF-IDF(признаки).
    vectorizer = TfidfVectorizer(stop_words={'english'})
    vectorized_data = vectorizer.fit_transform(article_contents)
    # print(vectorizer.get_feature_names())

    # С помощью pickle сохраняем вектор фичей и названия статей
    pickle.dump(article_names, open(article_names_plk, "wb"))
    pickle.dump(vectorized_data, open(article_contents_plk, "wb"))

