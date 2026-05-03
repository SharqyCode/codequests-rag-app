
import uuid
from app.utils.logger import setup_logger

logger = setup_logger("ingestion_service")


class IngestionService:

    def __init__(self, parser, chunker, embedding_service, vector_db):
        self.parser = parser
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.vector_db = vector_db

    def _process_file(self, file):
        document_id = str(uuid.uuid4())
        logger.info(f"Starting processing file: {file.filename} | doc_id={document_id}")

        try:
            text = self.parser.parse(file)

            if not text.strip():
                logger.warning(f"Empty document: {file.filename}")
                raise ValueError("Empty document")

            chunks = self.chunker.chunk(text)
            logger.info(f"{file.filename}: Generated {len(chunks)} chunks")

            chunk_records = [
                {
                    "id": str(uuid.uuid4()),
                    "document_id": document_id,
                    "text": chunk,
                    "source": file.filename
                }
                for chunk in chunks
            ]

            texts = [c["text"] for c in chunk_records]

            logger.info(f"{file.filename}: Generating embeddings...")
            embeddings = self.embedding_service.embed_batch(texts)

            if len(embeddings) != len(chunk_records):
                logger.error("Embedding count mismatch")
                raise RuntimeError("Embedding mismatch")

            for i, emb in enumerate(embeddings):
                chunk_records[i]["embedding"] = emb

            logger.info(f"{file.filename}: Storing {len(chunk_records)} chunks in DB")
            self.vector_db.insert_chunks(chunk_records)

            logger.info(f"Finished processing file: {file.filename}")
            return document_id

        except Exception as e:
            logger.error(f"Failed processing {file.filename}: {str(e)}", exc_info=True)
            raise

    def ingest_files(self, files):
        document_ids = []

        for file in files:
            try:
                doc_id = self._process_file(file)
                document_ids.append(doc_id)
            except Exception as e:
                logger.error(f"Skipping file {file.filename} due to error")

        return document_ids