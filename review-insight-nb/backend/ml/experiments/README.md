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
