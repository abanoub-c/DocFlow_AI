from fastapi import APIRouter

from src.modules.metrics.schemas import MetricsSummary
from src.platform.errors import NotImplementedYet

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/summary", response_model=MetricsSummary)
async def summary():
    raise NotImplementedYet("metrics.summary")