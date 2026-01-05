const API_URL = "https://phishing-plugin-3.onrender.com/predict";

window.onload = () => {
  scanCurrentPage();
};

function scanCurrentPage() {
  const riskText = document.getElementById("riskText");
  const progressFill = document.getElementById("progressFill");
  const findings = document.getElementById("findings");

  riskText.innerText = "🔄 Scanning current page…";
  progressFill.style.width = "0%";
  findings.innerHTML = "";

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    if (!tabs || !tabs.length) {
      riskText.innerText = "❌ No active tab";
      return;
    }

    const tab = tabs[0];
    const url = tab.url;

    // 🚫 Chrome internal pages
    if (!url || url.startsWith("chrome://")) {
      riskText.innerText = "⚠ Cannot scan this page";
      return;
    }

    // Gmail detection (NO executeScript here)
    if (url.includes("mail.google.com")) {
      findings.innerHTML += "<li>📧 Gmail environment detected</li>";
      findings.innerHTML += "<li>📄 Form submission detected</li>";
    }

    // ---------- API CALL ----------
    fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url })
    })
      .then(res => res.json())
      .then(data => {
        console.log("API RESPONSE:", data);

        if (data.error) {
          riskText.innerText = "❌ ML error";
          findings.innerHTML += `<li>${data.error}</li>`;
          return;
        }

        const score = Math.round(data.confidence * 100);

        let risk = "LOW";
        let color = "#22c55e";

        if (score > 70) {
          risk = "HIGH";
          color = "#ef4444";
        } else if (score > 40) {
          risk = "MEDIUM";
          color = "#facc15";
        }

        riskText.innerText = `${risk} RISK (${score}%)`;
        riskText.style.color = color;
        progressFill.style.width = score + "%";

        if (score > 40) {
          findings.innerHTML += "<li>⚠ Suspicious URL structure</li>";
        } else {
          findings.innerHTML += "<li>✅ No major phishing indicators</li>";
        }

        if (score > 75) {
          alert("🚨 WARNING: High-risk phishing page detected!");
        }
      })
      .catch(err => {
        console.error("FETCH FAILED:", err);
        riskText.innerText = "❌ Scan failed";
        findings.innerHTML += "<li>API unreachable</li>";
      });
  });
}
