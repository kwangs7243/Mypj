import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score

BASE_DIR = Path(__file__).resolve().parents[1]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ml.tokenizers.text_tokenizers import SentencePieceTokenizer

DATA_PATH = BASE_DIR / "data" / "splits" / "nsmc_light_train.csv"
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "sentiment_model.joblib"
VECTORIZER_PATH = MODELS_DIR / "vectorizer.joblib"
SENTENCEPIECE_MODEL_PATH = MODELS_DIR / "sentencepiece.model"
REQUIRED_COLUMNS = {"text", "label"}


def load_training_data(path: Path = DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Training dataset not found: {path}. "
            "Run `uv run python ml/experiments/convert_nsmc_dataset.py --mode light "
            "--train-output data/splits/nsmc_light_train.csv "
            "--test-output data/splits/nsmc_light_test.csv` first."
        )

    data = pd.read_csv(path)
    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    data = data.dropna(subset=["text", "label"]).copy()
    data["text"] = data["text"].astype(str).str.strip()
    data["label"] = data["label"].astype(str).str.strip()
    data = data[data["text"].str.len() > 0]

    if data.empty:
        raise ValueError("No valid training rows found.")

    return data


def tokenize_texts(texts: pd.Series, tokenizer: SentencePieceTokenizer) -> list[str]:
    return [" ".join(tokenizer(text)) for text in texts]


def train_model(data: pd.DataFrame) -> tuple[LogisticRegression, TfidfVectorizer]:
    if not SENTENCEPIECE_MODEL_PATH.exists():
        raise FileNotFoundError(
            f"SentencePiece model not found: {SENTENCEPIECE_MODEL_PATH}. "
            "Run `uv run python ml/tokenizers/train_sentencepiece.py "
            "--model-prefix models/sentencepiece` first."
        )

    tokenizer = SentencePieceTokenizer(SENTENCEPIECE_MODEL_PATH)
    texts = tokenize_texts(data["text"], tokenizer)
    labels = data["label"]

    vectorizer = TfidfVectorizer(
        tokenizer=str.split,
        token_pattern=None,
        lowercase=False,
    )
    x_train_vectorized = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=1000)
    model.fit(x_train_vectorized, labels)

    predictions = model.predict(x_train_vectorized)
    accuracy = accuracy_score(labels, predictions)
    macro_f1 = f1_score(labels, predictions, average="macro", zero_division=0)

    print(f"Train rows: {len(texts)}")
    print(f"Training accuracy: {accuracy:.4f}")
    print(f"Training macro F1: {macro_f1:.4f}")
    print("Training classification report:")
    print(classification_report(labels, predictions, zero_division=0))

    return model, vectorizer


def save_artifacts(
    model: LogisticRegression,
    vectorizer: TfidfVectorizer,
    model_path: Path = MODEL_PATH,
    vectorizer_path: Path = VECTORIZER_PATH,
) -> None:
    model_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vectorizer_path)

    print(f"Saved model to: {model_path}")
    print(f"Saved vectorizer to: {vectorizer_path}")


def main() -> None:
    data = load_training_data()
    model, vectorizer = train_model(data)
    save_artifacts(model, vectorizer)


if __name__ == "__main__":
    main()
