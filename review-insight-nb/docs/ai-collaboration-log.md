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

## 2026-06-19

### Progress

Implemented the first data preprocessing step before model training.

Completed:

- Created `backend/data/sample_reviews.csv`.
- Added 20 Korean sample reviews: 10 positive and 10 negative.
- Created `backend/ml/preprocess.py` as an independent script.
- The preprocessing script loads raw review data, validates required columns, cleans text, normalizes labels, removes invalid or empty rows, removes duplicates, and saves reusable preprocessed data.
- Generated `backend/data/preprocessed_reviews.csv`.

Validation:

```text
Raw rows: 20
Preprocessed rows: 20
Label counts: {'positive': 10, 'negative': 10}
```

### 진행 내용

모델 학습 전에 첫 데이터 전처리 단계를 구현했다.

완료:

- `backend/data/sample_reviews.csv` 생성
- 긍정 10개, 부정 10개의 한국어 샘플 리뷰 추가
- 독립 실행 가능한 `backend/ml/preprocess.py` 생성
- 전처리 스크립트에서 원본 리뷰 로드, 필수 컬럼 검증, 텍스트 정리, 라벨 정규화, 빈 값/잘못된 값 제거, 중복 제거, 전처리 데이터 저장을 수행
- `backend/data/preprocessed_reviews.csv` 생성

검증:

```text
Raw rows: 20
Preprocessed rows: 20
Label counts: {'positive': 10, 'negative': 10}
```

### Next Actions

1. Create `backend/ml/train_model.py`.
2. Load `backend/data/preprocessed_reviews.csv`.
3. Split train/test data.
4. Train `TfidfVectorizer` + `MultinomialNB`.
5. Save `backend/models/sentiment_model.joblib` and `backend/models/vectorizer.joblib`.

### 다음 작업

1. `backend/ml/train_model.py` 생성
2. `backend/data/preprocessed_reviews.csv` 로드
3. train/test 데이터 분리
4. `TfidfVectorizer` + `MultinomialNB` 학습
5. `backend/models/sentiment_model.joblib`, `backend/models/vectorizer.joblib` 저장

### Model Training Progress

Implemented the first independent model training script.

Completed:

- Created `backend/ml/train_model.py`.
- Loaded `backend/data/preprocessed_reviews.csv`.
- Split data into train/test sets with stratified labels.
- Trained `TfidfVectorizer` + `MultinomialNB`.
- Printed accuracy and classification report.
- Saved `backend/models/sentiment_model.joblib`.
- Saved `backend/models/vectorizer.joblib`.
- Verified that the saved artifacts can be loaded and used for prediction.

Latest training output:

```text
Train rows: 15
Test rows: 5
Accuracy: 0.4000
```

Note:

The current dataset has only 20 sample rows, so the score is not a meaningful final model quality signal. It is mainly a pipeline validation result.

### 모델 학습 진행 내용

첫 독립 모델 학습 스크립트를 구현했다.

완료:

- `backend/ml/train_model.py` 생성
- `backend/data/preprocessed_reviews.csv` 로드
- 라벨 비율을 유지하면서 train/test 데이터 분리
- `TfidfVectorizer` + `MultinomialNB` 학습
- accuracy와 classification report 출력
- `backend/models/sentiment_model.joblib` 저장
- `backend/models/vectorizer.joblib` 저장
- 저장된 모델과 벡터라이저를 다시 로드해 예측 가능 여부 확인

최근 학습 출력:

```text
Train rows: 15
Test rows: 5
Accuracy: 0.4000
```

메모:

현재 데이터셋은 샘플 20개뿐이므로 점수는 최종 모델 품질 지표로 보기 어렵다. 지금은 학습 파이프라인 검증 결과로 본다.

### Next Actions

1. Update `backend/app/model_loader.py` to load saved `.joblib` files.
2. Replace dummy sentiment logic with real model prediction.
3. Verify `POST /api/predict` returns real model output.

### 다음 작업

1. `backend/app/model_loader.py`에서 저장된 `.joblib` 파일 로드
2. 더미 감성 예측 로직을 실제 모델 예측으로 교체
3. `POST /api/predict`가 실제 모델 결과를 반환하는지 검증

### API Model Connection Progress

Connected the saved model artifacts to the FastAPI service.

Completed:

- Updated `backend/app/model_loader.py` to load `sentiment_model.joblib` and `vectorizer.joblib`.
- Added cached model loading so the artifacts are not loaded repeatedly for every request.
- Updated `GET /api/model-info` to report `trained` when both artifact files exist.
- Replaced dummy keyword-based prediction logic in `backend/app/services/sentiment_service.py`.
- Prediction now uses the same Korean-only cleaning rule, vectorizer transform, model prediction, and model probabilities.

Validation:

```text
GET /api/model-info -> {'status': 'trained', 'trained': True}
POST /api/predict -> real model prediction response
```

Example:

```text
Input: 배송이 빠르고 제품이 좋아요
Prediction: positive
Confidence: 0.6744
```

### API 모델 연결 진행 내용

저장된 모델 파일을 FastAPI 서비스에 연결했다.

완료:

- `backend/app/model_loader.py`에서 `sentiment_model.joblib`, `vectorizer.joblib` 로드
- 요청마다 모델 파일을 반복 로드하지 않도록 캐시 적용
- `GET /api/model-info`가 모델 파일 존재 여부에 따라 `trained` 상태를 반환하도록 수정
- `backend/app/services/sentiment_service.py`의 더미 키워드 기반 예측 로직 제거
- 예측은 이제 한글 전용 정제, 벡터라이저 변환, 모델 예측, 모델 확률을 사용한다.

검증:

```text
GET /api/model-info -> {'status': 'trained', 'trained': True}
POST /api/predict -> 실제 모델 예측 응답
```

예시:

```text
입력: 배송이 빠르고 제품이 좋아요
예측: positive
confidence: 0.6744
```

### Next Actions

1. Create the Vite React frontend.
2. Build a simple review input form.
3. Call `POST /api/predict`.
4. Display label, confidence, and probabilities.

### 다음 작업

1. Vite React 프론트엔드 생성
2. 간단한 리뷰 입력 form 구현
3. `POST /api/predict` 호출
4. label, confidence, probabilities 화면 출력

### Frontend MVP Progress

Started the first frontend MVP with static HTML/CSS/JavaScript instead of React.

Reason:

- Node.js and npm are not available in the current environment.
- The owner is backend-focused, so the first frontend goal is understanding the browser-to-API flow.

Completed:

- Created `frontend/index.html`.
- Created `frontend/styles.css`.
- Created `frontend/app.js`.
- Added a review textarea, analyze button, model status display, result area, and error message area.
- Added `fetch()` calls to `GET /api/model-info` and `POST /api/predict`.
- Added FastAPI CORS middleware so the static frontend can call the local backend.

Validation:

```text
GET /api/model-info -> trained true
POST /api/predict -> real prediction response
CORS preflight /api/predict -> 200, allow-origin *
```

Browser automation was not available in the current tool context, so visual/manual browser testing still remains.

### 프론트엔드 MVP 진행 내용

React 대신 정적 HTML/CSS/JavaScript로 첫 프론트엔드 MVP를 시작했다.

이유:

- 현재 환경에서 Node.js와 npm을 사용할 수 없다.
- 프로젝트 소유자는 백엔드 중심으로 공부해왔으므로, 첫 프론트 목표는 브라우저와 API의 연결 흐름을 이해하는 것이다.

완료:

- `frontend/index.html` 생성
- `frontend/styles.css` 생성
- `frontend/app.js` 생성
- 리뷰 입력 textarea, 분석 버튼, 모델 상태 표시, 결과 영역, 에러 메시지 영역 추가
- `GET /api/model-info`, `POST /api/predict`를 호출하는 `fetch()` 코드 추가
- 정적 프론트엔드가 로컬 백엔드를 호출할 수 있도록 FastAPI CORS middleware 추가

검증:

```text
GET /api/model-info -> trained true
POST /api/predict -> 실제 예측 응답
CORS preflight /api/predict -> 200, allow-origin *
```

현재 도구 환경에서는 브라우저 자동화가 노출되지 않아 화면 기반 수동 테스트는 아직 남아 있다.

### Next Actions

1. Start the backend server.
2. Open `frontend/index.html` in a browser.
3. Manually test valid and invalid inputs.
4. Review the frontend code flow.

### 다음 작업

1. 백엔드 서버 실행
2. 브라우저에서 `frontend/index.html` 열기
3. 정상 입력과 잘못된 입력 수동 테스트
4. 프론트엔드 코드 흐름 리뷰

