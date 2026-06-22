import argparse
from collections.abc import Callable
from pathlib import Path

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.naive_bayes import ComplementNB, MultinomialNB
from sklearn.svm import LinearSVC


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_TRAIN_PATH = BASE_DIR / "data" / "splits" / "korean_only_5k_train.csv"
DEFAULT_TEST_PATH = BASE_DIR / "data" / "splits" / "korean_only_5k_test.csv"
DEFAULT_REPORT_PATH = BASE_DIR / "ml" / "reports" / "model_comparison_5k.csv"
DEFAULT_DATASET_NAME = "korean_only_5k"
REQUIRED_COLUMNS = {"text", "label"}


def load_split(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Split dataset not found: {path}. "
            "Run `uv run python ml/experiments/split_dataset.py` first."
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
        raise ValueError(f"No valid rows found in split dataset: {path}")

    return data.reset_index(drop=True)


def build_vectorizers() -> dict[str, Callable[[], CountVectorizer | TfidfVectorizer]]:
    return {
        "count": CountVectorizer,
        "tfidf": TfidfVectorizer,
    }


def build_models() -> dict[str, Callable[[], object]]:
    return {
        "multinomial_nb": MultinomialNB,
        "complement_nb": ComplementNB,
        "logistic_regression": lambda: LogisticRegression(max_iter=1000),
        "linear_svc": lambda: LinearSVC(max_iter=5000),
    }


def evaluate_model(
    dataset_name: str,
    vectorizer_name: str,
    vectorizer: CountVectorizer | TfidfVectorizer,
    model_name: str,
    model: object,
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
) -> dict[str, object]:
    x_train = vectorizer.fit_transform(train_data["text"])
    x_test = vectorizer.transform(test_data["text"])
    y_train = train_data["label"]
    y_test = test_data["label"]

    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    return {
        "dataset": dataset_name,
        "tokenizer": "sklearn_default",
        "vectorizer": vectorizer_name,
        "model": model_name,
        "train_rows": len(train_data),
        "test_rows": len(test_data),
        "vocab_size": len(vectorizer.vocabulary_),
        "accuracy": accuracy_score(y_test, predictions),
        "macro_f1": f1_score(y_test, predictions, average="macro", zero_division=0),
        "weighted_f1": f1_score(
            y_test,
            predictions,
            average="weighted",
            zero_division=0,
        ),
    }


def compare_models(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    dataset_name: str,
) -> pd.DataFrame:
    results = []

    for vectorizer_name, build_vectorizer in build_vectorizers().items():
        for model_name, build_model in build_models().items():
            result = evaluate_model(
                dataset_name=dataset_name,
                vectorizer_name=vectorizer_name,
                vectorizer=build_vectorizer(),
                model_name=model_name,
                model=build_model(),
                train_data=train_data,
                test_data=test_data,
            )
            results.append(result)

    return pd.DataFrame(results).sort_values(
        by=["macro_f1", "accuracy"],
        ascending=False,
    )


def save_report(report: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    report.to_csv(path, index=False, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare baseline vectorizers and classical ML classifiers."
    )
    parser.add_argument("--train", type=Path, default=DEFAULT_TRAIN_PATH)
    parser.add_argument("--test", type=Path, default=DEFAULT_TEST_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT_PATH)
    parser.add_argument("--dataset-name", default=DEFAULT_DATASET_NAME)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    train_data = load_split(args.train)
    test_data = load_split(args.test)
    report = compare_models(
        train_data=train_data,
        test_data=test_data,
        dataset_name=args.dataset_name,
    )
    save_report(report, args.output)

    print(f"Train rows: {len(train_data)}")
    print(f"Test rows: {len(test_data)}")
    print(f"Saved report to: {args.output}")
    print(report.to_string(index=False))


if __name__ == "__main__":
    main()
