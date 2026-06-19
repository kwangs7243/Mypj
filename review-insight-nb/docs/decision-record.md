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

### Keep Layers Independent for Future Model Comparison

Reason:

- The first MVP should stay simple, but the project may later compare multiple ML models, datasets, vectorizers, or model settings.
- The ML layer should work without knowing whether the caller is FastAPI, React, a CLI script, or another service.
- The API layer should expose a stable request/response contract without depending on one specific model implementation.
- The frontend should communicate with the backend through API responses, not through knowledge of model internals.
- This structure keeps future changes safer: replacing the dataset, switching from `MultinomialNB` to another model, or adding model selection should not require rewriting every layer.

Rule:

- ML code owns training, loading, vectorizing, prediction, and evaluation logic.
- FastAPI owns HTTP routes, request validation, response shape, and service orchestration.
- React owns user interaction and API communication.
- Shared contracts should be simple data shapes such as text input, predicted label, confidence, probabilities, and optional model metadata.

Future direction:

- The first implementation will use one default model.
- A later version may add model selection through an API parameter and a frontend select box.
- Model comparison should be added after the single-model MVP is stable.

### Save Preprocessed Data Before Model Training

Reason:

- Future model comparison should use the same preprocessed input data.
- Saving the preprocessed CSV makes the training step reproducible and easier to inspect.
- Dataset changes and preprocessing changes can be tracked separately from model changes.
- The first training script can focus on model training instead of mixing raw data cleanup with training logic.

Rule:

- Keep raw or sample data in `backend/data/sample_reviews.csv`.
- Save cleaned reusable data to `backend/data/preprocessed_reviews.csv`.
- Training scripts should read the preprocessed file first.
- If preprocessing rules change, regenerate the preprocessed file before retraining models.

### 모델 학습 전에 전처리 데이터를 저장

이유:

- 이후 여러 모델을 비교할 때 같은 전처리 입력 데이터를 사용해야 공정하게 비교할 수 있다.
- 전처리된 CSV를 저장하면 학습 과정을 재현하기 쉽고 사람이 직접 확인하기도 쉽다.
- 데이터셋 변경, 전처리 변경, 모델 변경을 서로 분리해서 추적할 수 있다.
- 첫 학습 스크립트는 원본 데이터 정리와 모델 학습을 섞지 않고 모델 학습에 집중할 수 있다.

규칙:

- 원본 또는 샘플 데이터는 `backend/data/sample_reviews.csv`에 둔다.
- 정제된 재사용 데이터는 `backend/data/preprocessed_reviews.csv`에 저장한다.
- 학습 스크립트는 우선 전처리된 파일을 읽는다.
- 전처리 규칙이 바뀌면 모델을 다시 학습하기 전에 전처리 파일을 다시 생성한다.

### Start With Korean-Only Text Preprocessing

Reason:

- The MVP target is Korean review sentiment analysis.
- Korean and English need different preprocessing and tokenization strategies.
- Keeping English text would make the preprocessing responsibility less clear before the first model is trained.
- English words in typical Korean product reviews are expected to have limited value for the first MVP compared with the extra complexity they introduce.
- The model itself can learn from numeric vectors regardless of language, but the preprocessing and tokenization pipeline should be intentionally scoped.

Rule:

- The first preprocessing version keeps only Korean characters and whitespace.
- English letters, numbers, punctuation, emojis, and other symbols are removed.
- Do not add a morphological analyzer yet.
- Use the simple Korean-only preprocessing first, then evaluate whether tokenization quality is a real bottleneck.
- If needed later, add Korean tokenization as a separate tokenizer step so model training code can still reuse the same preprocessed dataset contract.

Future direction:

- Possible Korean tokenizers include morphological analyzers such as Okt, Mecab, Komoran, or Kiwi.
- Tokenizer choice should be decided later based on setup cost, Windows compatibility, explanation difficulty, and actual model performance.

### 한글 전용 전처리로 시작

이유:

- MVP 목표는 한국어 리뷰 감성 분석이다.
- 한글과 영어는 전처리 방식과 단어 분리 방식이 다르다.
- 첫 모델을 학습하기 전부터 영어를 함께 살려두면 전처리 책임이 애매해질 수 있다.
- 일반적인 한국어 상품 리뷰에서 영어 단어가 줄 수 있는 성능 이득은, 그로 인해 생기는 전처리 복잡도에 비해 크지 않을 가능성이 높다.
- 모델은 언어를 직접 이해하는 것이 아니라 숫자 벡터를 학습하지만, 그 숫자 벡터를 만들기 전의 전처리와 토큰화 범위는 의도적으로 제한해야 한다.

규칙:

- 첫 전처리 버전은 한글과 공백만 남긴다.
- 영어, 숫자, 문장부호, 이모지, 기타 기호는 제거한다.
- 아직 형태소 분석기는 추가하지 않는다.
- 먼저 단순한 한글 전용 전처리로 학습하고, 토큰화 품질이 실제 병목인지 확인한다.
- 이후 필요하면 한국어 토큰화 단계를 별도 tokenizer 단계로 추가해 학습 코드가 같은 전처리 데이터 계약을 계속 사용할 수 있게 한다.

향후 방향:

- 후보 형태소 분석기로는 Okt, Mecab, Komoran, Kiwi 등이 있다.
- tokenizer 선택은 설치 난이도, Windows 호환성, 설명 난이도, 실제 모델 성능을 보고 나중에 결정한다.

### Reject Non-Korean Prediction Input After Cleaning

Reason:

- The preprocessing function may return an empty string when the input contains no Korean characters.
- Empty cleaned text is valid as an intermediate dataset preprocessing result because those rows can be dropped.
- Empty cleaned text is not valid user input for the prediction API because the service cannot provide a meaningful Korean review sentiment result.
- The backend should enforce this contract even if the frontend later blocks invalid input earlier.

Rule:

- Keep `clean_text()` reusable and side-effect free.
- Do not raise prediction-specific errors inside `clean_text()`.
- In the sentiment service, return a 400 error when cleaned user input is empty.
- Later, add frontend validation so requests with no Korean characters are blocked before reaching the backend.

### 정제 후 한글이 없는 예측 입력 거부

이유:

- 입력에 한글이 없으면 전처리 함수가 빈 문자열을 반환할 수 있다.
- 데이터셋 전처리 중간 결과로 빈 문자열이 나오는 것은 자연스럽고, 해당 행은 이후 제거하면 된다.
- 하지만 사용자의 예측 요청에서 정제 결과가 빈 문자열이면 한국어 리뷰 감성 분석 서비스가 의미 있는 결과를 제공할 수 없다.
- 이후 프론트엔드에서 먼저 막더라도 백엔드는 이 입력 계약을 직접 지켜야 한다.

규칙:

- `clean_text()`는 재사용 가능하고 부작용 없는 함수로 유지한다.
- 예측 API 전용 예외를 `clean_text()` 내부에서 발생시키지 않는다.
- 감성 예측 서비스에서 정제된 사용자 입력이 비어 있으면 400 에러를 반환한다.
- 이후 프론트엔드 검증을 추가해 한글이 없는 요청은 백엔드에 도달하기 전에 막는다.

### 향후 모델 비교를 위해 계층 독립성 유지

이유:

- 1차 MVP는 단순하게 만들지만, 이후에는 여러 ML 모델, 데이터셋, 벡터라이저, 모델 설정을 비교할 수 있다.
- ML 계층은 호출자가 FastAPI인지, React인지, CLI 스크립트인지 몰라도 동작해야 한다.
- API 계층은 특정 모델 구현에 묶이지 않고 안정적인 요청/응답 계약을 제공해야 한다.
- 프론트엔드는 모델 내부 구현을 알 필요 없이 백엔드 API 응답만 보고 화면을 구성해야 한다.
- 이렇게 분리하면 데이터셋 교체, `MultinomialNB`에서 다른 모델로 변경, 모델 선택 기능 추가가 전체 구조를 흔들지 않고 가능해진다.

규칙:

- ML 코드는 학습, 로딩, 벡터화, 예측, 평가 로직을 담당한다.
- FastAPI는 HTTP 라우트, 요청 검증, 응답 형태, 서비스 호출 흐름을 담당한다.
- React는 사용자 입력, 화면 상태, API 통신을 담당한다.
- 계층 사이의 공통 계약은 리뷰 텍스트, 예측 라벨, confidence, probabilities, model metadata 같은 단순한 데이터 형태로 유지한다.

향후 방향:

- 첫 구현은 하나의 기본 모델만 사용한다.
- 이후 버전에서 API 파라미터와 프론트엔드 select box를 통해 모델 선택 기능을 추가할 수 있다.
- 모델 비교 기능은 단일 모델 MVP가 안정적으로 완성된 뒤 추가한다.

### Separate Documentation Language by Reader

Reason:

- Codex may read Korean Markdown incorrectly when terminal encoding settings differ between PCs.
- AI-facing continuity documents should be easy for Codex to parse reliably.
- Owner-facing documents should remain easy for the project owner to read, explain, and reuse in portfolio/interview contexts.
- Important decisions should be recorded in both English and Korean so both Codex and the owner can use them.

Rule:

- Use English-first documentation for Codex handoff files such as `AGENTS.md` and `docs/next-session.md`.
- Use Korean-first documentation for owner-facing files such as `README.md`, `docs/project-plan.md`, and `docs/portfolio-summary.md`.
- Use bilingual sections for shared decision records and major progress summaries.
- When equivalent English Codex-facing documentation exists, Codex should treat it as the primary source and read Korean owner-facing documents only when Korean wording, portfolio explanations, or missing details are needed.

### 문서 언어를 읽는 사람 기준으로 분리

이유:

- PC나 터미널 인코딩 설정이 달라지면 Codex가 한글 Markdown을 깨진 텍스트로 읽을 수 있다.
- Codex가 이어서 작업해야 하는 문서는 안정적으로 읽히는 것이 중요하다.
- 프로젝트 소유자가 읽는 문서는 한글로 남겨야 포트폴리오와 면접에서 직접 설명하기 쉽다.
- 중요한 결정은 Codex와 프로젝트 소유자 모두가 이해할 수 있도록 영어와 한글을 함께 남긴다.

규칙:

- `AGENTS.md`, `docs/next-session.md`처럼 Codex 인수인계용 문서는 영어 중심으로 작성한다.
- `README.md`, `docs/project-plan.md`, `docs/portfolio-summary.md`처럼 사용자가 읽는 문서는 한글 중심으로 작성한다.
- `docs/decision-record.md`와 주요 진행 요약처럼 양쪽 모두에게 중요한 문서는 영어와 한글을 함께 작성한다.
- 같은 내용의 Codex용 영어 문서가 있다면 Codex는 그 문서를 우선 기준으로 삼고, 한글 사용자용 문서는 한글 문구, 포트폴리오 설명, 또는 영어 문서에 없는 세부 내용이 필요할 때만 읽는다.

