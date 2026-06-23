import argparse
import sys
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ml.preprocess import clean_korean_only_text, clean_light_text

DEFAULT_TRAIN_INPUT_PATH = BASE_DIR / "data" / "raw" / "ratings_train.txt"
DEFAULT_TEST_INPUT_PATH = BASE_DIR / "data" / "raw" / "ratings_test.txt"
DEFAULT_TRAIN_OUTPUT_PATH = BASE_DIR / "data" / "splits" / "nsmc_korean_only_train.csv"
DEFAULT_TEST_OUTPUT_PATH = BASE_DIR / "data" / "splits" / "nsmc_korean_only_test.csv"
LABEL_MAP = {
    0: "negative",
    1: "positive",
}
REQUIRED_COLUMNS = {"document", "label"}
PREPROCESSORS = {
    "korean_only": clean_korean_only_text,
    "light": clean_light_text,
}


def load_nsmc(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"NSMC source file not found: {path}")

    data = pd.read_csv(path, sep="\t")
    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    return data


def convert_nsmc(data: pd.DataFrame, mode: str) -> pd.DataFrame:
    if mode not in PREPROCESSORS:
        raise ValueError(f"Unknown preprocessing mode: {mode}")

    clean_function = PREPROCESSORS[mode]
    converted = data.dropna(subset=["document", "label"]).copy()
    converted["original_text"] = converted["document"].astype(str)
    converted["text"] = converted["document"].apply(clean_function)
    converted["label"] = pd.to_numeric(converted["label"], errors="coerce").map(
        LABEL_MAP
    )
    converted = converted.dropna(subset=["label"])
    converted = converted[converted["text"] != ""]
    converted = converted[["original_text", "text", "label"]]

    if converted.empty:
        raise ValueError("No valid NSMC rows remain after conversion.")

    return converted.reset_index(drop=True)


def save_dataset(data: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data.to_csv(path, index=False, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert NSMC ratings_train/test files to project CSV format."
    )
    parser.add_argument("--train-input", type=Path, default=DEFAULT_TRAIN_INPUT_PATH)
    parser.add_argument("--test-input", type=Path, default=DEFAULT_TEST_INPUT_PATH)
    parser.add_argument("--train-output", type=Path, default=DEFAULT_TRAIN_OUTPUT_PATH)
    parser.add_argument("--test-output", type=Path, default=DEFAULT_TEST_OUTPUT_PATH)
    parser.add_argument(
        "--mode",
        choices=sorted(PREPROCESSORS),
        default="korean_only",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    train_data = convert_nsmc(load_nsmc(args.train_input), mode=args.mode)
    test_data = convert_nsmc(load_nsmc(args.test_input), mode=args.mode)

    save_dataset(train_data, args.train_output)
    save_dataset(test_data, args.test_output)

    print(f"Mode: {args.mode}")
    print(f"Train rows: {len(train_data)}")
    print(f"Train label counts: {train_data['label'].value_counts().to_dict()}")
    print(f"Test rows: {len(test_data)}")
    print(f"Test label counts: {test_data['label'].value_counts().to_dict()}")
    print(f"Saved train dataset to: {args.train_output}")
    print(f"Saved test dataset to: {args.test_output}")


if __name__ == "__main__":
    main()
