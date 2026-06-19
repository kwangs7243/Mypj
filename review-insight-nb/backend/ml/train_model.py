from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "preprocessed_reviews.csv"
MODELS_DIR = BASE_DIR / "models"
MODEL_PATH = MODELS_DIR / "sentiment_model.joblib"
VECTORIZER_PATH = MODELS_DIR / "vectorizer.joblib"
REQUIRED_COLUMNS = {"text", "label"}


def load_training_data(path: Path = DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Preprocessed dataset not found: {path}. "
            "Run `uv run python ml/preprocess.py` first."
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


def train_model(data: pd.DataFrame) -> tuple[MultinomialNB, TfidfVectorizer]:
    texts = data["text"]
    labels = data["label"]

    x_train, x_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels,
    )

    vectorizer = TfidfVectorizer()
    x_train_vectorized = vectorizer.fit_transform(x_train)
    x_test_vectorized = vectorizer.transform(x_test)

    model = MultinomialNB()
    model.fit(x_train_vectorized, y_train)

    predictions = model.predict(x_test_vectorized)
    accuracy = accuracy_score(y_test, predictions)

    print(f"Train rows: {len(x_train)}")
    print(f"Test rows: {len(x_test)}")
    print(f"Accuracy: {accuracy:.4f}")
    print("Classification report:")
    print(classification_report(y_test, predictions, zero_division=0))

    return model, vectorizer


def save_artifacts(
    model: MultinomialNB,
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
