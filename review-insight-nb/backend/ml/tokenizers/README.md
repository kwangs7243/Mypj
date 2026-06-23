# Tokenizers

Tokenizer-specific helpers live here.

Implemented tokenizer options:

```text
sklearn_default
kiwi
sentencepiece
```

## Kiwi

`kiwi` uses `kiwipiepy` for Korean morphological tokenization.

Run model comparison with:

```bash
uv run python ml/experiments/compare_models.py --dataset-name nsmc_korean_only --train data/splits/nsmc_korean_only_train.csv --test data/splits/nsmc_korean_only_test.csv --tokenizer kiwi --output ml/reports/model_comparison_nsmc_kiwi.csv
```

## SentencePiece

Train SentencePiece first:

```bash
uv run python ml/tokenizers/train_sentencepiece.py
```

Then run model comparison:

```bash
uv run python ml/experiments/compare_models.py --dataset-name nsmc_light --tokenizer sentencepiece --output ml/reports/model_comparison_nsmc_sentencepiece.csv
```

SentencePiece `.model`, `.vocab`, and training text files are ignored by Git because they are reproducible artifacts.
