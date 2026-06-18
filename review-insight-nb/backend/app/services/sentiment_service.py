from app.schemas import PredictRequest, PredictResponse


def predict_sentiment(request: PredictRequest) -> PredictResponse:
    text = request.text.strip()

    if any(word in text for word in ["좋", "만족", "추천", "빠르", "최고"]):
        return PredictResponse(
            label="positive",
            confidence=0.75,
            probabilities={"positive": 0.75, "negative": 0.25},
        )

    return PredictResponse(
        label="negative",
        confidence=0.62,
        probabilities={"positive": 0.38, "negative": 0.62},
    )

