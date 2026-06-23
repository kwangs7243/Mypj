from pathlib import Path

import sentencepiece as spm
from kiwipiepy import Kiwi


class KiwiTokenizer:
    def __init__(self) -> None:
        self._kiwi = Kiwi()

    def __call__(self, text: str) -> list[str]:
        return [
            token.form
            for token in self._kiwi.tokenize(str(text))
            if token.form.strip()
        ]


class SentencePieceTokenizer:
    def __init__(self, model_path: Path) -> None:
        if not model_path.exists():
            raise FileNotFoundError(
                f"SentencePiece model not found: {model_path}. "
                "Run `uv run python ml/tokenizers/train_sentencepiece.py` first."
            )

        self._processor = spm.SentencePieceProcessor()
        self._processor.load(str(model_path))

    def __call__(self, text: str) -> list[str]:
        return self._processor.encode(str(text), out_type=str)
