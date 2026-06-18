from fastapi import FastAPI

from app.schemas import HealthResponse, PredictRequest, PredictResponse
from app.services.sentiment_service import predict_sentiment

app = FastAPI(
    title="Review Insight NB API",
    description="Naive Bayes 기반 리뷰 감성 분석 API",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/api/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    return predict_sentiment(request)

