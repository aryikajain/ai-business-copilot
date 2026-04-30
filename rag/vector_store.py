# Vector store will be implemented here
import os
import faiss
import numpy as np
import pickle


BASE_VECTOR_PATH = "data/vectorstores"


def save_to_vectorstore(user_id, text_chunks, embeddings):
    """
    Save text chunks + embeddings into user-specific FAISS index
    """

    user_folder = os.path.join(BASE_VECTOR_PATH, user_id)
    os.makedirs(user_folder, exist_ok=True)

    # convert embeddings to numpy
    vectors = np.array(embeddings).astype("float32")

    # create FAISS index
    dimension = vectors.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    # save FAISS index
    faiss.write_index(index, os.path.join(user_folder, "faiss_index.bin"))

    # save original text chunks
    with open(os.path.join(user_folder, "chunks.pkl"), "wb") as f:
        pickle.dump(text_chunks, f)