const API_BASE_URL = "http://127.0.0.1:8000";

const form = document.querySelector("#review-form");
const reviewText = document.querySelector("#review-text");
const analyzeButton = document.querySelector("#analyze-button");
const formMessage = document.querySelector("#form-message");
const modelStatus = document.querySelector("#model-status");
const resultPanel = document.querySelector("#result-panel");
const resultLabel = document.querySelector("#result-label");
const resultConfidence = document.querySelector("#result-confidence");
const resultNegative = document.querySelector("#result-negative");
const resultPositive = document.querySelector("#result-positive");

function formatPercent(value) {
  return `${(value * 100).toFixed(1)}%`;
}

function formatLabel(label) {
  return label === "positive" ? "긍정" : "부정";
}

function containsKorean(text) {
  return /[가-힣]/.test(text);
}

function setMessage(message) {
  formMessage.textContent = message;
}

function setLoading(isLoading) {
  analyzeButton.disabled = isLoading;
  analyzeButton.textContent = isLoading ? "Analyzing..." : "Analyze";
}

function renderPrediction(prediction) {
  resultLabel.textContent = formatLabel(prediction.label);
  resultConfidence.textContent = formatPercent(prediction.confidence);
  resultNegative.textContent = formatPercent(prediction.probabilities.negative);
  resultPositive.textContent = formatPercent(prediction.probabilities.positive);
  resultPanel.hidden = false;
}

async function loadModelStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/model-info`);
    const modelInfo = await response.json();
    modelStatus.textContent = `Model status: ${modelInfo.status} (${modelInfo.model})`;
  } catch {
    modelStatus.textContent = "Model status: backend unavailable";
  }
}

async function requestPrediction(text) {
  const response = await fetch(`${API_BASE_URL}/api/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Prediction request failed.");
  }

  return data;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const text = reviewText.value.trim();
  setMessage("");

  if (!text) {
    setMessage("리뷰를 입력해 주세요.");
    resultPanel.hidden = true;
    return;
  }

  if (!containsKorean(text)) {
    setMessage("한글 리뷰를 입력해 주세요.");
    resultPanel.hidden = true;
    return;
  }

  try {
    setLoading(true);
    const prediction = await requestPrediction(text);
    renderPrediction(prediction);
  } catch (error) {
    resultPanel.hidden = true;
    setMessage(error.message);
  } finally {
    setLoading(false);
  }
});

loadModelStatus();
