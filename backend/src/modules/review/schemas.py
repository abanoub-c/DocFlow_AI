from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class ReviewItem(BaseModel):
    extraction_id: UUID
    document_id: UUID
    filename: str
    fields: dict[str, Any]
    confidences: dict[str, float]
    validation_errors: list[str] = Field(default_factory=list)


class ReviewQueue(BaseModel):
    items: list[ReviewItem]
    total: int


class ApproveRequest(BaseModel):
    # field name -> corrected value. Empty means approve as-is.
    corrections: dict[str, Any] = Field(default_factory=dict)


class RejectRequest(BaseModel):
    reason: str = Field(min_length=1, max_length=500)


class ReviewResult(BaseModel):
    extraction_id: UUID
    status: str