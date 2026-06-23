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

This endpoint reports whether the saved service model artifacts are available.

```http
GET /api/model-info
```

Response:

```json
{
  "model": "Logistic Regression",
  "tokenizer": "SentencePiece",
  "vectorizer": "TfidfVectorizer",
  "preprocessing": "light",
  "status": "trained",
  "trained": true
}
```

### Predict Sentiment

This endpoint uses the saved `SentencePiece`, `TfidfVectorizer`, and `LogisticRegression` artifacts.

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
- `model_loader.py`: Saved model/vectorizer loading and model status.
- `services/sentiment_service.py`: Real sentiment prediction with the loaded model.

## Data Preprocessing

Run from the backend root:

```bash
uv run python ml/preprocess.py
```

Input:

```text
data/sample_reviews.csv
```

Output:

```text
data/preprocessed_reviews.csv
```

## Model Training

Run from the backend root:

```bash
uv run python ml/tokenizers/train_sentencepiece.py --model-prefix models/sentencepiece
uv run python ml/train_model.py
```

Input:

```text
data/splits/nsmc_light_train.csv
```

Output:

```text
models/sentencepiece.model
models/sentiment_model.joblib
models/vectorizer.joblib
```

The current service model uses the model-experiment result:

```text
preprocessing: light
tokenizer: SentencePiece
vectorizer: TfidfVectorizer
model: LogisticRegression
```

