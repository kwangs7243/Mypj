import argparse
import sys
from collections.abc import Callable
from pathlib import Path

import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.naive_bayes import ComplementNB, MultinomialNB
from sklearn.svm import LinearSVC


BASE_DIR = Path(__file__).resolve().parents[2]
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from ml.tokenizers.text_tokenizers import KiwiTokenizer, SentencePieceTokenizer

DEFAULT_TRAIN_PATH = BASE_DIR / "data" / "splits" / "nsmc_light_train.csv"
DEFAULT_TEST_PATH = BASE_DIR / "data" / "splits" / "nsmc_light_test.csv"
DEFAULT_REPORT_PATH = BASE_DIR / "ml" / "reports" / "model_comparison_nsmc_light.csv"
DEFAULT_DATASET_NAME = "nsmc_light"
DEFAULT_TOKENIZER = "sklearn_default"
DEFAULT_SENTENCEPIECE_MODEL_PATH = (
    BASE_DIR / "ml" / "tokenizers" / "nsmc_sentencepiece.model"
)
REQUIRED_COLUMNS = {"text", "label"}
POSITIVE_LABEL = "positive"


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


def build_tokenizer(
    tokenizer_name: str,
    sentencepiece_model_path: Path,
) -> Callable[[str], list[str]] | None:
    if tokenizer_name == "sklearn_default":
        return None
    if tokenizer_name == "kiwi":
        return KiwiTokenizer()
    if tokenizer_name == "sentencepiece":
        return SentencePieceTokenizer(sentencepiece_model_path)

    raise ValueError(f"Unknown tokenizer: {tokenizer_name}")


def build_vectorizers(
    tokenizer: Callable[[str], list[str]] | None,
) -> dict[str, Callable[[], CountVectorizer | TfidfVectorizer]]:
    vectorizer_options = {}

    if tokenizer is not None:
        vectorizer_options["tokenizer"] = tokenizer
        vectorizer_options["token_pattern"] = None
        vectorizer_options["lowercase"] = False

    return {
        "count": lambda: CountVectorizer(**vectorizer_options),
        "tfidf": lambda: TfidfVectorizer(**vectorizer_options),
    }


def build_models() -> dict[str, Callable[[], object]]:
    return {
        "multinomial_nb": MultinomialNB,
        "complement_nb": ComplementNB,
        "logistic_regression": lambda: LogisticRegression(max_iter=1000),
        "linear_svc": lambda: LinearSVC(max_iter=5000),
    }


def get_positive_scores(model: object, x_data) -> list[float] | None:
    if hasattr(model, "predict_proba"):
        positive_class_index = list(model.classes_).index(POSITIVE_LABEL)
        return model.predict_proba(x_data)[:, positive_class_index]

    if hasattr(model, "decision_function"):
        return model.decision_function(x_data)

    return None


def calculate_metrics(y_true: pd.Series, y_pred: pd.Series, y_score) -> dict[str, float]:
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "macro_precision": precision_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
        "macro_recall": recall_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
        "macro_f1": f1_score(
            y_true,
            y_pred,
            average="macro",
            zero_division=0,
        ),
        "weighted_f1": f1_score(
            y_true,
            y_pred,
            average="weighted",
            zero_division=0,
        ),
    }

    if y_score is None:
        metrics["roc_auc"] = None
    else:
        y_binary = (y_true == POSITIVE_LABEL).astype(int)
        metrics["roc_auc"] = roc_auc_score(y_binary, y_score)

    return metrics


def evaluate_model(
    dataset_name: str,
    tokenizer_name: str,
    vectorizer_name: str,
    model_name: str,
    model: object,
    x_train,
    x_test,
    y_train: pd.Series,
    y_test: pd.Series,
    train_rows: int,
    test_rows: int,
    vocab_size: int,
) -> dict[str, object]:
    model.fit(x_train, y_train)
    train_predictions = model.predict(x_train)
    test_predictions = model.predict(x_test)
    train_scores = get_positive_scores(model, x_train)
    test_scores = get_positive_scores(model, x_test)
    train_metrics = calculate_metrics(y_train, train_predictions, train_scores)
    test_metrics = calculate_metrics(y_test, test_predictions, test_scores)

    return {
        "dataset": dataset_name,
        "tokenizer": tokenizer_name,
        "vectorizer": vectorizer_name,
        "model": model_name,
        "train_rows": train_rows,
        "test_rows": test_rows,
        "vocab_size": vocab_size,
        "train_accuracy": train_metrics["accuracy"],
        "train_macro_precision": train_metrics["macro_precision"],
        "train_macro_recall": train_metrics["macro_recall"],
        "train_macro_f1": train_metrics["macro_f1"],
        "train_weighted_f1": train_metrics["weighted_f1"],
        "train_roc_auc": train_metrics["roc_auc"],
        "test_accuracy": test_metrics["accuracy"],
        "test_macro_precision": test_metrics["macro_precision"],
        "test_macro_recall": test_metrics["macro_recall"],
        "test_macro_f1": test_metrics["macro_f1"],
        "test_weighted_f1": test_metrics["weighted_f1"],
        "test_roc_auc": test_metrics["roc_auc"],
        "generalization_gap_accuracy": (
            train_metrics["accuracy"] - test_metrics["accuracy"]
        ),
        "generalization_gap_macro_precision": (
            train_metrics["macro_precision"] - test_metrics["macro_precision"]
        ),
        "generalization_gap_macro_recall": (
            train_metrics["macro_recall"] - test_metrics["macro_recall"]
        ),
        "generalization_gap_macro_f1": (
            train_metrics["macro_f1"] - test_metrics["macro_f1"]
        ),
        "generalization_gap_roc_auc": (
            train_metrics["roc_auc"] - test_metrics["roc_auc"]
        ),
        "accuracy": test_metrics["accuracy"],
        "macro_f1": test_metrics["macro_f1"],
        "weighted_f1": test_metrics["weighted_f1"],
    }


def compare_models(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    dataset_name: str,
    tokenizer_name: str,
    sentencepiece_model_path: Path,
) -> pd.DataFrame:
    results = []
    tokenizer = build_tokenizer(
        tokenizer_name=tokenizer_name,
        sentencepiece_model_path=sentencepiece_model_path,
    )
    y_train = train_data["label"]
    y_test = test_data["label"]

    for vectorizer_name, build_vectorizer in build_vectorizers(tokenizer).items():
        vectorizer = build_vectorizer()
        x_train = vectorizer.fit_transform(train_data["text"])
        x_test = vectorizer.transform(test_data["text"])
        vocab_size = len(vectorizer.vocabulary_)

        for model_name, build_model in build_models().items():
            result = evaluate_model(
                dataset_name=dataset_name,
                tokenizer_name=tokenizer_name,
                vectorizer_name=vectorizer_name,
                model_name=model_name,
                model=build_model(),
                x_train=x_train,
                x_test=x_test,
                y_train=y_train,
                y_test=y_test,
                train_rows=len(train_data),
                test_rows=len(test_data),
                vocab_size=vocab_size,
            )
            results.append(result)

    return pd.DataFrame(results).sort_values(
        by=["test_macro_f1", "test_accuracy"],
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
    parser.add_argument(
        "--tokenizer",
        choices=["sklearn_default", "kiwi", "sentencepiece"],
        default=DEFAULT_TOKENIZER,
    )
    parser.add_argument(
        "--sentencepiece-model",
        type=Path,
        default=DEFAULT_SENTENCEPIECE_MODEL_PATH,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    train_data = load_split(args.train)
    test_data = load_split(args.test)
    report = compare_models(
        train_data=train_data,
        test_data=test_data,
        dataset_name=args.dataset_name,
        tokenizer_name=args.tokenizer,
        sentencepiece_model_path=args.sentencepiece_model,
    )
    save_report(report, args.output)

    print(f"Train rows: {len(train_data)}")
    print(f"Test rows: {len(test_data)}")
    print(f"Tokenizer: {args.tokenizer}")
    print(f"Saved report to: {args.output}")
    print(report.to_string(index=False))


if __name__ == "__main__":
    main()
