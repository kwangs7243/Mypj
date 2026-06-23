# Dataset Plan

## Purpose

The project uses NSMC as the main Korean sentiment-analysis dataset for model comparison.

## Korean Summary

이 프로젝트는 NSMC를 주요 한국어 감성분석 모델 비교 데이터셋으로 사용한다.

## Dataset Source

Source:

```text
https://github.com/e9t/nsmc
```

Files placed under `backend/data/raw/`:

```text
ratings_train.txt
ratings_test.txt
```

NSMC schema:

```text
id, document, label
```

Label meaning:

```text
0: negative
1: positive
```

Original size:

```text
ratings_train.txt: 150,000 rows
ratings_test.txt: 50,000 rows
```

The files are tab-separated text files.

## Git Tracking Rule

Do not commit raw or converted NSMC data files.

Track only:

- README files
- conversion scripts
- experiment scripts
- instructions
- small sample files if intentionally added later

Ignored local files include:

```text
backend/data/raw/ratings_train.txt
backend/data/raw/ratings_test.txt
backend/data/splits/nsmc_korean_only_train.csv
backend/data/splits/nsmc_korean_only_test.csv
backend/data/splits/nsmc_light_train.csv
backend/data/splits/nsmc_light_test.csv
backend/ml/reports/*.csv
```

## Current Dataset Workflow

Run from the backend root.

### 1. Place Raw NSMC Files

```text
backend/data/raw/ratings_train.txt
backend/data/raw/ratings_test.txt
```

### 2. Convert Korean-Only Version

```bash
uv run python ml/experiments/convert_nsmc_dataset.py
```

Outputs:

```text
backend/data/splits/nsmc_korean_only_train.csv
backend/data/splits/nsmc_korean_only_test.csv
```

Rule:

```text
Keep Korean characters and whitespace only.
```

### 3. Convert Light Version

```bash
uv run python ml/experiments/convert_nsmc_dataset.py --mode light --train-output data/splits/nsmc_light_train.csv --test-output data/splits/nsmc_light_test.csv
```

Outputs:

```text
backend/data/splits/nsmc_light_train.csv
backend/data/splits/nsmc_light_test.csv
```

Rule:

```text
Normalize spacing only. Preserve English letters, numbers, punctuation, and symbols.
```

## Current Converted Data Status

Observed local conversion result:

```text
nsmc_korean_only_train.csv: 148,385 rows
nsmc_korean_only_test.csv: 49,430 rows
nsmc_light_train.csv: 149,995 rows
nsmc_light_test.csv: 49,997 rows
```

`korean_only` has fewer rows because non-Korean-only reviews can become empty after cleaning.

`light` keeps more rows because it preserves English letters, numbers, punctuation, and symbols.

## Next Data Work

Use NSMC first for:

- scikit-learn default tokenizer baseline
- Korean morphological tokenizer comparison
- SentencePiece tokenizer comparison

Later, if the project needs a closer match to commerce or local-business reviews, add a real review dataset with clear source and license.
