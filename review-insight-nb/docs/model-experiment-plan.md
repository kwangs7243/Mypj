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
- Use `.py` scripts for reproducible execution pipelines and `.ipynb` notebooks for exploration, visualization, interpretation, and study notes.

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

Preprocessing should be selected by tokenizer family:

- `korean_only` for the current baseline and Korean morphological analyzer experiments.
- `light` for SentencePiece experiments, so English, numbers, punctuation, and noisy symbols remain available to the tokenizer.

토크나이저 종류에 따라 전처리 모드를 분리한다.

- 현재 baseline과 한국어 형태소 분석기 실험에는 `korean_only`를 사용한다.
- SentencePiece 실험에는 `light`를 사용해서 영어, 숫자, 문장부호, 노이즈 기호를 토크나이저가 볼 수 있게 둔다.

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
│  └─ .gitkeep
├─ tokenizers/
│  ├─ README.md
│  └─ .gitkeep
└─ reports/
   ├─ README.md
   └─ .gitkeep
```

Notebook topics are planned analysis spaces. They are not required to exist before the `.py` execution scripts are stable.

## Notebook Usage Rule

Use notebooks after a reproducible script has produced data or report files.

Recommended flow:

```text
.py script creates CSV/report output
-> .ipynb reads that output
-> notebook explains, visualizes, and compares results
```

Do not rely on hidden notebook cell execution order for the main project pipeline.

## 노트북 사용 규칙

재실행 가능한 데이터 생성, 전처리, split, 모델 비교 실행은 `.py` 스크립트에 둔다.

노트북은 `.py`가 만든 CSV나 report 파일을 읽어서 결과를 관찰하고, 그래프로 확인하고, 해석을 남기는 용도로 사용한다.

권장 흐름:

```text
.py 스크립트가 CSV/report 생성
-> .ipynb가 결과 파일 읽기
-> 노트북에서 시각화, 비교, 해석 정리
```

프로젝트의 핵심 실행 흐름을 노트북 셀 실행 순서에 의존하지 않는다.

## First Experiment Steps

1. Record the current baseline result.
2. Create a common evaluation result table format.
3. Create fixed train/test split CSV files from the processed 5k dataset.
4. Compare `CountVectorizer` and `TfidfVectorizer` with `MultinomialNB`.
5. Compare `MultinomialNB`, `ComplementNB`, `LogisticRegression`, and `LinearSVC`.
6. Add tokenizer experiments only after the baseline comparison code is stable.
7. Add SentencePiece after the simple tokenizer and model comparison flow is understood.

## First Experiment Steps Korean Summary

1. 현재 baseline 결과를 기록한다.
2. 공통 평가 결과표 형식을 만든다.
3. 전처리된 5k 데이터셋에서 고정 train/test split CSV 파일을 만든다.
4. `MultinomialNB` 기준으로 `CountVectorizer`와 `TfidfVectorizer`를 비교한다.
5. `MultinomialNB`, `ComplementNB`, `LogisticRegression`, `LinearSVC`를 비교한다.
6. baseline 비교 코드가 안정화된 뒤 토큰화 실험을 추가한다.
7. 단순 토큰화/모델 비교 흐름을 이해한 뒤 SentencePiece 실험을 추가한다.

## Result Table Draft

```text
experiment_id, dataset, preprocessing, tokenizer, vectorizer, model, accuracy, macro_f1, weighted_f1, memo
baseline_001, sample_reviews, korean_only, default, tfidf, MultinomialNB, 0.4000, 0.2900, 0.2300, tiny sample dataset
```

## First Comparison Scope

The first model comparison script uses:

```text
dataset: korean_only_5k fixed train/test split
tokenizer: scikit-learn default tokenization
vectorizers: CountVectorizer, TfidfVectorizer
models: MultinomialNB, ComplementNB, LogisticRegression, LinearSVC
report: backend/ml/reports/model_comparison_5k.csv
```

This is a baseline for validating the comparison code. It is not the final Korean tokenization experiment.

Later tokenizer-focused comparisons should replace `sklearn_default` with:

```text
morphological tokenizer
SentencePiece tokenizer
```

The vectorizer/model comparison structure should remain reusable.

## Synthetic Dataset Limitation

The generated 5k dataset currently reaches 100% test accuracy across all baseline vectorizer/model combinations.

This means the dataset is useful for checking whether the pipeline works, but it is not useful for measuring real model differences.

Next comparison should use NSMC:

```text
source: https://github.com/e9t/nsmc
train: ratings_train.txt
test: ratings_test.txt
schema conversion: document,label -> text,label
```

The model comparison script should be reused with NSMC train/test files after conversion.

## Synthetic 데이터셋 한계

현재 generated 5k 데이터셋은 모든 baseline vectorizer/model 조합에서 test accuracy 100%가 나온다.

따라서 이 데이터셋은 파이프라인 검증용으로는 유용하지만, 실제 모델 차이를 측정하기에는 적합하지 않다.

다음 비교는 NSMC로 진행한다.

```text
출처: https://github.com/e9t/nsmc
train: ratings_train.txt
test: ratings_test.txt
스키마 변환: document,label -> text,label
```

NSMC 변환 후 기존 model comparison 구조를 재사용한다.
