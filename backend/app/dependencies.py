from app.services.ingestion_service import IngestionService
from app.services.embedding_service import EmbeddingService
from app.services.retrieval_service import RetrievalService
from app.services.ai_service import AIService

from app.utils.file_parsers import FileParser
from app.utils.chunking import TextChunker
from app.db.chroma_client import ChromaClient

# Shared instances (singleton-style)
embedding_service = EmbeddingService()
vector_db = ChromaClient()

parser = FileParser()
chunker = TextChunker()

ingestion_service = IngestionService(
    parser=parser,
    chunker=chunker,
    embedding_service=embedding_service,
    vector_db=vector_db
)

retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    vector_db=vector_db
)

ai_service = AIService()