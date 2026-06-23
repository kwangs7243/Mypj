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

Default rule:

- Keep only Korean characters and whitespace.
- Remove English letters, numbers, punctuation, emojis, and other symbols.
- Add Korean tokenization later only if the first model needs it.

The preprocessing script now supports explicit modes:

```bash
uv run python ml/preprocess.py --mode korean_only
uv run python ml/preprocess.py --mode light
```

Mode meaning:

- `korean_only`: keep only Korean characters and whitespace. This matches the current service baseline and is useful before simple Korean-only vectorization or a Korean morphological analyzer.
- `light`: normalize spacing only and keep English, numbers, punctuation, and symbols. This is intended for later SentencePiece-style experiments where subword tokenization should see the original noisy text.

The active model-experiment dataset is NSMC. NSMC conversion lives in:

```text
ml/experiments/convert_nsmc_dataset.py
```

## Training

Run from the backend root:

```bash
uv run python ml/train_model.py
```

Input:

```text
data/splits/nsmc_light_train.csv
```

Output:

```text
models/sentencepiece.model
models/sentiment_model.joblib
models/vectorizer.joblib
```

The current service model follows the selected experiment result:

```text
SentencePiece -> TfidfVectorizer -> LogisticRegression
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

