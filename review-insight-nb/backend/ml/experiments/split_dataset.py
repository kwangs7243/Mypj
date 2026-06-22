import argparse
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_PATH = BASE_DIR / "data" / "processed" / "korean_only_5k.csv"
DEFAULT_TRAIN_OUTPUT_PATH = BASE_DIR / "data" / "splits" / "korean_only_5k_train.csv"
DEFAULT_TEST_OUTPUT_PATH = BASE_DIR / "data" / "splits" / "korean_only_5k_test.csv"
DEFAULT_TEST_SIZE = 0.2
DEFAULT_SEED = 42
REQUIRED_COLUMNS = {"text", "label"}


def load_dataset(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {path}. "
            "Run preprocessing before splitting the dataset."
        )

    data = pd.read_csv(path)
    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    data = data.dropna(subset=["text", "label"]).copy()
    data["text"] = data["text"].astype(str).str.strip()
    data["label"] = data["label"].astype(str).str.strip().str.lower()
    data = data[(data["text"] != "") & (data["label"] != "")]

    if data.empty:
        raise ValueError("No valid rows found for dataset splitting.")

    return data.reset_index(drop=True)


def split_dataset(
    data: pd.DataFrame,
    test_size: float,
    seed: int,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    if not 0 < test_size < 1:
        raise ValueError("test_size must be between 0 and 1.")

    label_counts = data["label"].value_counts()
    if len(label_counts) < 2:
        raise ValueError("At least two labels are required for stratified splitting.")

    rare_labels = label_counts[label_counts < 2]
    if not rare_labels.empty:
        raise ValueError(
            "Each label needs at least two rows for stratified splitting. "
            f"Rare labels: {rare_labels.to_dict()}"
        )

    train_data, test_data = train_test_split(
        data,
        test_size=test_size,
        random_state=seed,
        stratify=data["label"],
    )

    return train_data.reset_index(drop=True), test_data.reset_index(drop=True)


def save_split(data: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, index=False, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create fixed train/test CSV files from a processed review dataset."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--train-output", type=Path, default=DEFAULT_TRAIN_OUTPUT_PATH)
    parser.add_argument("--test-output", type=Path, default=DEFAULT_TEST_OUTPUT_PATH)
    parser.add_argument("--test-size", type=float, default=DEFAULT_TEST_SIZE)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data = load_dataset(args.input)
    train_data, test_data = split_dataset(
        data=data,
        test_size=args.test_size,
        seed=args.seed,
    )

    save_split(train_data, args.train_output)
    save_split(test_data, args.test_output)

    print(f"Input rows: {len(data)}")
    print(f"Train rows: {len(train_data)}")
    print(f"Test rows: {len(test_data)}")
    print(f"Seed: {args.seed}")
    print(f"Test size: {args.test_size}")
    print(f"Train label counts: {train_data['label'].value_counts().to_dict()}")
    print(f"Test label counts: {test_data['label'].value_counts().to_dict()}")
    print(f"Saved train split to: {args.train_output}")
    print(f"Saved test split to: {args.test_output}")


if __name__ == "__main__":
    main()
