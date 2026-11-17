from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Query

from src.modules.review.schemas import (
    ApproveRequest,
    RejectRequest,
    ReviewQueue,
    ReviewResult,
)
from src.platform.errors import NotImplementedYet

router = APIRouter(prefix="/review", tags=["review"])


def build_review_events(
    extraction_id: UUID,
    old_fields: dict[str, Any],
    new_fields: dict[str, Any],
    user_id: UUID,
    *,
    action: str = "approve",
    created_at: datetime | None = None,
) -> list[dict[str, Any]]:
    """Build one audit record for each field whose value changed."""
    timestamp = created_at or datetime.now(UTC)
    events = []
    for field in old_fields.keys() | new_fields.keys():
        old_value = old_fields.get(field)
        new_value = new_fields.get(field)
        if (
            field not in old_fields
            or field not in new_fields
            or old_value != new_value
        ):
            events.append(
                {
                    "extraction_id": extraction_id,
                    "user_id": user_id,
                    "action": action,
                    "field": field,
                    "old_value": old_value,
                    "new_value": new_value,
                    "created_at": timestamp,
                }
            )
    return events


@router.get("/queue", response_model=ReviewQueue)
async def review_queue(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    raise NotImplementedYet("review.queue")


@router.post("/{extraction_id}/approve", response_model=ReviewResult)
async def approve(extraction_id: UUID, body: ApproveRequest):
    raise NotImplementedYet("review.approve")


@router.post("/{extraction_id}/reject", response_model=ReviewResult)
async def reject(extraction_id: UUID, body: RejectRequest):
    raise NotImplementedYet("review.reject")
