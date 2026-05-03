/* ───── Yıldız Oluştur ───────────────────────────────────────────────────── */
(function generateStars() {
  const container = document.getElementById("stars");
  const N = 140;
  for (let i = 0; i < N; i++) {
    const s = document.createElement("div");
    s.className = "star";
    const size = Math.random() * 2.5 + 0.5;
    s.style.cssText = [
      `width:${size}px`, `height:${size}px`,
      `top:${Math.random() * 85}%`,
      `left:${Math.random() * 100}%`,
      `--dur:${(Math.random() * 3 + 2).toFixed(1)}s`,
      `--delay:${(Math.random() * 4).toFixed(1)}s`,
    ].join(";");
    container.appendChild(s);
  }
})();

/* ───── Element Referansları ─────────────────────────────────────────────── */
const form       = document.getElementById("predForm");
const submitBtn  = document.getElementById("submitBtn");
const btnLabel   = submitBtn.querySelector(".btn-label");
const btnIcon    = submitBtn.querySelector(".btn-icon");
const spinner    = document.getElementById("spinner");

const formCard   = document.getElementById("formCard");
const resultCard = document.getElementById("resultCard");
const resultIcon = document.getElementById("resultIcon");
const resultTitle= document.getElementById("resultTitle");
const resultSub  = document.getElementById("resultSub");
const probFill   = document.getElementById("probFill");
const probPct    = document.getElementById("probPct");
const retryBtn   = document.getElementById("retryBtn");

/* ───── Form Gönderimi ───────────────────────────────────────────────────── */
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  // Validasyon
  if (!validateForm()) return;

  // Loading durumu
  setLoading(true);

  const data = {
    pclass:   parseInt(getValue("pclass")),
    sex:      parseInt(getRadio("sex")),
    age:      parseFloat(getValue("age")),
    sibsp:    parseInt(getValue("sibsp")),
    parch:    parseInt(getValue("parch")),
    fare:     parseFloat(getValue("fare")),
    embarked: parseInt(getRadio("embarked")),
  };

  try {
    const res  = await fetch("/predict", {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify(data),
    });

    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const result = await res.json();
    showResult(result);

  } catch (err) {
    alert("❌ Sunucuya bağlanılamadı. Lütfen main.py'nin çalıştığından emin olun.\n\n" + err);
  } finally {
    setLoading(false);
  }
});

/* ───── Tekrar Dene ──────────────────────────────────────────────────────── */
retryBtn.addEventListener("click", () => {
  resultCard.classList.add("hidden");
  formCard.classList.remove("hidden");
  probFill.style.width = "0";
});

/* ───── Sonucu Göster ────────────────────────────────────────────────────── */
function showResult(result) {
  const survived = result.survived;
  const prob     = result.probability;  // 0–100

  resultIcon.textContent = survived ? "🌊✨" : "🌊💀";

  resultTitle.textContent = survived ? "Hayatta Kaldı!" : "Hayatta Kalamadı";
  resultTitle.className   = "result-title " + (survived ? "survived" : "died");

  resultSub.textContent = survived
    ? `Bu yolcu için hayatta kalma olasılığı: %${prob}`
    : `Bu yolcu için hayatta kalma olasılığı yalnızca: %${prob}`;

  probFill.className = "prob-bar-fill " + (survived ? "survived" : "died");
  probPct.textContent = `%${prob}`;
  probPct.style.color = survived ? "var(--green)" : "var(--red)";

  // Form gizle, result göster
  formCard.classList.add("hidden");
  resultCard.classList.remove("hidden");

  // Bar animasyonu (küçük gecikmeyle başlat)
  requestAnimationFrame(() => {
    setTimeout(() => { probFill.style.width = prob + "%"; }, 100);
  });
}

/* ───── Validasyon ───────────────────────────────────────────────────────── */
function validateForm() {
  let ok = true;

  const checks = [
    { id: "field-pclass",   val: getValue("pclass") },
    { id: "field-sex",      val: getRadio("sex") },
    { id: "field-age",      val: getValue("age") },
    { id: "field-fare",     val: getValue("fare") },
    { id: "field-embarked", val: getRadio("embarked") },
  ];

  checks.forEach(({ id, val }) => {
    const el = document.getElementById(id);
    if (val === null || val === "" || val === undefined) {
      el.classList.add("error");
      ok = false;
    } else {
      el.classList.remove("error");
    }
  });

  return ok;
}

/* ───── Loading Durumu ───────────────────────────────────────────────────── */
function setLoading(on) {
  submitBtn.disabled = on;
  btnLabel.textContent = on ? "Hesaplanıyor…" : "Tahmini Hesapla";
  btnIcon.classList.toggle("hidden", on);
  spinner.classList.toggle("hidden", !on);
}

/* ───── Yardımcı Fonksiyonlar ────────────────────────────────────────────── */
function getValue(id) {
  return document.getElementById(id)?.value ?? "";
}

function getRadio(name) {
  const el = document.querySelector(`input[name="${name}"]:checked`);
  return el ? el.value : null;
}

/* ───── Error Temizleme ──────────────────────────────────────────────────── */
document.querySelectorAll("input, select").forEach((el) => {
  el.addEventListener("change", () => {
    el.closest(".field")?.classList.remove("error");
  });
});
