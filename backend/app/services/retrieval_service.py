from typing import List, Dict, Any


class RetrievalService:
    def __init__(self, embedding_service, vector_db):
        self.embedding_service = embedding_service
        self.vector_db = vector_db

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        document_id = None
    ) -> List[Dict[str, Any]]:

        query_embedding = self.embedding_service.embed_text(query)

        results = self.vector_db.query(
            query_embedding=query_embedding,
            top_k=top_k,
            document_id=document_id
        )

        print("\n--- RETRIEVED CHUNKS ---")
        for r in results:
            print(r["text"][:200])

        results = sorted(results, key=lambda x: x["score"])
        results = self._deduplicate(results)

        return self._format_results(results)

    def _format_results(self, results):
        formatted = []

        for r in results:
            formatted.append({
                "text": r["text"],
                "source": r["metadata"].get("source"),
                "document_id": r["metadata"].get("document_id"),
                "score": r["score"]
            })

        return formatted

    def _deduplicate(self, results):
        seen = set()
        unique = []

        for r in results:
            key = r["text"][:100]
            if key not in seen:
                seen.add(key)
                unique.append(r)

        return unique