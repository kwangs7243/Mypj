# Model Experiment Plan

## Purpose

After the first web-service MVP, this project will also work as a small sentiment-analysis model experiment project.

The goal is not only to use one Naive Bayes model, but to compare preprocessing, tokenization, vectorization, and model choices in a controlled way.

## Korean Summary

1차 웹서비스 MVP 이후에는 이 프로젝트를 감성분석 모델 실험용 미니프로젝트로 확장한다.

목표는 Naive Bayes 모델 하나만 사용하는 것이 아니라, 전처리 방식, 토큰화 방식, 벡터화 방식, 모델 선택에 따라 결과가 어떻게 달라지는지 통제된 기준으로 비교하는 것이다.

## Baseline

The current baseline is:

```text
dataset: backend/data/preprocessed_reviews.csv
preprocessing: Korean-only text cleaning
tokenization: default TfidfVectorizer tokenization
vectorizer: TfidfVectorizer
model: MultinomialNB
train/test split: test_size=0.25, random_state=42, stratify=label
```

Latest baseline output:

```text
Train rows: 15
Test rows: 5
Accuracy: 0.4000
```

This score is not meaningful as a final performance signal because the dataset is intentionally tiny. For now, it only proves the pipeline works end to end.

## Baseline Korean Summary

현재 기준 모델은 다음과 같다.

```text
데이터셋: backend/data/preprocessed_reviews.csv
전처리: 한글 전용 텍스트 정제
토큰화: TfidfVectorizer 기본 토큰화
벡터화: TfidfVectorizer
모델: MultinomialNB
데이터 분리: test_size=0.25, random_state=42, stratify=label
```

현재 점수는 데이터가 너무 작기 때문에 최종 성능 지표로 해석하지 않는다. 지금은 파이프라인이 끝까지 동작한다는 기준점으로만 사용한다.

## Experiment Principles

- Keep the dataset split fixed when comparing models.
- Change one major variable at a time when possible.
- Save results in a table so changes can be compared later.
- Keep web-service code separate from experiment code.
- Treat the current FastAPI/frontend MVP as a working demo, not as the model research layer.
- Separate generated/synthetic data from real external datasets.
- Do not treat synthetic dataset scores as proof of real-world generalization.

## 실험 원칙

- 모델을 비교할 때는 가능한 한 같은 데이터 분리 기준을 사용한다.
- 가능하면 한 번에 하나의 주요 변수만 바꾼다.
- 결과는 표 형태로 저장해 나중에 비교할 수 있게 한다.
- 웹서비스 코드와 실험 코드는 분리한다.
- 현재 FastAPI/frontend MVP는 동작 데모로 유지하고, 모델 연구 계층은 별도로 다룬다.
- 생성/synthetic 데이터와 실제 외부 데이터셋을 분리한다.
- synthetic 데이터 점수를 실제 일반화 성능의 증거로 해석하지 않는다.

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

- default whitespace-like vectorizer tokenization
- Korean morphological analyzer tokenizer
- SentencePiece tokenizer

### 4. Dataset Improvement

- replace the tiny sample dataset with a larger Korean review dataset
- create a controlled generated dataset for experiment-code validation
- keep the dataset schema stable: `text`, `label`
- document dataset source and preprocessing decisions

See also:

```text
docs/dataset-plan.md
```

## Planned Folder Structure

```text
backend/ml/
├─ preprocess.py
├─ train_model.py
├─ experiments/
│  ├─ README.md
│  └─ .gitkeep
├─ tokenizers/
│  ├─ README.md
│  └─ .gitkeep
└─ reports/
   ├─ README.md
   └─ .gitkeep
```

## First Experiment Steps

1. Record the current baseline result.
2. Create a common evaluation result table format.
3. Compare `CountVectorizer` and `TfidfVectorizer` with `MultinomialNB`.
4. Compare `MultinomialNB`, `ComplementNB`, `LogisticRegression`, and `LinearSVC`.
5. Add tokenizer experiments only after the baseline comparison code is stable.
6. Add SentencePiece after the simple tokenizer and model comparison flow is understood.

## First Experiment Steps Korean Summary

1. 현재 baseline 결과를 기록한다.
2. 공통 평가 결과표 형식을 만든다.
3. `MultinomialNB` 기준으로 `CountVectorizer`와 `TfidfVectorizer`를 비교한다.
4. `MultinomialNB`, `ComplementNB`, `LogisticRegression`, `LinearSVC`를 비교한다.
5. baseline 비교 코드가 안정화된 뒤 토큰화 실험을 추가한다.
6. 단순 토큰화/모델 비교 흐름을 이해한 뒤 SentencePiece 실험을 추가한다.

## Result Table Draft

```text
experiment_id, dataset, preprocessing, tokenizer, vectorizer, model, accuracy, macro_f1, weighted_f1, memo
baseline_001, sample_reviews, korean_only, default, tfidf, MultinomialNB, 0.4000, 0.2900, 0.2300, tiny sample dataset
```
