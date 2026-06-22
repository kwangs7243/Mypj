# Splits

Saved train/test split files or split metadata will live here.

Keeping split information stable helps compare models fairly.

Planned examples:

```text
sample_5k_split_seed42.json
sample_20k_split_seed42.json
```

Current first experiment outputs:

```text
korean_only_5k_train.csv
korean_only_5k_test.csv
light_clean_5k_train.csv
light_clean_5k_test.csv
```

Run from the backend root:

```bash
uv run python ml/experiments/split_dataset.py
```

The default command splits `data/processed/korean_only_5k.csv` into train/test CSV files with `test_size=0.2` and `seed=42`.

For another processed dataset, pass explicit paths:

```bash
uv run python ml/experiments/split_dataset.py --input data/processed/light_clean_5k.csv --train-output data/splits/light_clean_5k_train.csv --test-output data/splits/light_clean_5k_test.csv
```
