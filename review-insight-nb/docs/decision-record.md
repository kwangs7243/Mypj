# Decision Record

## 2026-06-18

### Use Naive Bayes for the First Model

Reason:

- It is simple enough to explain in a portfolio interview.
- It works naturally with `CountVectorizer` or `TfidfVectorizer`.
- It is a good first text classification model for understanding the full ML flow.

### Build the MVP Before Advanced Features

Reason:

- The first goal is completing a working project, not adding every possible feature.
- CSV upload, database, authentication, and deployment will come after the basic review prediction flow works.

### Keep Continuity in Markdown

Reason:

- The project may continue on another PC.
- Codex context may not carry across devices or sessions.
- Markdown notes make the next session easier to recover.

### Use uv for Backend Dependency Management

Reason:

- The user already knows `uv`.
- `pyproject.toml` and `uv.lock` make the backend environment reproducible across home and academy PCs.
- Python backend dependencies stay separate from future Node frontend dependencies.

### Build the Backend API Skeleton Before Model Integration

Reason:

- This project is a web service, not only an ML experiment.
- Defining request and response schemas first makes the API contract clear.
- Flask route, DTO, and service-layer experience maps well to FastAPI.

### Use joblib for Model Persistence

Reason:

- It is similar in spirit to `pickle`, but common for scikit-learn model persistence.
- It can save both the trained model and the fitted vectorizer.
- It keeps the training step and API loading step clearly separated.

Security note:

- Do not load untrusted `.joblib` or `.pkl` files.

### Build ML Training Before API Integration

Reason:

- The ML layer should run independently from FastAPI and React.
- `backend/ml/train_model.py` should train, evaluate, and save model artifacts first.
- After that, `model_loader.py` can load saved `.joblib` files for API prediction.

