const API_BASE_URL = "http://127.0.0.1:8000";

const form = document.querySelector("#review-form");
const reviewText = document.querySelector("#review-text");
const analyzeButton = document.querySelector("#analyze-button");
const formMessage = document.querySelector("#form-message");
const modelStatus = document.querySelector("#model-status");
const modelDetail = document.querySelector("#model-detail");
const resultPanel = document.querySelector("#result-panel");
const resultLabel = document.querySelector("#result-label");
const resultConfidence = document.querySelector("#result-confidence");
const resultNegative = document.querySelector("#result-negative");
const resultPositive = document.querySelector("#result-positive");
const negativeBar = document.querySelector("#negative-bar");
const positiveBar = document.querySelector("#positive-bar");
const negativeBarValue = document.querySelector("#negative-bar-value");
const positiveBarValue = document.querySelector("#positive-bar-value");
const sampleButtons = document.querySelectorAll(".sample-button");

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

function clearResult() {
  resultPanel.hidden = true;
}

function setLoading(isLoading) {
  analyzeButton.disabled = isLoading;
  analyzeButton.textContent = isLoading ? "Analyzing..." : "Analyze";
}

function setBarWidth(element, value) {
  element.style.width = `${Math.round(value * 100)}%`;
}

function renderPrediction(prediction) {
  const negativeProbability = prediction.probabilities.negative;
  const positiveProbability = prediction.probabilities.positive;

  resultLabel.textContent = formatLabel(prediction.label);
  resultConfidence.textContent = formatPercent(prediction.confidence);
  resultNegative.textContent = formatPercent(negativeProbability);
  resultPositive.textContent = formatPercent(positiveProbability);
  negativeBarValue.textContent = formatPercent(negativeProbability);
  positiveBarValue.textContent = formatPercent(positiveProbability);
  setBarWidth(negativeBar, negativeProbability);
  setBarWidth(positiveBar, positiveProbability);
  resultPanel.hidden = false;
}

async function loadModelStatus() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/model-info`);
    const modelInfo = await response.json();
    modelStatus.textContent = `Model status: ${modelInfo.status}`;
    modelDetail.textContent = `${modelInfo.tokenizer} + ${modelInfo.vectorizer} + ${modelInfo.model}`;
  } catch {
    modelStatus.textContent = "Model status: backend unavailable";
    modelDetail.textContent = "Start the FastAPI server and refresh this page.";
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
    clearResult();
    return;
  }

  if (!containsKorean(text)) {
    setMessage("한글 리뷰를 입력해 주세요.");
    clearResult();
    return;
  }

  try {
    setLoading(true);
    const prediction = await requestPrediction(text);
    renderPrediction(prediction);
  } catch (error) {
    clearResult();
    setMessage(error.message);
  } finally {
    setLoading(false);
  }
});

sampleButtons.forEach((button) => {
  button.addEventListener("click", () => {
    reviewText.value = button.dataset.sample;
    reviewText.focus();
    setMessage("");
    clearResult();
  });
});

loadModelStatus();
