# Frontend

Simple browser UI for the first MVP.

This first frontend does not use React yet because Node.js and npm are not available in the current local environment. It uses static HTML, CSS, and JavaScript so the owner can focus on the browser-to-API flow before learning frontend tooling.

## Run

1. Start the backend:

```bash
cd review-insight-nb/backend
uv run uvicorn app.main:app --reload
```

2. Open this file in a browser:

```text
frontend/index.html
```

## Current UI

- Review input textarea
- Analyze button
- Model status display
- Model detail display
- Positive and negative sample buttons
- Prediction label
- Confidence
- Positive and negative probabilities
- Probability bars
- Basic error message area
- Frontend validation for empty input and input with no Korean characters

## Current API Flow

```text
Browser form submit
-> frontend validation
-> fetch("http://127.0.0.1:8000/api/predict")
-> FastAPI model prediction
-> JSON response
-> result rendered in the page
```

## Later Direction

After the first browser-to-API MVP works, this frontend can be replaced with React + Vite when Node.js is available.
