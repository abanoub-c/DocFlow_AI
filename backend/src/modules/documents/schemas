from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class DocType(str, Enum):
    invoice = "invoice"
    receipt = "receipt"


class DocumentStatus(str, Enum):
    queued = "queued"
    processing = "processing"
    needs_review = "needs_review"
    approved = "approved"
    rejected = "rejected"
    failed = "failed"


class DocumentOut(BaseModel):
    id: UUID
    filename: str
    doc_type: DocType
    status: DocumentStatus
    page_count: int | None = None
    created_at: datetime


class ExtractionOut(BaseModel):
    id: UUID
    schema_version: str
    prompt_version: str
    model: str
    fields: dict[str, Any]
    confidences: dict[str, float]
    validation_errors: list[str] = Field(default_factory=list)


class DocumentDetail(DocumentOut):
    extraction: ExtractionOut | None = None


class DocumentList(BaseModel):
    items: list[DocumentOut]
    total: int