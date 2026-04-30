try:
    from sentence_transformers import SentenceTransformer
    embedding_model = SentenceTransformer("all-MiniLM-L6-v2")
except Exception:
    embedding_model = None


def embed_text(text_chunks):
    """
    Convert text chunks into embeddings.
    Safe fallback if sentence-transformers is unavailable.
    """
    if embedding_model is None:
        return []

    return embedding_model.encode(text_chunks).tolist()