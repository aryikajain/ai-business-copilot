import os
import faiss
import pickle
import numpy as np
from sklearn.preprocessing import normalize


BASE_VECTOR_PATH = "data/vectorstores"


def save_to_vectorstore(
    user_id,
    text_chunks,
    embeddings
):

    """
    Save embeddings + chunks into
    user-specific FAISS vector memory
    """

    if not text_chunks or not embeddings:
        return

    user_folder = os.path.join(
        BASE_VECTOR_PATH,
        user_id
    )

    os.makedirs(user_folder, exist_ok=True)

    index_path = os.path.join(
        user_folder,
        "faiss_index.bin"
    )

    chunks_path = os.path.join(
        user_folder,
        "chunks.pkl"
    )

    metadata_path = os.path.join(
        user_folder,
        "metadata.pkl"
    )

    # convert embeddings
    vectors = np.array(
        embeddings
    ).astype("float32")

    # normalize vectors
    vectors = normalize(vectors)

    dimension = vectors.shape[1]

    # COSINE SIMILARITY INDEX
    index = faiss.IndexFlatIP(dimension)

    # add vectors
    index.add(vectors)

    # save index
    faiss.write_index(
        index,
        index_path
    )

    # save chunks
    with open(chunks_path, "wb") as f:

        pickle.dump(text_chunks, f)

    # OPTIONAL METADATA
    metadata = []

    for chunk in text_chunks:

        metadata.append({
            "text": chunk,
            "length": len(chunk),
        })

    with open(metadata_path, "wb") as f:

        pickle.dump(metadata, f)

    print(
        f"Saved {len(text_chunks)} chunks "
        f"for user {user_id}"
    )