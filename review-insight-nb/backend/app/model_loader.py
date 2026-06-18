from app.schemas import ModelInfoResponse


def get_model_info() -> ModelInfoResponse:
    return ModelInfoResponse(
        model="Multinomial Naive Bayes",
        vectorizer="TfidfVectorizer",
        status="not_trained",
        trained=False,
    )
