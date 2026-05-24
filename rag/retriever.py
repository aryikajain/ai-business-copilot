# # Retriever will be implemented here
# import os
# import faiss
# import pickle
# import numpy as np
# from rag.embedder import embed_text


# BASE_VECTOR_PATH = "data/vectorstores"


# def retrieve_context(user_id, query, top_k=3):
#     """
#     Retrieve most relevant business context for a user query
#     """

#     user_folder = os.path.join(BASE_VECTOR_PATH, user_id)

#     index_path = os.path.join(user_folder, "faiss_index.bin")
#     chunks_path = os.path.join(user_folder, "chunks.pkl")

#     # ensure files exist
#     if not os.path.exists(index_path) or not os.path.exists(chunks_path):
#         return []

#     # load FAISS index
#     index = faiss.read_index(index_path)

#     # load text chunks
#     with open(chunks_path, "rb") as f:
#         text_chunks = pickle.load(f)

#     # embed query
#     query_vector = np.array(embed_text([query])).astype("float32")

#     # search
#     distances, indices = index.search(query_vector, top_k)

#     results = []
#     for idx in indices[0]:
#         if idx < len(text_chunks):
#             results.append(text_chunks[idx])

#     return results

import os
import faiss
import pickle
import numpy as np

from rag.embedder import embed_query


BASE_VECTOR_PATH = "data/vectorstores"


def retrieve_context(
    user_id,
    query,
    top_k=5,
    similarity_threshold=0.15
):

    """
    Retrieve most relevant business context
    using semantic similarity search
    """

    user_folder = os.path.join(
        BASE_VECTOR_PATH,
        user_id
    )

    index_path = os.path.join(
        user_folder,
        "faiss_index.bin"
    )

    chunks_path = os.path.join(
        user_folder,
        "chunks.pkl"
    )

    # validate storage
    if (
        not os.path.exists(index_path)
        or not os.path.exists(chunks_path)
    ):
        return []

    try:

        # load FAISS index
        index = faiss.read_index(index_path)

        # load chunks
        with open(chunks_path, "rb") as f:

            text_chunks = pickle.load(f)

        # embed query
        query_embedding = embed_query(
            query,
            user_id
        )

        if not query_embedding:
            return []

        query_vector = np.array(
            query_embedding
        ).astype("float32")

        # search
        distances, indices = index.search(
            query_vector,
            top_k
        )

        results = []

        used_chunks = set()

        for score, idx in zip(
            distances[0],
            indices[0]
        ):

            # invalid index
            if idx < 0 or idx >= len(text_chunks):
                continue

            # similarity filtering
            if score < similarity_threshold:
                continue

            chunk = text_chunks[idx]

            # deduplicate
            if chunk in used_chunks:
                continue

            used_chunks.add(chunk)

            results.append({
                "text": chunk,
                "score": round(float(score), 4),
            })

        # sort by score descending
        results = sorted(
            results,
            key=lambda x: x["score"],
            reverse=True
        )

        # return only text
        return [r["text"] for r in results]

    except Exception as e:

        print(f"RAG RETRIEVAL ERROR: {e}")

        return []