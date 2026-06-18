# Backend

FastAPI backend for the review sentiment analysis service.

## Environment

This backend uses `uv` for Python dependency and virtual environment management.

```bash
cd review-insight-nb/backend
uv sync
```

Run the development server:

```bash
uv run uvicorn app.main:app --reload
```

If you are in the repository root, run:

```bash
uv --directory review-insight-nb/backend run uvicorn app.main:app --reload
```

Check the API:

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

### Model Info

This endpoint is a placeholder until the real Naive Bayes model is trained and connected.

```http
GET /api/model-info
```

Response:

```json
{
  "model": "Multinomial Naive Bayes",
  "vectorizer": "TfidfVectorizer",
  "status": "not_trained",
  "trained": false
}
```

### Predict Sentiment

This endpoint currently uses temporary keyword-based dummy logic. It will later use the trained Naive Bayes model.

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
├─ model_loader.py
├─ schemas.py
└─ services/
   └─ sentiment_service.py
```

## File Roles

- `main.py`: FastAPI app object and API route definitions.
- `schemas.py`: Pydantic request and response DTOs.
- `model_loader.py`: Model status and future model-loading logic.
- `services/sentiment_service.py`: Sentiment prediction logic.

