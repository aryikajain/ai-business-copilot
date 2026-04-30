# Retriever will be implemented here
import os
import faiss
import pickle
import numpy as np
from rag.embedder import embed_text


BASE_VECTOR_PATH = "data/vectorstores"


def retrieve_context(user_id, query, top_k=3):
    """
    Retrieve most relevant business context for a user query
    """

    user_folder = os.path.join(BASE_VECTOR_PATH, user_id)

    index_path = os.path.join(user_folder, "faiss_index.bin")
    chunks_path = os.path.join(user_folder, "chunks.pkl")

    # ensure files exist
    if not os.path.exists(index_path) or not os.path.exists(chunks_path):
        return []

    # load FAISS index
    index = faiss.read_index(index_path)

    # load text chunks
    with open(chunks_path, "rb") as f:
        text_chunks = pickle.load(f)

    # embed query
    query_vector = np.array(embed_text([query])).astype("float32")

    # search
    distances, indices = index.search(query_vector, top_k)

    results = []
    for idx in indices[0]:
        if idx < len(text_chunks):
            results.append(text_chunks[idx])

    return results