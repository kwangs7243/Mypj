import argparse
import re
from collections.abc import Callable
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
RAW_DATA_PATH = DATA_DIR / "sample_reviews.csv"
PREPROCESSED_DATA_PATH = DATA_DIR / "preprocessed_reviews.csv"
VALID_LABELS = {"positive", "negative"}


def clean_korean_only_text(value: str) -> str:
    text = str(value).strip()
    text = re.sub(r"[^가-힣\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_light_text(value: str) -> str:
    text = str(value).strip()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_text(value: str) -> str:
    return clean_korean_only_text(value)


PREPROCESSORS: dict[str, Callable[[str], str]] = {
    "korean_only": clean_korean_only_text,
    "light": clean_light_text,
}


def load_raw_reviews(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Raw dataset not found: {path}")

    reviews = pd.read_csv(path)
    required_columns = {"text", "label"}
    missing_columns = required_columns - set(reviews.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    return reviews


def preprocess_reviews(
    reviews: pd.DataFrame,
    mode: str = "korean_only",
) -> pd.DataFrame:
    if mode not in PREPROCESSORS:
        raise ValueError(f"Unknown preprocessing mode: {mode}")

    clean_function = PREPROCESSORS[mode]
    processed = reviews.dropna(subset=["text", "label"]).copy()
    processed["original_text"] = processed["text"].astype(str)
    processed["text"] = processed["text"].apply(clean_function)
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Preprocess review dataset CSV files.")
    parser.add_argument("--input", type=Path, default=RAW_DATA_PATH)
    parser.add_argument("--output", type=Path, default=PREPROCESSED_DATA_PATH)
    parser.add_argument(
        "--mode",
        choices=sorted(PREPROCESSORS),
        default="korean_only",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    raw_reviews = load_raw_reviews(args.input)
    processed_reviews = preprocess_reviews(raw_reviews, mode=args.mode)
    save_preprocessed_reviews(processed_reviews, args.output)

    label_counts = processed_reviews["label"].value_counts().to_dict()
    print(f"Mode: {args.mode}")
    print(f"Raw rows: {len(raw_reviews)}")
    print(f"Preprocessed rows: {len(processed_reviews)}")
    print(f"Label counts: {label_counts}")
    print(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()
