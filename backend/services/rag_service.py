# RAG service will be implemented here
from rag.embedder import embed_text
from rag.vector_store import save_to_vectorstore
from rag.retriever import retrieve_context


# def build_rag_memory(user_id, analysis):
#     """
#     Convert business analysis into text chunks
#     and store them in FAISS memory
#     """

#     text_chunks = []

#     # metrics → text
#     for key, value in analysis.get("metrics", {}).items():
#         text_chunks.append(f"{key} is {value}")

#     # business insights → text
#     for insight in analysis.get("insights", []):
#         text_chunks.append(insight)

#     if not text_chunks:
#         return

#     embeddings = embed_text(text_chunks)
#     save_to_vectorstore(user_id, text_chunks, embeddings)
def build_rag_memory(user_id, analysis):
    text_chunks = []

    for key, value in analysis.get("metrics", {}).items():
        text_chunks.append(f"{key} is {value}")

    for insight in analysis.get("insights", []):
        text_chunks.append(insight)

    print("RAG TEXT CHUNKS:", text_chunks)

    if not text_chunks:
        print("RAG SKIPPED: no text chunks")
        return

    embeddings = embed_text(text_chunks, user_id)
    print("RAG EMBEDDINGS COUNT:", len(embeddings))

    if not embeddings:
        print("RAG SKIPPED: embeddings unavailable")
        return

    save_to_vectorstore(user_id, text_chunks, embeddings)
    print("RAG MEMORY SAVED")

def get_rag_context(user_id, query):
    """
    Retrieve relevant business memory for a user query
    """
    return retrieve_context(user_id, query)