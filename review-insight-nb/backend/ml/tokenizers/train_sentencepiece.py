import argparse
from pathlib import Path

import pandas as pd
import sentencepiece as spm


BASE_DIR = Path(__file__).resolve().parents[2]
DEFAULT_INPUT_PATH = BASE_DIR / "data" / "splits" / "nsmc_light_train.csv"
DEFAULT_TEXT_PATH = BASE_DIR / "ml" / "tokenizers" / "nsmc_sentencepiece_train.txt"
DEFAULT_MODEL_PREFIX = BASE_DIR / "ml" / "tokenizers" / "nsmc_sentencepiece"
DEFAULT_VOCAB_SIZE = 8000
REQUIRED_COLUMNS = {"text"}


def load_texts(path: Path) -> pd.Series:
    if not path.exists():
        raise FileNotFoundError(f"Training dataset not found: {path}")

    data = pd.read_csv(path)
    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    texts = data["text"].dropna().astype(str).str.strip()
    texts = texts[texts != ""]

    if texts.empty:
        raise ValueError("No valid text rows found for SentencePiece training.")

    return texts


def save_training_text(texts: pd.Series, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    texts.to_csv(path, index=False, header=False, encoding="utf-8")


def train_sentencepiece(
    input_path: Path,
    model_prefix: Path,
    vocab_size: int,
) -> None:
    model_prefix.parent.mkdir(parents=True, exist_ok=True)
    spm.SentencePieceTrainer.train(
        input=str(input_path),
        model_prefix=str(model_prefix),
        vocab_size=vocab_size,
        character_coverage=0.9995,
        model_type="unigram",
        bos_id=-1,
        eos_id=-1,
        pad_id=0,
        unk_id=1,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train a SentencePiece tokenizer from an NSMC split CSV."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT_PATH)
    parser.add_argument("--text-output", type=Path, default=DEFAULT_TEXT_PATH)
    parser.add_argument("--model-prefix", type=Path, default=DEFAULT_MODEL_PREFIX)
    parser.add_argument("--vocab-size", type=int, default=DEFAULT_VOCAB_SIZE)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    texts = load_texts(args.input)
    save_training_text(texts, args.text_output)
    train_sentencepiece(
        input_path=args.text_output,
        model_prefix=args.model_prefix,
        vocab_size=args.vocab_size,
    )

    print(f"Input rows: {len(texts)}")
    print(f"Training text saved to: {args.text_output}")
    print(f"SentencePiece model saved to: {args.model_prefix}.model")
    print(f"SentencePiece vocab saved to: {args.model_prefix}.vocab")


if __name__ == "__main__":
    main()
