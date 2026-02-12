import numpy as np

def embed_text(text: str) -> list[float]:
    # Temporary stub embedding (replace later)
    np.random.seed(abs(hash(text)) % (10**6))
    return np.random.rand(384).tolist()

