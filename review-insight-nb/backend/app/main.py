from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.model_loader import get_model_info
from app.schemas import (
    HealthResponse,
    ModelInfoResponse,
    PredictRequest,
    PredictResponse,
)
from app.services.sentiment_service import predict_sentiment

app = FastAPI(
    title="Review Insight NB API",
    description="Review sentiment analysis API with a Naive Bayes model",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/api/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    return predict_sentiment(request)


@app.get("/api/model-info", response_model=ModelInfoResponse)
def model_info() -> ModelInfoResponse:
    return get_model_info()
