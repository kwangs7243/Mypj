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
- sample review dataset
- independent preprocessing script
- saved preprocessed dataset for future model training and comparison
- independent model training script
- saved `MultinomialNB` model and `TfidfVectorizer` artifacts
- saved model artifacts connected to FastAPI prediction service

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

Current real sentiment prediction logic. It loads the saved model/vectorizer through `model_loader.py`.

```text
backend/app/model_loader.py
```

Loads saved `.joblib` model files and reports model status.

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

## Review Rule

Always include a code review after implementation work in this project.

The review should help the owner compare their own reading with Codex's reading. Keep it focused on:

- code flow
- responsibility boundaries
- risks or fragile parts
- learning points
- small improvement candidates

## 리뷰 규칙

이 프로젝트에서는 구현 작업 후 항상 코드 리뷰를 함께 진행한다.

리뷰는 프로젝트 소유자가 직접 읽은 내용과 Codex의 해석을 대조할 수 있게 돕는 목적이다. 다음 항목을 중심으로 짧고 명확하게 정리한다.

- 코드 흐름
- 책임 분리
- 위험하거나 약한 부분
- 학습 포인트
- 작은 개선 후보

## Current API Flow

```text
POST /api/predict
-> main.py route
-> PredictRequest schema validation
-> sentiment_service.predict_sentiment()
-> model_loader.load_model_bundle()
-> vectorizer.transform()
-> model.predict() and model.predict_proba()
-> PredictResponse
-> JSON response
```

## Next Step

The preprocessing, model training, and API model connection are now complete. Next, start the frontend MVP.

Planned small step:

1. Create the Vite React frontend.
2. Build a simple review input form.
3. Call `POST /api/predict`.
4. Display label, confidence, and probabilities.
5. Keep model selection out of the first frontend MVP.

Expected output files:

```text
backend/models/sentiment_model.joblib
backend/models/vectorizer.joblib
```

Current data files:

```text
backend/data/sample_reviews.csv
backend/data/preprocessed_reviews.csv
```

Preprocessing command:

```bash
cd review-insight-nb/backend
uv run python ml/preprocess.py
```

Training command:

```bash
cd review-insight-nb/backend
uv run python ml/train_model.py
```

Latest training check:

```text
Train rows: 15
Test rows: 5
Accuracy: 0.4000
```

The score is low because the current sample dataset is intentionally tiny. Treat it as a pipeline check, not as a final model quality signal.

Latest API model connection check:

```text
GET /api/model-info -> trained true
POST /api/predict -> real model prediction response
```

Prediction input rule:

- The backend cleans input with the same Korean-only rule used by preprocessing.
- If cleaned user input contains no Korean characters, `POST /api/predict` returns 400.
- Later, add frontend validation so invalid requests are blocked before submission.

Current preprocessing rule:

- Keep only Korean characters and whitespace.
- Remove English letters, numbers, punctuation, emojis, and other symbols.
- Do not add a Korean morphological analyzer yet.
- Add tokenizer comparison later only if simple Korean-only preprocessing becomes a real limitation.

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

## Layer Independence Direction

Keep each layer replaceable.

- ML layer: training, vectorizing, loading, predicting, and evaluating
- API layer: HTTP routes, schemas, response contracts, and service orchestration
- Frontend layer: user input, UI state, and API communication

The first version should use one default model, `MultinomialNB`. Do not design the frontend or API around model internals. Later, the project may add model comparison, dataset changes, vectorizer comparison, or model selection through an API parameter and a frontend select box.

The important rule is that a model should work regardless of whether the caller is a web API, frontend, CLI script, or another service. The frontend should also continue to work as long as the backend response contract stays stable, even if the underlying ML model changes.

## 계층 독립성 방향

각 계층은 교체 가능한 구조로 유지한다.

- ML 계층: 학습, 벡터화, 로딩, 예측, 평가
- API 계층: HTTP 라우트, schema, 응답 계약, 서비스 호출 흐름
- 프론트엔드 계층: 사용자 입력, 화면 상태, API 통신

첫 버전은 기본 모델 하나인 `MultinomialNB`만 사용한다. 프론트엔드나 API를 모델 내부 구현에 맞춰 설계하지 않는다. 이후에는 모델 비교, 데이터셋 변경, 벡터라이저 비교, API 파라미터와 프론트엔드 select box를 통한 모델 선택 기능을 추가할 수 있다.

중요한 규칙은 모델이 웹 API, 프론트엔드, CLI 스크립트, 다른 서비스 중 무엇에서 호출되든 독립적으로 동작해야 한다는 것이다. 프론트엔드도 백엔드 응답 계약만 유지된다면 내부 ML 모델이 바뀌어도 계속 동작해야 한다.

## Documentation Language Rule

Use reader-based documentation language.

- Codex handoff documents should be English-first.
- Owner-facing explanation documents should be Korean-first.
- Shared decisions and major progress summaries should include both English and Korean.
- When equivalent English Codex-facing documentation exists, Codex should use it as the primary source and read Korean owner-facing documents only when Korean wording, portfolio explanations, or missing details are needed.

This rule exists because Korean Markdown can be misread when terminal encoding differs between PCs. English handoff notes make continuation safer for Codex, while Korean owner-facing notes keep the project explainable for portfolio and interview use.

## 문서 언어 규칙

문서는 읽는 사람 기준으로 언어를 나눈다.

- Codex가 이어서 읽어야 하는 인수인계 문서는 영어 중심으로 작성한다.
- 프로젝트 소유자가 읽는 설명 문서는 한글 중심으로 작성한다.
- 중요한 결정과 주요 진행 요약은 영어와 한글을 함께 작성한다.
- 같은 내용의 Codex용 영어 문서가 있다면 Codex는 그 문서를 우선 기준으로 삼고, 한글 사용자용 문서는 한글 문구, 포트폴리오 설명, 또는 영어 문서에 없는 세부 내용이 필요할 때만 읽는다.

이 규칙은 PC나 터미널 인코딩 차이로 한글 Markdown이 깨져 보일 수 있기 때문에 추가했다. Codex용 인수인계는 영어로 안정성을 높이고, 사용자용 설명 문서는 한글로 남겨 포트폴리오와 면접 설명에 활용한다.

## Serialization Decision

Use `joblib` for this project.

Reason:

- familiar enough if `pickle` is already understood
- common convention for scikit-learn model persistence
- simple API: `joblib.dump()` and `joblib.load()`
- suitable for saving both model and vectorizer

Security note:

Do not load untrusted `.joblib` or `.pkl` files.

