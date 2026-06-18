# AI Collaboration Log

## 2026-06-18

### Context

프로젝트 목적과 방향을 정리했다.

목표는 Naive Bayes 기반 리뷰 감성 분석 웹서비스를 완성하면서, 개발자가 AI 협업 상황에서도 프로젝트 전체 구조와 의사결정을 통제할 수 있는지 체험하는 것이다.

### Decisions

- 프로젝트는 현재 작업 폴더 아래 `review-insight-nb`로 시작한다.
- 1차 목표는 단건 리뷰 입력 후 긍정/부정 예측 결과를 웹에서 확인하는 MVP다.
- 백엔드는 Python + FastAPI를 사용한다.
- 프론트엔드는 React + Vite를 사용한다.
- 머신러닝은 scikit-learn의 Naive Bayes 계열 모델을 사용한다.
- 커밋 메시지는 `type: 작업 요약` 형식을 사용한다.
- GitHub private repository는 `https://github.com/kwangs7243/Mypj.git`를 사용한다.
- 백엔드 패키지 관리는 `requirements.txt` 대신 `uv`, `pyproject.toml`, `uv.lock`을 기준으로 한다.

### GitHub

원격 저장소:

```text
https://github.com/kwangs7243/Mypj.git
```

다른 PC에서 이어서 작업할 때:

```bash
git clone https://github.com/kwangs7243/Mypj.git
```

### Backend Setup

완료한 작업:

- `uv init --bare`로 백엔드 Python 프로젝트 초기화
- `.venv` 생성
- FastAPI, uvicorn, pandas, scikit-learn, joblib 설치
- FastAPI 테스트용 개발 의존성 `httpx2` 추가
- `GET /health` 구현
- `POST /api/predict` 더미 응답 구현
- 요청/응답 DTO 역할의 Pydantic schema 작성
- 예측 로직을 `services/sentiment_service.py`로 분리

검증:

```text
GET /health -> {"status": "ok"}
POST /api/predict -> positive 더미 예측 응답 확인
```

### Next Actions

1. 백엔드 서버를 실제로 띄워 `/docs` 확인
2. 데이터셋 후보 결정
3. 모델 학습 스크립트 작성
4. 저장된 모델을 API에 연결
5. 프론트엔드 Vite 앱 생성

