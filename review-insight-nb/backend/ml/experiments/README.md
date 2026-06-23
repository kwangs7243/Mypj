# Experiments

Model comparison scripts live here.

Current scope:

- convert NSMC raw train/test files to the project `text,label` format
- compare vectorizers and classical ML classifiers
- later compare Korean morphological tokenization and SentencePiece tokenization

Keep these scripts independent from FastAPI routes and frontend code.

## Convert NSMC Dataset

Place these NSMC files under `data/raw/`:

```text
ratings_train.txt
ratings_test.txt
```

Run from the backend root:

```bash
uv run python ml/experiments/convert_nsmc_dataset.py
```

Default outputs:

```text
data/splits/nsmc_korean_only_train.csv
data/splits/nsmc_korean_only_test.csv
```

The converter maps:

```text
document -> text
0 -> negative
1 -> positive
```

For the current baseline comparison, use `light` mode:

```bash
uv run python ml/experiments/convert_nsmc_dataset.py --mode light --train-output data/splits/nsmc_light_train.csv --test-output data/splits/nsmc_light_test.csv
```

## Compare Models

Run from the backend root after converting NSMC:

```bash
uv run python ml/experiments/compare_models.py
```

Default inputs:

```text
data/splits/nsmc_light_train.csv
data/splits/nsmc_light_test.csv
```

Default output:

```text
ml/reports/model_comparison_nsmc_light.csv
```

The first comparison intentionally uses scikit-learn's default tokenization as a baseline only.
The target experiment direction is to replace the tokenizer later with Korean morphological tokenization and SentencePiece tokenization while keeping the same vectorizer/model comparison structure.

Tokenizer options:

```text
sklearn_default
kiwi
sentencepiece
```

The report records train/test metrics and their generalization gaps:

```text
accuracy
macro_precision
macro_recall
macro_f1
weighted_f1
roc_auc
```

For the current Korean sentiment comparison, `test_macro_f1` is the primary model selection metric.
`test_accuracy`, `test_roc_auc`, and train-test gaps are used as supporting evidence.
