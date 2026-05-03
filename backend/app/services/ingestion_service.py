import uuid
from fastapi import UploadFile

class IngestionService:

    def __init__(
    self,
    parser,
    chunker,
    embedding_service,
    vector_db
    ):
        self.parser = parser
        self.chunker = chunker
        self.embedding_service = embedding_service
        self.vector_db = vector_db

    def _process_file(self, file: UploadFile) -> str:
        document_id = str(uuid.uuid4())
        text = self.parser.parse(file)
        
        # print("text:", text)
        if not text.strip():
            raise ValueError("Empty document")
        chunks = self.chunker.chunk(text)
        
        print(f"Generated {len(chunks)} chunks")
        
        chunk_records = [
        {
            "id": str(uuid.uuid4()),
            "document_id": document_id,
            "text": chunk,
            "source": file.filename
        }
        for chunk in chunks
        ]

        # print(f"chunk_records: {chunk_records}")

        texts = [c["text"] for c in chunk_records]


        embeddings = self.embedding_service.embed_batch(texts)

        # print(f"ingestion.embedding:{embeddings}")

        assert len(embeddings) == len(chunk_records)

        for i, emb in enumerate(embeddings):
            chunk_records[i]["embedding"] = emb

        self.vector_db.insert_chunks(chunk_records)
        return document_id

    def ingest_files(self, files):
        document_ids = []

        for file in files:
            try:
                doc_id = self._process_file(file)
                # print(f"ingest.doc_id {doc_id}")
                document_ids.append(doc_id)
            except Exception as e:
                print(f"Failed to process {file.filename}: {e}")
            
        return document_ids
    
    def clear_all_documents(self):
        self.vector_db.clear_collection()

