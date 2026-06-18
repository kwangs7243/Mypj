# Project Guidance for Codex

## Project

This repository is a portfolio-oriented review sentiment analysis web service using a Naive Bayes machine learning model.

## Collaboration Goals

- Keep the project understandable for the owner.
- Prefer small, explainable steps over large opaque rewrites.
- Record important decisions in `docs/decision-record.md`.
- Record session progress and next actions in `docs/ai-collaboration-log.md`.
- Make every major implementation choice explainable in interviews.

## Technical Direction

- Backend: Python + FastAPI.
- ML: scikit-learn Naive Bayes pipeline.
- Frontend: React + Vite.
- Start with a single-review prediction MVP before CSV upload, database, authentication, or deployment.

## Engineering Rules

- Keep code structure simple and portfolio-friendly.
- Avoid unnecessary abstraction until duplication or complexity justifies it.
- Add comments only when they clarify non-obvious logic.
- Prefer relative paths inside project code.
- Do not hard-code absolute local machine paths.
- Keep generated model files under `backend/models/`.
- Keep raw or sample datasets under `backend/data/`.

## Documentation Rules

When making meaningful progress, update:

- `docs/ai-collaboration-log.md`
- `docs/next-session.md` before stopping for the day or switching PCs
- `docs/decision-record.md` when a design choice is made
- `README.md` when setup or usage changes

## Current Next Step

Continue with the ML layer, not frontend.

Build `backend/ml/train_model.py` as an independent script before connecting the model to FastAPI. The script should train a Naive Bayes model, save the model and vectorizer with `joblib`, and be runnable with:

```bash
cd review-insight-nb/backend
uv run python ml/train_model.py
```

## Git Rules

- Use `type: Korean summary` commit messages.
- Follow examples in `docs/git-convention.md`.
- Prefer small commits that each explain one meaningful project step.
