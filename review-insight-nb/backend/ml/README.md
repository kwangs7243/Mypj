# Machine Learning

Model training, preprocessing, and evaluation scripts live here.

Planned files:

- `preprocess.py`
- `train_model.py`
- `evaluate.py`

Planned experiment folders:

- `experiments/`
- `tokenizers/`
- `reports/`

## Preprocessing

Run from the backend root:

```bash
uv run python ml/preprocess.py
```

Input:

```text
data/sample_reviews.csv
```

Output:

```text
data/preprocessed_reviews.csv
```

Current rule:

- Keep only Korean characters and whitespace.
- Remove English letters, numbers, punctuation, emojis, and other symbols.
- Add Korean tokenization later only if the first model needs it.

## Training

Run from the backend root:

```bash
uv run python ml/train_model.py
```

Input:

```text
data/preprocessed_reviews.csv
```

Output:

```text
models/sentiment_model.joblib
models/vectorizer.joblib
```

## Experiments

The first web-service MVP uses one baseline model. Later model analysis work should live under:

```text
ml/experiments/
ml/tokenizers/
ml/reports/
```

See:

```text
docs/model-experiment-plan.md
docs/dataset-plan.md
```

