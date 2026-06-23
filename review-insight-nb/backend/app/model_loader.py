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
SENTENCEPIECE_MODEL_PATH = MODELS_DIR / "sentencepiece.model"


@dataclass(frozen=True)
class ModelBundle:
    model: Any
    vectorizer: Any
    tokenizer: Any


@lru_cache(maxsize=1)
def load_model_bundle() -> ModelBundle:
    artifact_paths = [MODEL_PATH, VECTORIZER_PATH, SENTENCEPIECE_MODEL_PATH]
    if not all(path.exists() for path in artifact_paths):
        raise FileNotFoundError(
            "Model artifacts not found. Run `uv run python ml/train_model.py` first."
        )

    from ml.tokenizers.text_tokenizers import SentencePieceTokenizer

    return ModelBundle(
        model=joblib.load(MODEL_PATH),
        vectorizer=joblib.load(VECTORIZER_PATH),
        tokenizer=SentencePieceTokenizer(SENTENCEPIECE_MODEL_PATH),
    )


def get_model_info() -> ModelInfoResponse:
    trained = all(
        path.exists()
        for path in [MODEL_PATH, VECTORIZER_PATH, SENTENCEPIECE_MODEL_PATH]
    )

    return ModelInfoResponse(
        model="Logistic Regression",
        tokenizer="SentencePiece",
        vectorizer="TfidfVectorizer",
        preprocessing="light",
        status="trained" if trained else "not_trained",
        trained=trained,
    )
