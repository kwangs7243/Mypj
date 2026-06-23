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

Run from backend root:

```bash
uv run python ml/experiments/compare_models.py
```

## Latest NSMC Baseline Result

Using scikit-learn default tokenization:

```text
nsmc_korean_only
best: TfidfVectorizer + ComplementNB
accuracy: 0.8180
macro_f1: 0.8180

nsmc_light
best: TfidfVectorizer + MultinomialNB
accuracy: 0.8276
macro_f1: 0.8276
```

This confirms that NSMC is useful enough for meaningful model comparison.

The result also suggests that preserving English letters, numbers, punctuation, and symbols through `light` preprocessing helps slightly even with the current scikit-learn default tokenizer.

## 최신 NSMC Baseline 결과

scikit-learn 기본 토큰화를 사용한 결과:

```text
nsmc_korean_only
best: TfidfVectorizer + ComplementNB
accuracy: 0.8180
macro_f1: 0.8180

nsmc_light
best: TfidfVectorizer + MultinomialNB
accuracy: 0.8276
macro_f1: 0.8276
```

이 결과는 NSMC가 의미 있는 모델 비교에 충분히 유용하다는 것을 보여준다.

또한 현재 scikit-learn 기본 토큰화에서도 영어, 숫자, 문장부호, 기호를 보존하는 `light` 전처리가 약간 더 좋은 결과를 낼 수 있음을 보여준다.

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

1. Keep NSMC baseline result as the first meaningful comparison.
2. Add Korean morphological tokenizer support.
3. Compare morphological tokenizer results against `sklearn_default`.
4. Add SentencePiece tokenizer support.
5. Compare SentencePiece results against morphological tokenizer and `sklearn_default`.
6. Use notebooks to inspect token examples and report differences.
