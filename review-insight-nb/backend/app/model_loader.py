from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib

from app.schemas import ModelInfoResponse


BASE_DIR = Path(__file__).resolve().parents[1]
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "sentiment_model.joblib"
VECTORIZER_PATH = MODELS_DIR / "vectorizer.joblib"


@dataclass(frozen=True)
class ModelBundle:
    model: Any
    vectorizer: Any


@lru_cache(maxsize=1)
def load_model_bundle() -> ModelBundle:
    if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
        raise FileNotFoundError(
            "Model artifacts not found. Run `uv run python ml/train_model.py` first."
        )

    return ModelBundle(
        model=joblib.load(MODEL_PATH),
        vectorizer=joblib.load(VECTORIZER_PATH),
    )


def get_model_info() -> ModelInfoResponse:
    trained = MODEL_PATH.exists() and VECTORIZER_PATH.exists()

    return ModelInfoResponse(
        model="Multinomial Naive Bayes",
        vectorizer="TfidfVectorizer",
        status="trained" if trained else "not_trained",
        trained=trained,
    )
