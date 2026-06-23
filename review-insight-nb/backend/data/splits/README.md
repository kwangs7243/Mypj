# Splits

Fixed train/test CSV files live here.

Current NSMC outputs:

```text
nsmc_korean_only_train.csv
nsmc_korean_only_test.csv
nsmc_light_train.csv
nsmc_light_test.csv
```

NSMC already provides `ratings_train.txt` and `ratings_test.txt`, so these files are converted from the original train/test split instead of being randomly split inside this project.

Run from the backend root:

```bash
uv run python ml/experiments/convert_nsmc_dataset.py
uv run python ml/experiments/convert_nsmc_dataset.py --mode light --train-output data/splits/nsmc_light_train.csv --test-output data/splits/nsmc_light_test.csv
```

Large split CSV files are ignored by Git.
