from uuid import UUID

from fastapi import APIRouter, status

from src.modules.exports.schemas import ExportOut, ExportRequest
from src.platform.errors import NotImplementedYet

router = APIRouter(prefix="/exports", tags=["exports"])


@router.post("", response_model=ExportOut, status_code=status.HTTP_201_CREATED)
async def create_export(body: ExportRequest):
    """Export approved documents only."""
    raise NotImplementedYet("exports.create")


@router.get("/{export_id}/download")
async def download_export(export_id: UUID):
    """Stream the generated CSV."""
    raise NotImplementedYet("exports.download")