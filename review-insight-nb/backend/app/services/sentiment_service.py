from fastapi import HTTPException

from app.model_loader import load_model_bundle
from app.schemas import PredictRequest, PredictResponse
from ml.preprocess import clean_text


def predict_sentiment(request: PredictRequest) -> PredictResponse:
    bundle = load_model_bundle()
    text = clean_text(request.text)

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Review text must contain Korean characters.",
        )

    vectorized_text = bundle.vectorizer.transform([text])

    predicted_label = bundle.model.predict(vectorized_text)[0]
    predicted_probabilities = bundle.model.predict_proba(vectorized_text)[0]
    probabilities = {
        label: float(probability)
        for label, probability in zip(
            bundle.model.classes_,
            predicted_probabilities,
            strict=True,
        )
    }

    return PredictResponse(
        label=str(predicted_label),
        confidence=max(probabilities.values()),
        probabilities=probabilities,
    )
