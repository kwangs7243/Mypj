# Next Session

## Current Direction

The model experiment direction starts from NSMC.

Raw files expected locally:

```text
backend/data/raw/ratings_train.txt
backend/data/raw/ratings_test.txt
```

These files are ignored by Git.

## Current Completed Flow

From backend root:

```bash
uv run python ml/experiments/convert_nsmc_dataset.py
uv run python ml/experiments/convert_nsmc_dataset.py --mode light --train-output data/splits/nsmc_light_train.csv --test-output data/splits/nsmc_light_test.csv
uv run python ml/experiments/compare_models.py
```

Current meaningful baseline:

```text
nsmc_light
TfidfVectorizer + MultinomialNB
accuracy: 0.8276
macro_f1: 0.8276
```

## Next Work

Recommended next step:

```text
Add Korean morphological tokenizer experiment.
```

Goal:

```text
NSMC korean_only text
-> morphological tokenizer
-> CountVectorizer / TfidfVectorizer
-> 4 classical ML models
-> compare against sklearn_default baseline
```

Keep reviews educational and file-by-file.
