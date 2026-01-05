const API_URL = "http://127.0.0.1:8000/predict";

window.onload = () => {
  scanCurrentPage();
};

function scanCurrentPage() {
  const riskText = document.getElementById("riskText");
  const progressFill = document.getElementById("progressFill");
  const findings = document.getElementById("findings");

  riskText.innerText = "🔄 Scanning current page…";
  findings.innerHTML = "";
  progressFill.style.width = "0%";

  chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
    const tab = tabs[0];
    const url = tab.url;

    /* ---------- PAGE CONTEXT SCAN ---------- */
    chrome.scripting.executeScript(
      {
        target: { tabId: tab.id },
        func: pageAnalysis
      },
      (results) => {
        const pageData = results[0].result;

        if (url.includes("mail.google.com")) {
          findings.innerHTML += "<li>📧 Gmail environment detected</li>";
        }

        if (pageData.hasPassword) {
          findings.innerHTML += "<li>🔐 Password field detected</li>";
        }

        if (pageData.hasForms) {
          findings.innerHTML += "<li>📄 Form submission detected</li>";
        }

        /* ---------- CALL ML API ---------- */
        fetch(API_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ url })
        })
        .then(res => res.json())
        .then(data => {
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
            findings.innerHTML += "<li>⚠ Login-related keywords</li>";
          } else {
            findings.innerHTML += "<li>✅ No major phishing indicators</li>";
          }

          /* ---------- VISUAL LINK HIGHLIGHTING ---------- */
          if (score > 60) {
            chrome.scripting.executeScript({
              target: { tabId: tab.id },
              func: highlightSuspiciousLinks
            });
          }

          /* ---------- STRONG WARNING ---------- */
          if (score > 75) {
            alert("🚨 WARNING: High-risk phishing page detected!");
          }
        })
        .catch(() => {
          riskText.innerText = "❌ Scan failed";
        });
      }
    );
  });
}

/* ---------- PAGE ANALYSIS FUNCTION ---------- */
function pageAnalysis() {
  return {
    hasPassword: document.querySelectorAll("input[type='password']").length > 0,
    hasForms: document.querySelectorAll("form").length > 0
  };
}

/* ---------- LINK HIGHLIGHTING FUNCTION ---------- */
function highlightSuspiciousLinks() {
  document.querySelectorAll("a").forEach(link => {
    if (
      link.href.includes("login") ||
      link.href.includes("verify") ||
      link.href.includes("secure")
    ) {
      link.style.border = "2px solid red";
      link.title = "Potential phishing link";
    }
  });
}

