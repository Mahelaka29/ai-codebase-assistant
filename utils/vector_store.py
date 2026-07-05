import faiss
import numpy as np


def build_vector_store(embeddings):
    """
    Build a FAISS index from embeddings.
    """
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(np.asarray(embeddings, dtype="float32"))

    return index


def search(index, model, chunks, query, k=5):
    """
    Perform semantic search.
    """
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    scores, indices = index.search(
        np.asarray(query_embedding, dtype="float32"),
        k
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        if idx == -1:
            continue

        chunk = chunks[idx].copy()
        chunk["score"] = float(score)

        results.append(chunk)

    return results