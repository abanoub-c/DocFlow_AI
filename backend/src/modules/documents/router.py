from uuid import UUID

from fastapi import APIRouter, File, Form, Query, UploadFile, status

from src.modules.documents.schemas import (
    DocType,
    DocumentDetail,
    DocumentList,
    DocumentOut,
    DocumentStatus,
)
from src.platform.errors import NotImplementedYet

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("", response_model=list[DocumentOut], status_code=status.HTTP_202_ACCEPTED)
async def upload_documents(
    files: list[UploadFile] = File(...),
    doc_type: DocType = Form(DocType.invoice),
):
    """Upload one or many files. Returns 202: processing happens in the background."""
    # TODO: service.upload(files, doc_type) -> validate (magic bytes, size, pages),
    #       hash for idempotency, store file, create document, enqueue process_document job
    raise NotImplementedYet("documents.upload")


@router.get("", response_model=DocumentList)
async def list_documents(
    status_filter: DocumentStatus | None = Query(None, alias="status"),
    doc_type: DocType | None = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    raise NotImplementedYet("documents.list")


@router.get("/{document_id}", response_model=DocumentDetail)
async def get_document(document_id: UUID):
    raise NotImplementedYet("documents.get")


@router.get("/{document_id}/file")
async def get_document_file(document_id: UUID):
    """Signed URL / stream of the original file, for the review viewer."""
    raise NotImplementedYet("documents.file")


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: UUID):
    """Delete the document, its file, and all derived data."""
    raise NotImplementedYet("documents.delete")