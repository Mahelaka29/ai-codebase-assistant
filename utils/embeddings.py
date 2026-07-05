from sentence_transformers import SentenceTransformer
import streamlit as st


@st.cache_resource
def get_model():
    """
    Load the embedding model once.
    """
    return SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """
    Generate embeddings for all code chunks.
    """
    model = get_model()

    texts = [chunk["text"] for chunk in chunks]

    embeddings = model.encode(
        texts,
        batch_size=32,
        show_progress_bar=False,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings