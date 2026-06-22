# Experiments

Model comparison scripts will live here.

Planned scope:

- baseline result recording
- controlled generated dataset creation
- vectorizer comparison
- classical ML model comparison
- later tokenizer comparison

Keep these scripts independent from FastAPI routes and frontend code.

## Generate Dataset

Run from the backend root:

```bash
uv run python ml/experiments/generate_review_dataset.py
```

Default output:

```text
data/generated/generated_reviews_5k.csv
```

The generated CSV is ignored by Git. Regenerate it after cloning or copy it from external storage.

## Split Dataset

Run from the backend root after preprocessing:

```bash
uv run python ml/experiments/split_dataset.py
```

Default input:

```text
data/processed/korean_only_5k.csv
```

Default outputs:

```text
data/splits/korean_only_5k_train.csv
data/splits/korean_only_5k_test.csv
```

The split script uses stratified train/test splitting so each label keeps a similar ratio in both files.
The output CSV files are ignored by Git. Regenerate them after cloning or copy them from external storage.

## Compare Models

Run from the backend root after creating split files:

```bash
uv run python ml/experiments/compare_models.py
```

Default inputs:

```text
data/splits/korean_only_5k_train.csv
data/splits/korean_only_5k_test.csv
```

Default output:

```text
ml/reports/model_comparison_5k.csv
```

Example for another fixed split:

```bash
uv run python ml/experiments/compare_models.py --dataset-name light_clean_5k --train data/splits/light_clean_5k_train.csv --test data/splits/light_clean_5k_test.csv --output ml/reports/model_comparison_light_5k.csv
```

This first comparison intentionally uses scikit-learn's default tokenization as a baseline only.
The target experiment direction is to replace the tokenizer later with Korean morphological tokenization and SentencePiece tokenization while keeping the same comparison structure.
