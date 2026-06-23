# Reports

Experiment result tables and reproducible evaluation summaries live here.

Current baseline reports:

```text
model_comparison_nsmc_korean_only.csv
model_comparison_nsmc_light.csv
```

Generate the current default report from the backend root:

```bash
uv run python ml/experiments/compare_models.py
```

Report CSV files are ignored by Git because they are reproducible experiment outputs.

Latest observed NSMC baseline summary:

```text
nsmc_korean_only best: TfidfVectorizer + ComplementNB, accuracy 0.8180, macro_f1 0.8180
nsmc_light best: TfidfVectorizer + MultinomialNB, accuracy 0.8276, macro_f1 0.8276
```

These scores use scikit-learn's default tokenization and should be treated as a baseline before Korean morphological tokenization and SentencePiece comparisons.
