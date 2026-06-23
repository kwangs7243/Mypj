# NSMC 토크나이저 비교 결과

## 범위

이 문서는 NSMC 데이터셋 기준의 토크나이저 비교 결과를 기록한다.

현재 비교한 토크나이저:

```text
sklearn_default
kiwi
sentencepiece
```

모든 결과는 같은 전통 ML 비교 구조를 사용한다.

```text
tokenizer -> CountVectorizer / TfidfVectorizer -> 4개 ML 모델 -> test 성능 평가
```

## 데이터셋 변형

`nsmc_light`

- 입력 원본: NSMC `ratings_train.txt`, `ratings_test.txt`
- 전처리 규칙: 공백만 정리하고 영어, 숫자, 문장부호, 기호를 보존
- 사용 토크나이저: `sklearn_default`, `sentencepiece`
- train rows: 149,995
- test rows: 49,997

`nsmc_korean_only`

- 입력 원본: NSMC `ratings_train.txt`, `ratings_test.txt`
- 전처리 규칙: 한글과 공백만 유지
- 사용 토크나이저: `kiwi`
- train rows: 148,385
- test rows: 49,430

## 토크나이저별 최고 결과

| 토크나이저 | 데이터셋 | 벡터화 | 모델 | Accuracy | Macro F1 |
|---|---|---|---|---:|---:|
| sentencepiece | nsmc_light | tfidf | logistic_regression | 0.8507 | 0.8506 |
| kiwi | nsmc_korean_only | tfidf | logistic_regression | 0.8452 | 0.8452 |
| sklearn_default | nsmc_light | tfidf | multinomial_nb | 0.8276 | 0.8276 |

## 핵심 해석

현재 결과에서는 `sentencepiece`가 가장 높은 성능을 냈다.

`sentencepiece`는 문장을 subword 단위로 쪼개기 때문에 띄어쓰기 품질이나 미등록 단어 문제에 상대적으로 강하다. NSMC처럼 짧은 리뷰, 오타, 신조어, 영어, 숫자, 기호가 섞인 데이터에서는 이 장점이 성능으로 이어진 것으로 볼 수 있다.

`kiwi` 형태소 분석기도 `sklearn_default`보다 좋은 결과를 냈다.

이는 한국어 문장을 어절 그대로 보는 것보다 형태소 단위로 분해하는 것이 감성 분류에 더 유리할 수 있음을 보여준다.

`sklearn_default`는 한국어 전용 토크나이저가 아니므로 기준선으로만 해석한다.

## 토크나이저별 상세 결과

### sklearn_default

데이터셋: `nsmc_light`

| 벡터화 | 모델 | Accuracy | Macro F1 | Weighted F1 |
|---|---|---:|---:|---:|
| tfidf | multinomial_nb | 0.8276 | 0.8276 | 0.8276 |
| tfidf | complement_nb | 0.8275 | 0.8275 | 0.8275 |
| count | multinomial_nb | 0.8258 | 0.8258 | 0.8258 |
| count | complement_nb | 0.8257 | 0.8257 | 0.8257 |
| tfidf | linear_svc | 0.8161 | 0.8160 | 0.8160 |
| count | logistic_regression | 0.8146 | 0.8145 | 0.8145 |
| tfidf | logistic_regression | 0.8127 | 0.8126 | 0.8126 |
| count | linear_svc | 0.8067 | 0.8067 | 0.8066 |

### kiwi

데이터셋: `nsmc_korean_only`

| 벡터화 | 모델 | Accuracy | Macro F1 | Weighted F1 |
|---|---|---:|---:|---:|
| tfidf | logistic_regression | 0.8452 | 0.8452 | 0.8452 |
| count | logistic_regression | 0.8433 | 0.8433 | 0.8433 |
| tfidf | linear_svc | 0.8403 | 0.8403 | 0.8403 |
| tfidf | complement_nb | 0.8359 | 0.8359 | 0.8359 |
| tfidf | multinomial_nb | 0.8359 | 0.8359 | 0.8358 |
| count | linear_svc | 0.8324 | 0.8324 | 0.8324 |
| count | complement_nb | 0.8317 | 0.8317 | 0.8317 |
| count | multinomial_nb | 0.8317 | 0.8316 | 0.8316 |

### sentencepiece

데이터셋: `nsmc_light`

| 벡터화 | 모델 | Accuracy | Macro F1 | Weighted F1 |
|---|---|---:|---:|---:|
| tfidf | logistic_regression | 0.8507 | 0.8506 | 0.8506 |
| tfidf | linear_svc | 0.8486 | 0.8486 | 0.8486 |
| count | logistic_regression | 0.8471 | 0.8471 | 0.8471 |
| tfidf | complement_nb | 0.8455 | 0.8455 | 0.8455 |
| tfidf | multinomial_nb | 0.8454 | 0.8454 | 0.8454 |
| count | linear_svc | 0.8438 | 0.8438 | 0.8438 |
| count | complement_nb | 0.8426 | 0.8426 | 0.8426 |
| count | multinomial_nb | 0.8426 | 0.8425 | 0.8425 |

## 모델 순위 변화

`sklearn_default`에서는 Naive Bayes 계열이 가장 좋은 결과를 냈다.

하지만 `kiwi`와 `sentencepiece`에서는 `LogisticRegression`이 가장 좋은 결과를 냈다.

이는 토큰화 방식이 바뀌면 같은 모델이라도 입력 벡터의 의미가 바뀌고, 그 결과 모델별 유리함도 달라진다는 것을 보여준다.

## 다음 작업

다음에는 다음 내용을 확인하면 좋다.

- SentencePiece vocabulary size 변경
- Kiwi에서 전체 형태소를 쓸지, 명사/동사/형용사 중심으로 제한할지 비교
- 토크나이저별 예시 문장 분해 결과를 노트북으로 시각화
- 최종 서비스 모델을 어떤 조합으로 갱신할지 결정

## 용어 메모

`Accuracy`

- 전체 test 데이터 중 정답을 맞힌 비율이다.

`Macro F1`

- 각 라벨의 F1 점수를 같은 비중으로 평균낸 값이다.
- positive와 negative를 균등하게 평가하고 싶을 때 중요하다.

`Weighted F1`

- 각 라벨의 데이터 개수를 반영해 F1 점수를 평균낸 값이다.
- 라벨 불균형이 있을 때 전체 데이터 분포를 반영한다.
