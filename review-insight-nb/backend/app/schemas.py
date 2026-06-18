from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, description="분석할 리뷰 텍스트")


class PredictResponse(BaseModel):
    label: str
    confidence: float
    probabilities: dict[str, float]

