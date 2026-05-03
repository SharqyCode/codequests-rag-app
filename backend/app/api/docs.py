from fastapi import APIRouter
from app.dependencies import vector_db

router = APIRouter(prefix="/api/docs", tags=["Documents"])


@router.get("/")
def list_documents():
    docs = vector_db.get_all_documents()
    print("docs api")
    return {"documents": docs}

@router.get("/{doc_id}")
async def fetch_document(doc_id: str):
    """
    API endpoint to fetch a specific document by its ID.
    """
    # Call the helper function
    doc_data = vector_db.get_document_by_id(doc_id)
    
    # If the helper returned None, the ID wasn't in the database
    if doc_data is None:
        raise HTTPException(
            status_code=404, 
            detail=f"Document with ID '{doc_id}' not found."
        )
        
    # Return the formatted document data (FastAPI automatically converts this to JSON)
    return doc_data


@router.delete("/truncate")
def truncate_collection():
    vector_db.clear_collection()
    return {"message": "Collection cleared"}