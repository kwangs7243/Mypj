from app.schemas import PredictRequest, PredictResponse

POSITIVE_HINTS = [
    "\uc88b",  # 좋
    "\ub9cc\uc871",  # 만족
    "\ucd94\ucc9c",  # 추천
    "\ube60\ub974",  # 빠르
    "\ucd5c\uace0",  # 최고
]


def predict_sentiment(request: PredictRequest) -> PredictResponse:
    text = request.text.strip()

    if any(word in text for word in POSITIVE_HINTS):
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
