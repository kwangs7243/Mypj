# Model Experiment Plan

## Purpose

This project now uses NSMC to compare Korean sentiment-analysis model behavior.

The goal is to compare preprocessing, tokenization, vectorization, and classical ML model choices in a controlled way.

## Korean Summary

이 프로젝트는 이제 NSMC를 사용해 한국어 감성분석 모델의 동작 차이를 비교한다.

목표는 전처리 방식, 토큰화 방식, 벡터화 방식, 전통 ML 모델 선택에 따라 결과가 어떻게 달라지는지 통제된 흐름으로 비교하는 것이다.

## Active Dataset

```text
dataset: NSMC
raw train: backend/data/raw/ratings_train.txt
raw test: backend/data/raw/ratings_test.txt
converted train/test: backend/data/splits/nsmc_*.csv
labels: negative, positive
```

## Experiment Principles

- Keep train/test data fixed when comparing models.
- Change one major variable at a time when possible.
- Save results in CSV reports so changes can be compared later.
- Keep web-service code separate from experiment code.
- Treat FastAPI/frontend as the demo layer, not the model research layer.
- Use `.py` scripts for reproducible execution pipelines.
- Use `.ipynb` notebooks for exploration, visualization, interpretation, and study notes.

## 실험 원칙

- 모델 비교 시 train/test 데이터를 고정한다.
- 가능하면 한 번에 하나의 주요 변수만 바꾼다.
- 결과를 CSV report로 저장해 나중에 비교할 수 있게 한다.
- 웹서비스 코드와 실험 코드를 분리한다.
- FastAPI/frontend는 데모 계층으로 보고, 모델 연구 계층은 별도로 둔다.
- 재실행 가능한 흐름은 `.py` 스크립트로 둔다.
- 탐색, 시각화, 해석, 학습 메모는 `.ipynb` 노트북으로 둔다.

## Current Baseline

Current baseline:

```text
dataset: nsmc_light
tokenizer: scikit-learn default tokenization
vectorizers: CountVectorizer, TfidfVectorizer
models: MultinomialNB, ComplementNB, LogisticRegression, LinearSVC
report: backend/ml/reports/model_comparison_nsmc_light.csv
```

Tracked summary:

```text
backend/ml/reports/tokenizer_comparison_nsmc.md
backend/ml/reports/model_selection_visual_report.md
```

Run from backend root:

```bash
uv run python ml/experiments/compare_models.py
```

## Latest NSMC Tokenizer Result

Current best results:

```text
sklearn_default best: TfidfVectorizer + MultinomialNB, accuracy 0.8276, macro_f1 0.8276
kiwi best: TfidfVectorizer + LogisticRegression, accuracy 0.8452, macro_f1 0.8452
sentencepiece best: TfidfVectorizer + LogisticRegression, accuracy 0.8507, macro_f1 0.8506
```

SentencePiece currently performs best on NSMC.

## 최신 NSMC 토크나이저 결과

현재 최고 결과:

```text
sklearn_default best: TfidfVectorizer + MultinomialNB, accuracy 0.8276, macro_f1 0.8276
kiwi best: TfidfVectorizer + LogisticRegression, accuracy 0.8452, macro_f1 0.8452
sentencepiece best: TfidfVectorizer + LogisticRegression, accuracy 0.8507, macro_f1 0.8506
```

현재 NSMC에서는 SentencePiece가 가장 좋은 결과를 냈다.

## Planned Experiment Axes

### 1. Vectorizer Comparison

- `CountVectorizer`
- `TfidfVectorizer`

### 2. Classical ML Model Comparison

- `MultinomialNB`
- `ComplementNB`
- `LogisticRegression`
- `LinearSVC`

### 3. Tokenization Comparison

- scikit-learn default tokenization baseline
- Korean morphological analyzer tokenizer
- SentencePiece tokenizer

Preprocessing should be selected by tokenizer family:

- `korean_only` for Korean morphological analyzer experiments.
- `light` for SentencePiece experiments and the current default baseline.

## Planned Folder Structure

```text
notebooks/
├─ README.md
├─ 01_dataset_inspection.ipynb
├─ 02_preprocessing_comparison.ipynb
├─ 03_model_result_analysis.ipynb
└─ 04_tokenizer_comparison.ipynb

backend/ml/
├─ preprocess.py
├─ train_model.py
├─ experiments/
│  ├─ README.md
│  ├─ convert_nsmc_dataset.py
│  └─ compare_models.py
├─ tokenizers/
│  ├─ README.md
│  └─ .gitkeep
└─ reports/
   ├─ README.md
   └─ .gitkeep
```

## Next Experiment Steps

1. Inspect tokenizer output examples in a notebook.
2. Compare SentencePiece vocabulary sizes.
3. Compare Kiwi full-token output against selected POS output.
4. Decide whether the service model should be updated from the original MultinomialNB baseline.
