import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from pathlib import Path

class ChromaClient:
    def __init__(self, persist_dir: str = None):

        if persist_dir is None:
            # chroma_client.py → db → app → backend
            base_dir = Path(__file__).resolve().parent.parent
            persist_dir = base_dir / "data" / "chroma"

        self.client = chromadb.Client(
            Settings(
                is_persistent=True,
                persist_directory=str(persist_dir),
                anonymized_telemetry=False
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="documents"
        )

    def insert_chunks(self, chunk_records: List[Dict[str, Any]]):
        ids = []
        documents = []
        embeddings = []
        metadatas = []

        for chunk in chunk_records:
            ids.append(chunk["id"])
            documents.append(chunk["text"])
            embeddings.append(chunk["embedding"])

            metadatas.append({
                "document_id": chunk["document_id"],
                "source": chunk.get("source", "")
            })

        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        document_id: Optional[str]  = None
    ):
    
        where: Optional[Dict[str, Any]] = (
            {"document_id": document_id} if document_id else None
        )

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where
        )

        print("results:", results)

        if not results or not results.get("ids"):
            return []

        chunks = []

        for i in range(len(results["ids"][0])):
            chunks.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "score": results["distances"][0][i]
            })

        print(chunks)
        return chunks
    
    def get_all_documents(self):
        docs: chromadb.GetResult = self.collection.get()
        documents = []
        for id in docs["ids"]:
            documents.append({"document_id": id})
        for i, metadata in enumerate(docs["metadatas"]):
            documents[i]["source"] = metadata["source"]
        print(documents)
        return documents


       
    

    def get_document_by_id(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single document from ChromaDB by its ID.
        Returns a dictionary of the document data or None if not found.
        """
        # Query ChromaDB (omitting embeddings by default for performance)
        result: chromadb.GetResult = self.collection.get(
            ids=[doc_id],
            include=["documents", "metadatas"] 
        )
        
        # Chroma returns empty lists if the ID is not found
        if not result or not result.get("ids"):
            return None
            
        # Safely extract the first item from the returned lists
        
        return {
            "document_id": result["ids"][0],
            "source": result["metadatas"][0]["source"] if result.get("metadatas") else None,
            "content": result["documents"][0] if result.get("documents") else None
        }
    
    def clear_collection(self):
        self.collection.delete(where={})