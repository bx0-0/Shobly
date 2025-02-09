from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def recommend_products_tfidf(products, user_input, n_recommendations=5):

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(products["description"])

    user_vector = vectorizer.transform([user_input])

    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()

    products["similarity"] = similarities

    recommendations = products.sort_values(by="similarity", ascending=False)

    if recommendations.empty:
        return products.head(n_recommendations)[["slug", "title", "catigory", "price"]]
    else:
        return recommendations.head(n_recommendations)[
            ["slug", "title", "catigory", "price", "similarity"]
        ]
