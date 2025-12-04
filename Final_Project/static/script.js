function escapeHtml(s) {
  if (!s && s !== 0) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function previewText(text, words=8) {
  const toks = text.trim().split(/\s+/);
  if (toks.length <= words) return escapeHtml(text);
  return escapeHtml(toks.slice(0, words).join(" ")) + "…";
}

const latestTitle = document.getElementById("latestTitle");
const latestBody = document.getElementById("latestBody");
const latestMeta = document.getElementById("latestMeta");
const inboxList = document.getElementById("inboxList");
const emptyMsg = document.getElementById("emptyMsg");
const lastUpdated = document.getElementById("lastUpdated");

const modalBackdrop = document.getElementById("modalBackdrop");
const modalTitle = document.getElementById("modalTitle");
const modalBody = document.getElementById("modalBody");
const modalFreq = document.getElementById("modalFreq");
const modalClose = document.getElementById("modalClose");

modalClose.addEventListener("click", () => hideModal());
modalBackdrop.addEventListener("click", (e) => { if (e.target === modalBackdrop) hideModal(); });

let spectrumChart = null;
function getPeakFrequency(frequencies, magnitudes) {
    if (!frequencies || !magnitudes || frequencies.length !== magnitudes.length) return null;
    let peakIdx = 0;
    let maxMag = -Infinity;
    for (let i = 0; i < magnitudes.length; i++) {
        if (magnitudes[i] > maxMag) {
            maxMag = magnitudes[i];
            peakIdx = i;
        }
    }
    return frequencies[peakIdx];
}
function classifyVoice(frequency) {
    if (frequency < 165) return "Male";
    else if (frequency < 255) return "Female";
    else return "Unknown";
}


function showModal(entry) {
    modalTitle.textContent = entry.text.split(/\s+/).slice(0,6).join(" ") + (entry.text.split(/\s+/).length>6?"…":"");
    modalBody.textContent = entry.text;

    const ctx = document.getElementById("modalSpectrum").getContext("2d");

    if(entry.frequencies && entry.magnitudes 
       && Array.isArray(entry.frequencies) && Array.isArray(entry.magnitudes)) {
        
        modalFreq.textContent = "Frequency Spectrum";

        // Destroy old chart
        if(spectrumChart) spectrumChart.destroy();

        spectrumChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: entry.frequencies,   // x-axis = frequencies
                datasets: [{
                    label: 'Relative Magnitude',
                    data: entry.magnitudes,  // y-axis = magnitudes
                    backgroundColor: 'rgba(54, 162, 235, 0.5)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        title: { display: true, text: 'Relative Magnitude' }
                    },
                    x: {
                        type: 'linear',
                        min: 0,
                        max: 300,
                        title: { display: true, text: 'Frequency (Hz)' }
                    }
                }
            }
        });

    } else {
        modalFreq.textContent = "Frequency: " + entry.frequency + " Hz";
        if(spectrumChart) spectrumChart.destroy();
    }
    let peakFreq = getPeakFrequency(entry.frequencies, entry.magnitudes);
    let voiceType = peakFreq ? classifyVoice(peakFreq) : "Unknown";

    modalFreq.textContent = `Peak: ${peakFreq ? peakFreq.toFixed(1) : "N/A"} Hz (${voiceType})`;

    modalBackdrop.style.display = "flex";
    modalBackdrop.setAttribute("aria-hidden","false");
}


function hideModal() {
  modalBackdrop.style.display = "none";
  modalBackdrop.setAttribute("aria-hidden", "true");
}

let lastSeenLen = 0;
let latestChart = null;

async function fetchDataAndRender() {
  try {
    const resp = await fetch("/data", {cache: "no-store"});
    if (!resp.ok) throw new Error("Network response was not ok");
    const data = await resp.json();

    lastUpdated.textContent = "Updated: " + new Date().toLocaleTimeString();

    if (!Array.isArray(data) || data.length === 0) {
      emptyMsg.style.display = "block";
      latestTitle.textContent = "No entries yet";
      latestBody.textContent = "";
      latestMeta.textContent = "";
      inboxList.innerHTML = "<div class='empty' id='emptyMsg'>No entries yet.</div>";
      lastSeenLen = 0;
      return;
    }

    emptyMsg.style.display = "none";

    const latest = data[data.length - 1];

   latestTitle.textContent = previewText(latest.text, 40);
        latestBody.textContent = latest.text;
        latestMeta.textContent = "Frequency Spectrum";

        // Render latest entry chart as a bar chart
        const latestCtx = document.getElementById("latestSpectrum").getContext("2d");
        if(latest.frequencies && latest.magnitudes &&
           Array.isArray(latest.frequencies) && Array.isArray(latest.magnitudes)) {

            if(latestChart) latestChart.destroy();

            latestChart = new Chart(latestCtx, {
                type: 'bar', // <-- bar chart for latest entry
                data: {
                    labels: latest.frequencies,
                    datasets: [{
                        label: 'Magnitude',
                        data: latest.magnitudes,
                        backgroundColor: 'rgba(54, 162, 235, 0.5)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Magnitude' } },
                        x: { type: 'linear', min: 0, max: 300, title: { display: true, text: 'Frequency (Hz)' } }
                    }
                }
            });

        } else {
            if(latestChart) latestChart.destroy();
        }
    const reversed = data.slice().reverse();
    let html = "";

    reversed.forEach((entry, idx) => {
      const preview = previewText(entry.text, 8);
      const originalIndex = data.length - 1 - idx;
      html += `
        <div class="item" data-index="${originalIndex}" tabindex="0" role="button">
          <div>
            <div class="preview">${preview}</div>
          </div>
          <div class="timestamp">#${originalIndex}</div>
        </div>
      `;
    });

    inboxList.innerHTML = html;

    document.querySelectorAll(".item").forEach(el => {
      el.addEventListener("click", () => showModal(data[parseInt(el.getAttribute("data-index"))]));
      el.addEventListener("keydown", ev => {
        if (ev.key === "Enter" || ev.key === " ") {
          ev.preventDefault();
          showModal(data[parseInt(el.getAttribute("data-index"))]);
        }
      });
    });

    lastSeenLen = data.length;

  } catch (err) {
    console.error("Failed to fetch /data:", err);
    lastUpdated.textContent = "Error fetching data";
  }
}

fetchDataAndRender();
setInterval(fetchDataAndRender, 1000);

