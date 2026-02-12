from rank_bm25 import BM25Okapi

class SparseRetriever:
    def __init__(self):
        self.docs = []
        self.bm25 = None

    def index(self, documents: list[str]):
        self.docs = documents
        tokenized = [doc.split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)

    def search(self, query: str, top_k: int = 3):
        if not self.bm25:
            return []
        scores = self.bm25.get_scores(query.split())
        ranked = sorted(
            zip(self.docs, scores),
            key=lambda x: x[1],
            reverse=True
        )
        return [doc for doc, _ in ranked[:top_k]]
