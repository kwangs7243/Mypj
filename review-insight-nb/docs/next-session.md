# Next Session Notes

## Current Repository

```text
https://github.com/kwangs7243/Mypj.git
```

Clone on another PC:

```bash
git clone https://github.com/kwangs7243/Mypj.git
```

Project path after clone:

```text
Mypj/review-insight-nb
```

## Current Status

The backend skeleton is ready.

Completed:

- `uv` backend project setup
- FastAPI app entry point
- Pydantic DTO schemas
- service layer for dummy sentiment prediction
- model info endpoint placeholder
- Swagger/OpenAPI docs available from FastAPI

Validated endpoints:

```text
GET /health
GET /api/model-info
POST /api/predict
```

## How to Run Backend

From the backend root:

```bash
cd review-insight-nb/backend
uv sync
uv run uvicorn app.main:app --reload
```

From the repository root:

```bash
uv --directory review-insight-nb/backend run uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Backend File Roles

```text
backend/app/main.py
```

FastAPI app object and route definitions.

```text
backend/app/schemas.py
```

Pydantic DTOs for request and response validation.

```text
backend/app/services/sentiment_service.py
```

Current dummy sentiment prediction logic. Later this will call the trained model.

```text
backend/app/model_loader.py
```

Current model status placeholder. Later this will load `.joblib` model files.

## Important Understanding So Far

Pydantic `BaseModel` is used as the DTO base class.

It provides:

- automatic constructor behavior
- type validation
- request body validation
- response shape validation
- JSON conversion support
- OpenAPI and Swagger documentation generation

`Field(...)` means the field is required.

`description` is mainly for generated API documentation.

## Current API Flow

```text
POST /api/predict
-> main.py route
-> PredictRequest schema validation
-> sentiment_service.predict_sentiment()
-> PredictResponse
-> JSON response
```

## Next Step

Do not connect the model to the API immediately.

First build the ML layer as an independent script.

Planned small step:

1. Create `backend/data/sample_reviews.csv`
2. Create `backend/ml/train_model.py`
3. Load CSV with pandas
4. Split train/test data
5. Vectorize text with `TfidfVectorizer`
6. Train `MultinomialNB`
7. Print accuracy and classification report
8. Save these files with `joblib`

Expected output files:

```text
backend/models/sentiment_model.joblib
backend/models/vectorizer.joblib
```

Run command:

```bash
cd review-insight-nb/backend
uv run python ml/train_model.py
```

## Design Direction

Keep the ML layer independent from FastAPI.

The training script should work without:

- frontend
- FastAPI route objects
- request DTOs

After the training script works, update `model_loader.py` to load the saved `.joblib` files.

Then replace the dummy logic in `sentiment_service.py` with real model prediction.

## Serialization Decision

Use `joblib` for this project.

Reason:

- familiar enough if `pickle` is already understood
- common convention for scikit-learn model persistence
- simple API: `joblib.dump()` and `joblib.load()`
- suitable for saving both model and vectorizer

Security note:

Do not load untrusted `.joblib` or `.pkl` files.

