# Reports

실험 결과표와 평가 요약 문서를 보관하는 폴더다.

## 현재 Baseline Report

```text
model_comparison_nsmc_korean_only.csv
model_comparison_nsmc_light.csv
model_comparison_nsmc_kiwi.csv
model_comparison_nsmc_sentencepiece.csv
tokenizer_comparison_nsmc.md
model_selection_visual_report.md
```

현재 기본 report 생성 명령:

```bash
uv run python ml/experiments/compare_models.py
```

CSV report 파일은 재생성 가능한 실험 산출물이므로 Git에서 무시한다.

실험 결과를 설명하는 Markdown 요약 문서는 사람이 읽는 결과 정리이므로 커밋할 수 있다.

현재 CSV report는 다음 지표를 train/test/gap 기준으로 남긴다.

```text
accuracy
macro_precision
macro_recall
macro_f1
weighted_f1
roc_auc
```

## 최신 NSMC 토크나이저 비교 요약

```text
sklearn_default best: TfidfVectorizer + MultinomialNB, accuracy 0.8276, macro_f1 0.8276
kiwi best: TfidfVectorizer + LogisticRegression, accuracy 0.8452, macro_f1 0.8452
sentencepiece best: TfidfVectorizer + LogisticRegression, accuracy 0.8507, macro_f1 0.8506
```

토크나이저별 수치 결과는 `tokenizer_comparison_nsmc.md`에 기록한다.

그래프 기반 선택 과정과 모델별 해석은 `model_selection_visual_report.md`에 기록한다.
