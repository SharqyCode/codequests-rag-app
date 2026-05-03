from fastapi import APIRouter, UploadFile, File
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