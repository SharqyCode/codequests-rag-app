from services.embedding_service import EmbeddingService
from db.chroma_client import ChromaClient
from services.ai_service import AIService

# ebmedder  = EmbeddingService()

# embedded_text = ebmedder.embed_batch(texts=["Golden Retrievers are widely considered", "one of the most beloved dog breeds in the world", "renowned for their gentle temperament and striking 'sunny' appearance"])
# print(embedded_text)


cclient = ChromaClient()

# ChromaClient.insert_chunks()

# embedder  = EmbeddingService()
# embedded_text = embedder.embed_text("golden retrievers are nice")
# cclient.query(query_embedding=embedded_text);

