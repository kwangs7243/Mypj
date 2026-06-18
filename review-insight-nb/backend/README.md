# Backend

FastAPI 서버와 머신러닝 모델 학습 코드를 관리합니다.

## Environment

이 백엔드는 `uv`를 기준으로 Python 가상환경과 패키지를 관리합니다.

```bash
cd review-insight-nb/backend
uv sync
```

개발 서버 실행:

```bash
uv run uvicorn app.main:app --reload
```

서버 실행 후 확인:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

## Current API

### Health Check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Predict Sentiment

현재는 모델 연결 전 더미 예측 로직입니다. 이후 학습된 Naive Bayes 모델을 연결합니다.

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
  "confidence": 0.75,
  "probabilities": {
    "positive": 0.75,
    "negative": 0.25
  }
}
```

## Structure

```text
app/
├─ main.py
├─ schemas.py
└─ services/
   └─ sentiment_service.py
```

## Responsibilities

- 리뷰 감성 예측 API 제공
- 요청/응답 DTO 관리
- 학습된 모델과 벡터라이저 로드
- 리뷰 텍스트 전처리
- 모델 학습 및 평가 스크립트 관리

