from sentence_transformers import SentenceTransformer

# Load once when the app starts
embedding_model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def get_embedding(text: str) -> list[float]:
    """
    Generate a real 384-dimensional embedding for a text string.
    """
    vector = embedding_model.encode(text, normalize_embeddings=True)
    return vector.tolist()
