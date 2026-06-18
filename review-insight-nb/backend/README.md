# Backend

FastAPI 서버와 머신러닝 모델 학습 코드를 관리합니다.

## Planned Responsibilities

- 리뷰 감성 예측 API 제공
- 학습된 모델과 벡터라이저 로드
- 리뷰 텍스트 전처리
- 모델 학습 및 평가 스크립트 관리

## Planned API

```http
POST /api/predict
```

Request:

```json
{
  "text": "배송이 빠르고 제품도 만족스러워요"
}
```

Response:

```json
{
  "label": "positive",
  "confidence": 0.87,
  "probabilities": {
    "positive": 0.87,
    "negative": 0.13
  }
}
```

