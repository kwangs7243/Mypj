# Project Guidance for Codex

## Project

This repository is a portfolio-oriented review sentiment analysis web service using a Naive Bayes machine learning model.

## Collaboration Goals

- Keep the project understandable for the owner.
- Prefer small, explainable steps over large opaque rewrites.
- After each implementation step, include a code review so the owner can compare Codex's review with their own reading.
- Record important decisions in `docs/decision-record.md`.
- Record session progress and next actions in `docs/ai-collaboration-log.md`.
- Make every major implementation choice explainable in interviews.

## Technical Direction

- Backend: Python + FastAPI.
- ML: scikit-learn Naive Bayes pipeline.
- Frontend: React + Vite.
- Start with a single-review prediction MVP before CSV upload, database, authentication, or deployment.
- Keep layers independent: ML should not depend on FastAPI or React, FastAPI should expose stable request/response contracts, and React should depend on API responses rather than model internals.
- Design the first version around one default model, but leave room for later model comparison or model selection without rewriting every layer.

## Engineering Rules

- Keep code structure simple and portfolio-friendly.
- Avoid unnecessary abstraction until duplication or complexity justifies it.
- Add comments only when they clarify non-obvious logic.
- Treat review as part of the development loop: after implementation, explain code flow, risks, learning points, and small improvement candidates before moving to the next feature.
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

## Documentation Language Rules

Separate documentation by reader.

AI-facing continuity documents should be written in English so Codex can read them reliably across terminals, PCs, and encoding settings.

Owner-facing explanation documents should be written in Korean so the project owner can review and explain the project comfortably.

When a document is important to both Codex and the owner, include both English and Korean sections.

If an English Codex-facing document already contains the same handoff or rule, Codex should use that English document as the primary source. Korean owner-facing documents do not need to be read unless the task requires checking user-facing wording, Korean explanations, portfolio text, or a missing detail not covered by the English handoff.

Suggested split:

- English-first for Codex: `AGENTS.md`, `docs/next-session.md`, technical handoff notes
- Korean-first for the owner: `README.md`, `docs/project-plan.md`, `docs/portfolio-summary.md`
- Bilingual when decisions matter: `docs/decision-record.md`, major progress summaries

## 문서 언어 규칙

문서는 읽는 사람 기준으로 나눈다.

Codex가 이어서 읽어야 하는 작업 인수인계 문서는 영어로 작성한다. 터미널, PC, 인코딩 설정이 달라도 안정적으로 읽기 위함이다.

프로젝트 소유자가 읽고 이해해야 하는 설명 문서는 한글로 작성한다. 포트폴리오와 면접에서 직접 설명하기 쉽게 하기 위함이다.

Codex와 프로젝트 소유자 모두에게 중요한 문서는 영어와 한글을 함께 작성한다.

같은 인수인계 내용이나 작업 규칙이 Codex용 영어 문서에 이미 정리되어 있다면, Codex는 그 영어 문서를 우선 기준으로 삼는다. 한글 사용자용 문서는 사용자에게 보이는 문구, 한글 설명, 포트폴리오 문장, 또는 영어 인수인계에 없는 세부 내용을 확인해야 할 때만 보조로 읽는다.

권장 분기:

- Codex용 영어 중심: `AGENTS.md`, `docs/next-session.md`, 기술 인수인계 메모
- 사용자용 한글 중심: `README.md`, `docs/project-plan.md`, `docs/portfolio-summary.md`
- 중요한 결정은 양쪽 모두: `docs/decision-record.md`, 주요 진행 요약

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
