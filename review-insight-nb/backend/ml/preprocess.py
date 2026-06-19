from pathlib import Path
import re

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "sample_reviews.csv"
PREPROCESSED_DATA_PATH = DATA_DIR / "preprocessed_reviews.csv"
VALID_LABELS = {"positive", "negative"}


def clean_text(value: str) -> str:
    text = str(value).strip()
    text = re.sub(r"[^가-힣\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def load_raw_reviews(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {path}")

    reviews = pd.read_csv(path)
    required_columns = {"text", "label"}
    missing_columns = required_columns - set(reviews.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    return reviews


def preprocess_reviews(reviews: pd.DataFrame) -> pd.DataFrame:
    processed = reviews.dropna(subset=["text", "label"]).copy()
    processed["original_text"] = processed["text"].astype(str)
    processed["text"] = processed["text"].apply(clean_text)
    processed["label"] = processed["label"].astype(str).str.strip().str.lower()

    processed = processed[processed["text"] != ""]
    processed = processed[processed["label"].isin(VALID_LABELS)]
    processed = processed.drop_duplicates(subset=["text", "label"])
    processed = processed[["original_text", "text", "label"]]

    if processed.empty:
        raise ValueError("No valid reviews remain after preprocessing.")

    return processed.reset_index(drop=True)


def save_preprocessed_reviews(
    reviews: pd.DataFrame,
    path: Path = PREPROCESSED_DATA_PATH,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    reviews.to_csv(path, index=False, encoding="utf-8")


def main() -> None:
    raw_reviews = load_raw_reviews()
    processed_reviews = preprocess_reviews(raw_reviews)
    save_preprocessed_reviews(processed_reviews)

    label_counts = processed_reviews["label"].value_counts().to_dict()
    print(f"Raw rows: {len(raw_reviews)}")
    print(f"Preprocessed rows: {len(processed_reviews)}")
    print(f"Label counts: {label_counts}")
    print(f"Saved to: {PREPROCESSED_DATA_PATH}")

if __name__ == "__main__":
    main()
