from fastapi import APIRouter, UploadFile, File
from app.schemas.ingest_schema import ExternalSourceRequest
from typing import List

from app.dependencies import ingestion_service

router = APIRouter(prefix="/api/ingest", tags=["Ingestion"])


@router.post("/files")
async def ingest_files(files: List[UploadFile] = File(...)):
    document_ids = ingestion_service.ingest_files(files)

    return {
        "message": "Files processed successfully",
        "document_ids": document_ids
    }

@router.post("/source")
def ingest_source(payload: ExternalSourceRequest):
    try:
        document_id = ingestion_service.ingest_external_source(
            payload.source_type,
            payload.data
        )

        return {
            "status": "success",
            "document_id": document_id
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }