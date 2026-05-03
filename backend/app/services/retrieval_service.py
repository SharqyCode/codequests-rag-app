from app.utils.logger import setup_logger

logger = setup_logger("retrieval_service")


class RetrievalService:

    def __init__(self, embedding_service, vector_db):
        self.embedding_service = embedding_service
        self.vector_db = vector_db

    def retrieve(self, query, top_k=5, document_id=None):
        logger.info(f"Retrieving for query: {query[:100]}")

        try:
            query_embedding = self.embedding_service.embed_text(query)

            results = self.vector_db.query(
                query_embedding=query_embedding,
                top_k=top_k,
                document_id=document_id
            )

            logger.info(f"Retrieved {len(results)} raw results")

            if not results:
                logger.warning("No results found")

            results = sorted(results, key=lambda x: x["score"])
            results = self._deduplicate(results)

            logger.info(f"{len(results)} results after deduplication")

            return self._format_results(results)

        except Exception as e:
            logger.error(f"Retrieval failed: {str(e)}", exc_info=True)
            raise