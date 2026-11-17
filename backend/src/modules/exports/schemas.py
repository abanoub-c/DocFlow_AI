from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class ExportTarget(str, Enum):
    csv = "csv"
    # google_sheets = "google_sheets"  # later
    # webhook = "webhook"              # later


class ExportRequest(BaseModel):
    document_ids: list[UUID] = Field(min_length=1)
    target: ExportTarget = ExportTarget.csv


class ExportOut(BaseModel):
    id: UUID
    target: ExportTarget
    state: str
    document_count: int