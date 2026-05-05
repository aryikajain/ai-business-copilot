# try:
#     from sentence_transformers import SentenceTransformer
#     embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
# except Exception:
#     embedding_model = None


# def embed_text(text_chunks):
#     """
#     Convert text chunks into embeddings.
#     Safe fallback if sentence-transformers is unavailable.
#     """
#     if embedding_model is None:
#         return []

#     return embedding_model.encode(text_chunks).tolist()
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

BASE_VECTOR_PATH = "data/vectorstores"

vectorizer = TfidfVectorizer()


def embed_text(text_chunks, user_id):
    """
    Fit vectorizer + save it per user
    """
    vectors = vectorizer.fit_transform(text_chunks)

    user_folder = os.path.join(BASE_VECTOR_PATH, user_id)
    os.makedirs(user_folder, exist_ok=True)

    # save vectorizer
    with open(os.path.join(user_folder, "vectorizer.pkl"), "wb") as f:
        pickle.dump(vectorizer, f)

    return vectors.toarray().tolist()


def embed_query(query, user_id):
    """
    Load vectorizer + transform query
    """
    user_folder = os.path.join(BASE_VECTOR_PATH, user_id)

    vectorizer_path = os.path.join(user_folder, "vectorizer.pkl")

    if not os.path.exists(vectorizer_path):
        return []

    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

    return vectorizer.transform([query]).toarray().tolist()