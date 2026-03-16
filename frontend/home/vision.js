// ═══════════════ CONFIG ═══════════════
const BACKEND_URL = window.location.origin;

// ═══════════════ STATE ═══════════════
let currentFile = null, webcamStream = null, activeDish = null;
let recipeSteps = [], currentStep = 0, timerInterval = null, timerRemaining = 0;
let isMuted = false;

// ═══════════════ TTS ═══════════════
function speak(text) {
  if (isMuted || !window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = 0.92;
  utter.pitch = 1.0;
  // Prefer a natural voice
  const voices = window.speechSynthesis.getVoices();
  const preferred = voices.find(v => v.lang === 'en-IN') ||
    voices.find(v => v.lang.startsWith('en') && v.localService) ||
    voices[0];
  if (preferred) utter.voice = preferred;
  window.speechSynthesis.speak(utter);
}

function stopSpeech() {
  if (window.speechSynthesis) window.speechSynthesis.cancel();
}

// ═══════════════ DOM ═══════════════
const $ = id => document.getElementById(id);
const fileInput = $('fileInput'), previewContainer = $('previewContainer');
const inputPlaceholder = $('inputPlaceholder');
const previewImg = $('previewImg'), previewName = $('previewName'), previewSize = $('previewSize');
const analyzeBtn = $('analyzeBtn'), clearBtn = $('clearBtn'), loader = $('loader');
const resultsContainer = $('resultsContainer'), resultsEl = $('results'), errorBox = $('errorBox');
const newAnalysisBtn = $('newAnalysisBtn'), feedbackMsg = $('feedbackMsg'), placeholderText = $('placeholderText');
const drawerOverlay = $('drawerOverlay'), dishDrawer = $('dishDrawer');
const drawerClose = $('drawerClose'), drawerClose2 = $('drawerClose2'), startCookingBtn = $('startCookingBtn');
const recipeModal = $('recipeModal'), recipeClose = $('recipeClose');
const prevBtn = $('prevBtn'), nextBtn = $('nextBtn'), repeatBtn = $('repeatBtn'), jumpBtn = $('jumpBtn');
const jumpModal = $('jumpModal'), jumpClose = $('jumpClose');
const webcamModal = $('webcamModal'), webcamBtn = $('webcamBtn'), webcamVideo = $('webcamVideo');
const captureBtn = $('captureBtn'), closeWebcamBtn = $('closeWebcamBtn');
const visionServings = $('visionServings');

// Load voices once they're available
if (window.speechSynthesis) window.speechSynthesis.onvoiceschanged = () => window.speechSynthesis.getVoices();

// ═══════════════ UPLOAD ═══════════════
fileInput.addEventListener('change', e => { if (e.target.files[0]) loadFile(e.target.files[0]) });

function loadFile(file) {
  currentFile = file;
  previewImg.src = URL.createObjectURL(file);
  previewName.textContent = file.name;
  previewSize.textContent = `${(file.size / 1024).toFixed(1)} KB`;
  previewContainer.classList.add('show');
  inputPlaceholder.classList.add('hidden');
  feedbackMsg.textContent = 'Great! Hit 🔍 Detect to analyse your image.';
  hideResults();
}

clearBtn.addEventListener('click', resetAll);
newAnalysisBtn.addEventListener('click', resetAll);

function resetAll() {
  currentFile = null;
  fileInput.value = '';
  previewContainer.classList.remove('show');
  inputPlaceholder.classList.remove('hidden');
  feedbackMsg.textContent = "What's in your kitchen today?";
  placeholderText.style.display = '';
  hideResults();
}

// ═══════════════ ANALYZE ═══════════════
analyzeBtn.addEventListener('click', () => {
  if (!currentFile) return;
  const fd = new FormData();
  fd.append('image', currentFile);
  runDetection(BACKEND_URL + '/detect', fd);
});

function runDetection(endpoint, body) {
  hideResults();
  showError('');
  loader.style.display = 'block';
  feedbackMsg.textContent = 'Analysing\u2026 this will take a moment \uD83D\uDD0D';

  const controller = new AbortController();
  // 120 s timeout — the multi-model pipeline can be slow
  const timer = setTimeout(() => controller.abort(), 120000);

  const opts = typeof body === 'string'
    ? { method: 'POST', headers: { 'Content-Type': 'application/json' }, body, signal: controller.signal }
    : { method: 'POST', body, signal: controller.signal };

  fetch(endpoint, opts)
    .then(async r => {
      clearTimeout(timer);
      if (!r.ok) {
        let t = await r.text();
        try { t = JSON.parse(t).error || t; } catch (e) { }
        throw new Error(t || `Server error ${r.status}`);
      }
      return r.json();
    })
    .then(data => {
      loader.style.display = 'none';
      if (data.error) { showError(data.error); return; }
      renderResults(data);
    })
    .catch(err => {
      clearTimeout(timer);
      loader.style.display = 'none';
      if (err.name === 'AbortError') {
        showError('Detection timed out (>2 min). Try a smaller image.');
      } else {
        showError('Detection failed: ' + err.message);
      }
      feedbackMsg.textContent = 'Something went wrong. Please try again.';
    });
}

// ═══════════════ RENDER ═══════════════
function renderResults(data) {
  try {
    console.log("Rendering results with data:", data);
    const ms = data.model_stats || {};

    $('statYolo').textContent = ms.yolo_detections ?? '—';
    $('statEffnet').textContent = ms.efficientnet_detections ?? '—';
    $('statMobile').textContent = ms.mobilenet_detections ?? '—';
    $('statResnet').textContent = ms.resnet_detections ?? '—';
    $('statColor').textContent = ms.color_detections ?? '—';
    $('statTotal').textContent = data.total_found ?? 0;
    $('itemCountBadge').textContent = `${data.total_found ?? 0} found`;
    $('timeBadge').textContent = `⏱ ${data.processing_time ?? 0}s`;

    if (data.annotated_url) {
      let url = data.annotated_url;
      if (!url.startsWith('http')) url = BACKEND_URL + url;
      $('annotatedImg').src = url + '?t=' + Date.now();
    }

    const grid = $('ingredientGrid');
    grid.innerHTML = '';
    const ingredients = data.ingredients || [];

    if (ingredients.length === 0) {
      grid.innerHTML = '<div style="color:white;padding:1rem;grid-column:1/-1;text-align:center;">No specific ingredients identified.</div>';
    } else {
      ingredients.forEach((item, i) => {
        const multi = (item.model_count || 0) > 1, pct = Math.round((item.confidence || 0) * 100);
        const card = document.createElement('div');
        card.className = 'ingredient-card' + (multi ? ' multi' : '');
        card.style.animationDelay = (i * 55) + 'ms';
        card.innerHTML = `
          <div class="ing-name">${item.name || 'Unknown'}</div>
          <div class="ing-cat">${item.category || 'Food'}</div>
          <div class="conf-wrap">
            <div class="conf-bar ${multi ? 'amber' : ''}" style="width:0%" data-w="${pct}%"></div>
          </div>
          <div class="conf-lbl">
            <span>${multi ? '⭐ Multi-model' : 'Single model'}</span>
            <span>${pct}%</span>
          </div>
          <div class="model-tags">${(item.sources || []).map(s => `<span class="model-tag">${s}</span>`).join('')}</div>
          ${item.nutrition ? `<div class="nut-text">${item.nutrition}</div>` : ''}
        `;
        grid.appendChild(card);
        setTimeout(() => {
          const bar = card.querySelector('.conf-bar');
          if (bar) bar.style.width = pct + '%';
        }, 80 + i * 55);
      });
    }

    const dg = $('dishesGrid');
    dg.innerHTML = '<div style="color:white;padding:1rem;">Finding recipes...</div>';
    feedbackMsg.textContent = 'Here are your results! Finding recipes...';

    const detectedNames = ingredients.map(i => (i.name || '').toLowerCase()).filter(n => n);

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);

    fetch(`${BACKEND_URL}/suggest-recipes`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ingredients: detectedNames }),
      signal: controller.signal
    })
      .then(r => r.json())
      .then(recipes => {
        clearTimeout(timeout);
        dg.innerHTML = '';
        if (recipes && recipes.length > 0) {
          feedbackMsg.textContent = 'Results ready! Click any dish to explore 🍛';
          recipes.forEach((r, i) => {
            const card = document.createElement('div');
            card.className = 'dish-card indian-badge';
            card.style.animationDelay = (i * 70) + 'ms';
            card.innerHTML = `<span class="dish-emoji">🍽️</span><div class="dish-name">${r.name}</div><div class="dish-hint">View Details</div>`;
            card.addEventListener('click', () => openDishDrawer(r.name, r.index));
            dg.appendChild(card);
          });
        } else {
          dg.innerHTML = '<div style="color:white;padding:1rem;">No matching recipes found based on detections.</div>';
          feedbackMsg.textContent = 'Detection complete, but no recipes matched.';
        }
      })
      .catch(e => {
        clearTimeout(timeout);
        console.error("Error fetching recipes:", e);
        if (e.name === 'AbortError') {
          dg.innerHTML = '<div style="color:white;padding:1rem;">Recipe search timed out. Processing is slow.</div>';
        } else {
          dg.innerHTML = '<div style="color:white;padding:1rem;">Could not load recipes (Network Error).</div>';
        }
      });

    const nl = $('nutritionList');
    nl.innerHTML = '';
    (data.nutrition_summary || []).forEach((n, i) => {
      const ingr = ingredients[i];
      const el = document.createElement('div');
      el.className = 'nutrition-item';
      el.innerHTML = ingr ? `<strong>${ingr.name || 'Ingredient'}</strong>${n}` : n;
      nl.appendChild(el);
    });

    placeholderText.style.display = 'none';
    loader.style.display = 'none';
    resultsEl.style.display = 'block';
    resultsEl.scrollIntoView({ behavior: 'smooth', block: 'start' });

  } catch (err) {
    console.error("Critical error in renderResults:", err);
    loader.style.display = 'none';
    showError("Rendering error: " + err.message);
  }
}

// ═══════════════ DRAWER ═══════════════
async function openDishDrawer(name, recipeIndex) {
  $('drawerTitle').textContent = '🍽️ ' + name;
  $('drawerSubtitle').textContent = 'Loading...';
  $('drawerChips').innerHTML = '';
  $('drawerAbout').textContent = '';
  $('drawerIngredients').innerHTML = '<span style="color:white">Loading ingredients...</span>';
  $('drawerTips').innerHTML = '';
  drawerOverlay.classList.add('open');
  dishDrawer.classList.add('open');
  document.body.style.overflow = 'hidden';

  activeDish = { name: name, info: { steps: [] } }; // Temp state

  const servings = visionServings ? parseInt(visionServings.value) || 2 : 2;

  try {
    // First try loading by name from the database (Vision Chef)
    let data = null;
    const byNameRes = await fetch(`${BACKEND_URL}/start-cooking-by-name`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ recipe_name: name, servings })
    });
    if (byNameRes.ok) {
      data = await byNameRes.json();
    } else if (recipeIndex != null) {
      // Fallback: load by index
      const idxRes = await fetch(`${BACKEND_URL}/start-cooking`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recipe_index: recipeIndex, servings })
      });
      if (idxRes.ok) data = await idxRes.json();
    }

    if (!data) throw new Error('Recipe not available');

    const stepsObj = data.steps.map((s, i) => ({ title: `Step ${i + 1}`, body: s }));
    activeDish = { name: data.name, info: { steps: stepsObj } };

    $('drawerSubtitle').textContent = `${servings} serving${servings > 1 ? 's' : ''}`;
    $('drawerChips').innerHTML = `<span class="chip chip-green">👥 Serves ${servings}</span>`;
    $('drawerAbout').textContent = `Enjoy this delicious ${data.name} made with fresh ingredients. Click Start Cooking to view step-by-step instructions.`;

    let ingsHtml = Object.entries(data.ingredients || {}).map(([ing, qty]) => `<span class="ing-pill">${qty} ${ing}</span>`).join('');
    $('drawerIngredients').innerHTML = ingsHtml || '<span style="color:white">No ingredients listed</span>';

    // ── Render nutrition info ──────────────────────────────
    const nut = data.nutrition || {};
    const ingNut = data.ingredient_nutrition || {};
    const nutSection = $('drawerNutritionSection');
    const nutSummary = $('drawerNutSummary');
    const nutIngredients = $('drawerIngNutrition');

    if (nut.calories || Object.keys(ingNut).length > 0) {
      nutSection.style.display = '';

      // Recipe-level nutrition summary
      if (nut.calories || nut.protein || nut.carbs || nut.fat) {
        nutSummary.innerHTML = `
          <div class="drawer-nut-stats">
            ${nut.calories ? `<div class="drawer-nut-item"><span class="drawer-nut-val">${nut.calories}</span><span class="drawer-nut-lbl">kcal</span></div>` : ''}
            ${nut.protein ? `<div class="drawer-nut-item"><span class="drawer-nut-val">${nut.protein}g</span><span class="drawer-nut-lbl">Protein</span></div>` : ''}
            ${nut.carbs ? `<div class="drawer-nut-item"><span class="drawer-nut-val">${nut.carbs}g</span><span class="drawer-nut-lbl">Carbs</span></div>` : ''}
            ${nut.fat ? `<div class="drawer-nut-item"><span class="drawer-nut-val">${nut.fat}g</span><span class="drawer-nut-lbl">Fat</span></div>` : ''}
          </div>`;
      } else {
        nutSummary.innerHTML = '';
      }

      // Per-ingredient nutrition
      let ingNutHtml = '';
      for (const [item, info] of Object.entries(ingNut)) {
        const cal = info.calories_per_100g;
        const vitamins = info.key_vitamins || {};
        const topVits = Object.entries(vitamins).slice(0, 3);
        ingNutHtml += `<div class="drawer-ing-nut-card">
          <div class="drawer-ing-nut-name">${item}</div>
          <div class="drawer-ing-nut-details">
            ${cal != null ? `<span class="drawer-nut-cal">🔥 ${cal} kcal/100g</span>` : ''}
            ${topVits.map(([v, a]) => `<span class="drawer-nut-vit">${v}: ${a}</span>`).join('')}
          </div>
        </div>`;
      }
      nutIngredients.innerHTML = ingNutHtml;

      // Voice narration of nutrition
      let nutSpeech = '';
      if (nut.calories) {
        nutSpeech = `This recipe has ${nut.calories} calories`;
        if (nut.protein) nutSpeech += `, ${nut.protein} grams of protein`;
        nutSpeech += '.';
      }
      if (nutSpeech) setTimeout(() => speak(nutSpeech), 500);
    } else {
      nutSection.style.display = 'none';
    }
  } catch (e) {
    console.error(e);
    $('drawerSubtitle').textContent = 'Recipe details loading from AI suggestions';
    $('drawerIngredients').innerHTML = '<span style="color:var(--text-muted,#aaa)">This dish\'s full recipe will load when you start cooking.</span>';
    $('drawerAbout').textContent = `Enjoy ${name}! Click Start Cooking to see the full step-by-step instructions.`;
    $('drawerChips').innerHTML = `<span class="chip chip-green">👥 Serves ${servings}</span>`;
    if ($('drawerNutritionSection')) $('drawerNutritionSection').style.display = 'none';
  }
}

// Re-open drawer with updated servings when selector changes
if (visionServings) {
  visionServings.addEventListener('change', () => {
    if (activeDish && dishDrawer.classList.contains('open')) {
      openDishDrawer(activeDish.name, null);
    }
  });
}

function closeDishDrawer() {
  dishDrawer.classList.remove('open');
  drawerOverlay.classList.remove('open');
  document.body.style.overflow = '';
  stopSpeech();
}

drawerClose.addEventListener('click', closeDishDrawer);
drawerClose2.addEventListener('click', closeDishDrawer);
drawerOverlay.addEventListener('click', closeDishDrawer);

// ═══════════════ RECIPE MODAL ═══════════════
startCookingBtn.addEventListener('click', () => {
  if (!activeDish) return;
  closeDishDrawer();
  openRecipeModal(activeDish.name, activeDish.info);
});

function openRecipeModal(name, info) {
  recipeSteps = info.steps || []; currentStep = 0; clearTimer();
  $('recipeModalTitle').textContent = '🍽️ ' + name;
  $('recipeModalSub').textContent = `1 serving`;
  buildStepDots(); renderStep(0);
  recipeModal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function buildStepDots() {
  const dots = $('stepDots');
  dots.innerHTML = recipeSteps.map((s, i) => `<div class="step-dot ${i === 0 ? 'active' : ''}" data-i="${i}" title="${s.title}"></div>`).join('');
  dots.querySelectorAll('.step-dot').forEach(d => { d.addEventListener('click', () => goToStep(parseInt(d.dataset.i))) });
}

function renderStep(idx) {
  clearTimer(); currentStep = idx;
  const step = recipeSteps[idx], total = recipeSteps.length;
  $('recipeProgress').style.width = ((idx + 1) / total * 100) + '%';
  $('stepLabel').textContent = `Step ${idx + 1} of ${total}`;
  document.querySelectorAll('.step-dot').forEach((d, i) => { d.classList.remove('active', 'done'); if (i < idx) d.classList.add('done'); else if (i === idx) d.classList.add('active') });
  prevBtn.disabled = idx === 0;
  nextBtn.textContent = idx === total - 1 ? '🎉 Finish!' : 'Next →';
  const hasTimer = !!step.timer;
  const body = $('recipeBody');
  body.innerHTML = `
    <div class="step-num-pill">Step ${idx + 1} <span>of ${total}</span></div>
    <div class="step-title">${step.title}</div>
    <div class="step-body-text">${step.body}</div>
    ${hasTimer ? `<div class="step-timer has-timer"><div><div style="font-size:.72rem;color:var(--muted);margin-bottom:.2rem">⏱ SUGGESTED TIME</div><div class="timer-display" id="timerDisplay">${formatTime(step.timer)}</div></div><div class="timer-btns"><button class="btn btn-saffron btn-sm" id="timerStartBtn">▶ Start</button><button class="btn btn-muted btn-sm" id="timerResetBtn">↺ Reset</button></div></div>` : ''}
    ${step.tip ? `<div class="chef-tip">${step.tip}</div>` : ''}
  `;
  if (hasTimer) {
    timerRemaining = step.timer;
    $('timerStartBtn').addEventListener('click', startTimer);
    $('timerResetBtn').addEventListener('click', () => { clearTimer(); timerRemaining = step.timer; $('timerDisplay').textContent = formatTime(timerRemaining); $('timerStartBtn').textContent = '▶ Start' });
  }
  body.scrollTop = 0;
  // Auto-speak the step
  setTimeout(() => speak(`${step.title}. ${step.body}`), 200);
}

function showCompletion() {
  $('recipeBody').innerHTML = `<div class="completion"><span class="completion-emoji">🎉</span><h2>Dish is ready!</h2><p>You've completed all the steps. Time to plate up, serve, and enjoy! Share it with loved ones. 🍽️</p><div style="margin-top:1.5rem;display:flex;gap:.8rem;justify-content:center;flex-wrap:wrap"><button class="btn btn-saffron" id="restartBtn">🔁 Cook Again</button><button class="btn btn-outline" id="finishCloseBtn">✓ Done</button></div></div>`;
  $('recipeProgress').style.width = '100%';
  $('stepLabel').textContent = `All ${recipeSteps.length} steps done!`;
  $('restartBtn').addEventListener('click', () => { nextBtn.style.display = ''; goToStep(0) });
  $('finishCloseBtn').addEventListener('click', closeRecipeModal);
  nextBtn.style.display = 'none';
  document.querySelectorAll('.step-dot').forEach(d => d.classList.add('done'));
}

function goToStep(idx) { if (idx < 0 || idx > recipeSteps.length) return; nextBtn.style.display = ''; renderStep(idx) }
prevBtn.addEventListener('click', () => goToStep(currentStep - 1));
nextBtn.addEventListener('click', () => { if (currentStep >= recipeSteps.length - 1) showCompletion(); else goToStep(currentStep + 1) });
repeatBtn.addEventListener('click', () => { goToStep(currentStep); speak(recipeSteps[currentStep]?.body || ''); });
jumpBtn.addEventListener('click', () => {
  const list = $('jumpStepList');
  list.innerHTML = recipeSteps.map((s, i) => `<button class="btn btn-sm ${i === currentStep ? 'btn-saffron' : 'btn-outline'}" style="text-align:left;border-radius:10px;justify-content:flex-start" data-i="${i}"><span style="font-weight:700;min-width:22px">${i + 1}.</span>${s.title}</button>`).join('');
  list.querySelectorAll('button').forEach(b => { b.addEventListener('click', () => { goToStep(parseInt(b.dataset.i)); jumpModal.classList.remove('open') }) });
  jumpModal.classList.add('open');
});
jumpClose.addEventListener('click', () => jumpModal.classList.remove('open'));
jumpModal.addEventListener('click', e => { if (e.target === jumpModal) jumpModal.classList.remove('open') });

function closeRecipeModal() { recipeModal.classList.remove('open'); document.body.style.overflow = ''; clearTimer(); stopSpeech(); nextBtn.style.display = '' }
recipeClose.addEventListener('click', closeRecipeModal);
recipeModal.addEventListener('click', e => { if (e.target === recipeModal) closeRecipeModal() });

// ═══════════════ TIMER ═══════════════
function startTimer() {
  const btn = $('timerStartBtn');
  if (timerInterval) { clearTimer(); btn.textContent = '▶ Start'; return; }
  btn.textContent = '⏸ Pause';
  timerInterval = setInterval(() => {
    timerRemaining--;
    const d = $('timerDisplay');
    if (d) d.textContent = formatTime(timerRemaining);
    if (timerRemaining <= 0) { clearTimer(); if (d) { d.textContent = '✅ Done!'; d.style.color = 'var(--cardamom)' } if (btn) btn.textContent = '▶ Start'; }
  }, 1000);
}

function clearTimer() { if (timerInterval) { clearInterval(timerInterval); timerInterval = null; } }
function formatTime(s) { if (s <= 0) return "0:00"; const m = Math.floor(s / 60), sec = s % 60; return `${m}:${sec.toString().padStart(2, '0')}`; }

// ═══════════════ WEBCAM ═══════════════
webcamBtn.addEventListener('click', openWebcam);
closeWebcamBtn.addEventListener('click', closeWebcam);

async function openWebcam() {
  try {
    webcamStream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' }, audio: false });
    webcamVideo.srcObject = webcamStream;
    webcamModal.classList.add('open');
  } catch (e) { showError('Camera access failed: ' + e.message); }
}

function closeWebcam() {
  if (webcamStream) { webcamStream.getTracks().forEach(t => t.stop()); webcamStream = null; }
  webcamModal.classList.remove('open');
}

captureBtn.addEventListener('click', () => {
  const canvas = $('snapCanvas');
  canvas.width = webcamVideo.videoWidth;
  canvas.height = webcamVideo.videoHeight;
  canvas.getContext('2d').drawImage(webcamVideo, 0, 0);
  const dataURL = canvas.toDataURL('image/jpeg', .92);
  previewImg.src = dataURL;
  previewName.textContent = 'webcam_capture.jpg';
  previewSize.textContent = 'Live capture';
  previewContainer.classList.add('show');
  inputPlaceholder.classList.add('hidden');
  currentFile = null;
  closeWebcam();
  hideResults();
  runDetection(BACKEND_URL + '/detect_base64', JSON.stringify({ image: dataURL }));
});

// ═══════════════ HELPERS ═══════════════
function showError(msg) { errorBox.textContent = msg; errorBox.classList.toggle('show', !!msg); }
function hideResults() {
  resultsEl.style.display = 'none';
  loader.style.display = 'none';
  placeholderText.style.display = '';
}

