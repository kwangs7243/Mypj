# Review Insight NB

Naive Bayes 기반 한국어 리뷰 감성 분석 웹서비스 프로젝트입니다.

## Project Goal

리뷰 텍스트를 입력하면 머신러닝 모델이 긍정/부정 감성을 예측하고, 예측 결과와 확률을 웹 화면에서 확인할 수 있는 서비스를 완성합니다.

이 프로젝트의 핵심 목표는 단순 구현이 아니라, 프로젝트 전체 구조를 직접 통제하면서 AI 협업으로 완성까지 밀어보는 것입니다.

## MVP Scope

1. 한국어 리뷰 데이터셋 준비
2. 텍스트 전처리
3. Naive Bayes 모델 학습
4. 학습 모델과 벡터라이저 저장
5. FastAPI 예측 API 구현
6. React 프론트엔드 구현
7. 리뷰 입력 후 긍정/부정 결과 출력
8. README와 포트폴리오 문서 정리

## Tech Stack

- Backend: Python, FastAPI, scikit-learn, pandas, joblib
- Frontend: React, Vite
- ML: Multinomial Naive Bayes, CountVectorizer or TfidfVectorizer
- Documentation: Markdown

## Directory Structure

```text
review-insight-nb/
├─ backend/
│  ├─ app/
│  │  ├─ services/
│  │  └─ README.md
│  ├─ ml/
│  ├─ models/
│  ├─ data/
│  ├─ requirements.txt
│  └─ README.md
├─ frontend/
│  ├─ src/
│  │  ├─ api/
│  │  ├─ components/
│  │  └─ pages/
│  └─ README.md
├─ docs/
│  ├─ project-plan.md
│  ├─ ai-collaboration-log.md
│  ├─ decision-record.md
│  └─ portfolio-summary.md
└─ AGENTS.md
```

## First Completion Target

로컬 환경에서 백엔드와 프론트엔드를 실행한 뒤, 웹 화면에 리뷰를 입력하면 긍정/부정 예측 결과가 출력되는 상태를 1차 완성으로 봅니다.

