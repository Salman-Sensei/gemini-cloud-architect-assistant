async function submitPrompt() {
  const promptInput = document.getElementById("prompt");
  const submitBtn = document.getElementById("submit-btn");
  const loading = document.getElementById("loading");
  const responseContainer = document.getElementById("response-container");
  const responseText = document.getElementById("response-text");
  const errorContainer = document.getElementById("error-container");
  const errorText = document.getElementById("error-text");

  const prompt = promptInput.value.trim();

  if (!prompt) {
    errorText.textContent = "Please enter a question or prompt.";
    errorContainer.classList.remove("hidden");
    return;
  }

  errorContainer.classList.add("hidden");
  responseContainer.classList.add("hidden");
  loading.classList.remove("hidden");
  submitBtn.disabled = true;

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: prompt })
    });

    const data = await response.json();

    if (response.ok && data.status === "success") {
      responseText.innerText = data.response;
      responseContainer.classList.remove("hidden");
    } else {
      errorText.textContent = data.message || "An error occurred during request processing.";
      errorContainer.classList.remove("hidden");
    }
  } catch (err) {
    errorText.textContent = "Failed to connect to backend server: " + err.message;
    errorContainer.classList.remove("hidden");
  } finally {
    loading.classList.add("hidden");
    submitBtn.disabled = false;
  }
}
