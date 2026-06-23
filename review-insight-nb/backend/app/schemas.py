from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class ModelInfoResponse(BaseModel):
    model: str
    tokenizer: str
    vectorizer: str
    preprocessing: str
    status: str
    trained: bool


class PredictRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Review text to analyze")


class PredictResponse(BaseModel):
    label: str
    confidence: float
    probabilities: dict[str, float]
