# Notebooks

This folder is for exploratory analysis, result interpretation, visualization, and study notes.

Notebook files should not become the main execution pipeline. Reproducible steps should be implemented in `.py` scripts first, then notebooks should read the CSV/report files and explain the results.

## Role Split

Use `.py` files for:

- dataset generation
- preprocessing
- fixed train/test splitting
- model comparison execution
- report CSV creation

Use `.ipynb` files for:

- inspecting datasets
- comparing preprocessing outputs
- visualizing label and text-length distributions
- reading model report CSV files
- interpreting model, vectorizer, and tokenizer differences
- keeping study notes for concepts that need explanation

## Korean Summary

이 폴더는 탐색 분석, 결과 해석, 시각화, 학습 메모를 위한 공간이다.

노트북이 메인 실행 파이프라인이 되면 안 된다. 재실행 가능해야 하는 과정은 먼저 `.py` 스크립트로 구현하고, 노트북은 생성된 CSV나 report 파일을 읽어서 결과를 분석하고 설명하는 역할로 사용한다.

`.py` 파일에 둘 것:

- 데이터셋 생성
- 전처리
- 고정 train/test 분할
- 모델 비교 실행
- report CSV 생성

`.ipynb` 파일에 둘 것:

- 데이터셋 관찰
- 전처리 결과 비교
- 라벨 분포와 문장 길이 분포 시각화
- 모델 report CSV 분석
- 모델, 벡터화 방식, 토크나이저 차이 해석
- 이해가 필요한 개념 학습 메모

## Planned Notebooks

```text
01_dataset_inspection.ipynb
02_preprocessing_comparison.ipynb
03_model_result_analysis.ipynb
04_tokenizer_comparison.ipynb
```

These files are planned topics, not required immediate implementation.

## Planned Notebook Purpose

`01_dataset_inspection.ipynb`

- Inspect NSMC and later real review datasets.
- Check label counts, duplicate rows, null values, and text length distribution.

`02_preprocessing_comparison.ipynb`

- Compare `korean_only` and `light` preprocessing outputs.
- Inspect examples where rows disappear after cleaning or duplicate removal.

`03_model_result_analysis.ipynb`

- Read `backend/ml/reports/*.csv`.
- Compare accuracy, macro F1, weighted F1, model type, and vectorizer type.

`04_tokenizer_comparison.ipynb`

- Compare default vectorizer tokenization, Korean morphological tokenization, and SentencePiece tokenization.
- Inspect how the same review is split differently by each tokenizer.
