function previewText(text, words = 8) {
    const toks = text.trim().split(/\s+/);
    if (toks.length <= words) return text;
    return toks.slice(0, words).join(" ") + "…";
}

//define all divs in html
const title = document.getElementById("title");
const body = document.getElementById("body");
const inboxList = document.getElementById("inboxList");
const popuphaze = document.getElementById("popuphaze");
const popupPrev = document.getElementById("popupPrev");
const popupText = document.getElementById("popupText");
const popupFreq = document.getElementById("popupFreq");
const closePopup = document.getElementById("closePopup");

//x out of popup
closePopup.addEventListener("click", () => hideModal());
popuphaze.addEventListener("click", (e) => { if (e.target === popuphaze) hideModal(); });

//function to find peak frequency for male/female detection
function getPeakFrequency(frequencies, magnitudes) {
    let peakIdx = 0;
    let maxMag = -1;
    for (let i = 0; i < magnitudes.length; i++) {
        if (magnitudes[i] > maxMag) {
            maxMag = magnitudes[i];
            peakIdx = i;
        }
    }
    return frequencies[peakIdx];
}
//classifying voice
function maleOrFemale(frequency) {
    if (frequency < 140) return "Male";
    else return "Female";
}

let chart = null;

function showModal(entry) {
    popupPrev.textContent = entry.text.split(/\s+/).slice(0, 6).join(" ") + (entry.text.split(/\s+/).length > 6 ? "…" : "");
    popupText.textContent = entry.text;

    const ctx = document.getElementById("popupChart").getContext("2d");

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: entry.frequencies,
            datasets: [{
                label: 'Relative Magnitude',
                data: entry.magnitudes,
                backgroundColor: 'rgba(0, 0, 255, 0.5)',
                borderColor: 'rgba(0, 0, 255, 1)',
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
                    max: 600,
                    title: { display: true, text: 'Frequency (Hz)' }
                }
            }
        }
    });
    let peakFreq = getPeakFrequency(entry.frequencies, entry.magnitudes);
    let voiceType = maleOrFemale(peakFreq);

    popupFreq.textContent = `Peak: ${peakFreq} Hz (${voiceType})`;

    popuphaze.style.display = "flex";
    popuphaze.setAttribute("aria-hidden", "false");
}


function hideModal() {
    popuphaze.style.display = "none";
    popuphaze.setAttribute("aria-hidden", "true");
}

let latestChart = null;

//rendering site
async function fetchDataAndRender() {
    try {
        const resp = await fetch("/data", { cache: "no-store" });
        if (!resp.ok) throw new Error("Network response was not ok");
        const data = await resp.json();


        if (!Array.isArray(data) || data.length == 0) {
            title.textContent = "No entries yet";
            body.textContent = "";
            inboxList.innerHTML = "<div class='empty'>No entries yet.</div>";
            return;
        }

        const latest = data[data.length - 1];

        title.textContent = previewText(latest.text, 40);
        body.textContent = latest.text;

        const latestCtx = document.getElementById("latestSpectrum").getContext("2d");

            if (latestChart) {
                latestChart.destroy();
            }

            latestChart = new Chart(latestCtx, {
                type: 'bar',
                data: {
                    labels: latest.frequencies,
                    datasets: [{
                        label: 'Magnitude',
                        data: latest.magnitudes,
                        backgroundColor: 'rgba(0, 0, 255, 0.5)',
                        borderColor: 'rgba(0, 0, 255, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: { beginAtZero: true, title: { display: true, text: 'Magnitude' } },
                        x: { type: 'linear', min: 0, max: 600, title: { display: true, text: 'Frequency (Hz)' } }
                    }
                }
            });
        //reverse entries so that newest appears first
        const reversed = data.slice().reverse();
        let html = "";

        reversed.forEach((entry, idx) => {
            const preview = previewText(entry.text, 8);
            const originalIndex = data.length - idx -1;
            html += `
        <div class="item" data-index="${originalIndex}" tabindex="0" role="button">
          <div>
            <div class="preview">${preview}</div>
          </div>
          <div class="index">${originalIndex+1}</div>
        </div>
      `;
        });

        inboxList.innerHTML = html;

        document.querySelectorAll(".item").forEach(el => {
            el.addEventListener("click", () => showModal(data[parseInt(el.getAttribute("data-index"))]));
        });


    } catch (err) {
        console.error("Failed to fetch /data:", err);
    }
}

//render site
fetchDataAndRender();

// update site every second
setInterval(fetchDataAndRender, 1000);