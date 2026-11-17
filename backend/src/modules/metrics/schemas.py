from pydantic import BaseModel


class MetricsSummary(BaseModel):
    documents_total: int
    auto_approve_rate: float
    review_rate: float
    failure_rate: float
    avg_latency_ms: float
    avg_cost_usd: float