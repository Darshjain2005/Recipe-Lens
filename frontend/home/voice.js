// ────────────────────────────────────────────────────────────
//  Recipe Lens — Voice Chef  (voice.js)
//  Improvements:
//   • Top-8 recipe selection (was top-3)
//   • Better speech recognition: interim previews, confidence
//     filtering, smarter restart, en-IN + en-US fallback
// ────────────────────────────────────────────────────────────

const BACKEND_URL = window.location.origin;

// ── State ──────────────────────────────────────────────────
let stage = "idle";          // idle → ingredients → servings → choose → confirm_start → cook
let searchResults    = [];
let servings         = 1;
let recipeIndex      = 0;
let currentStepIdx   = 0;
let allSteps         = [];
let detectedIngredients = [];
let isSpeaking       = false; // true while TTS is playing — don't restart recognition
let isListening      = false; // guard against double-start calls

// ── DOM refs ───────────────────────────────────────────────
const voiceText  = document.getElementById("voice-text");
const recipeList = document.getElementById("recipes");
const feedbackMsg = document.getElementById("feedback-msg");

// ── Speech Recognition setup ───────────────────────────────
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.lang             = "en-IN";  // Best for Indian accents; browser falls back to en-US
recognition.continuous       = false;    // Single-shot → restart manually; much more reliable
recognition.interimResults   = true;     // Show live visual preview of what's being heard
recognition.maxAlternatives  = 3;        // Let us pick the best alternative

// ── Safe start / stop helpers ──────────────────────────────
function startListening() {
    if (isSpeaking || isListening) return;
    try {
        recognition.start();
        isListening = true;
    } catch (e) {
        // Already started — ignore
    }
}

function stopListening() {
    try {
        recognition.stop();
    } catch (_) {}
    isListening = false;
}

// ── Mic button ─────────────────────────────────────────────
document.querySelector(".mic-btn").onclick = () => {
    stage = "ingredients";
    startListening();
    voiceText.innerText = "🎙️ Listening… Say your ingredients, then say DONE.";
};

// ── Interim result handler (live preview) ──────────────────
recognition.onresult = async (e) => {
    // Show interim transcript as the user speaks
    let interimTranscript = "";
    let finalTranscript   = "";

    for (let i = e.resultIndex; i < e.results.length; i++) {
        const result     = e.results[i];
        const transcript = result[0].transcript;
        if (result.isFinal) {
            // Pick the highest-confidence alternative
            let best = result[0];
            for (let j = 1; j < result.length; j++) {
                if (result[j].confidence > best.confidence) best = result[j];
            }
            finalTranscript += best.transcript;
        } else {
            interimTranscript += transcript;
        }
    }

    // Live preview of partial speech
    if (interimTranscript) {
        voiceText.innerText = `🎙️ Hearing: "${interimTranscript}"`;
    }

    // Only act on final results
    if (!finalTranscript) return;

    // Apply word-to-number conversion and clean up
    let rawText = finalTranscript.toLowerCase().trim();
    let text    = wordToNumber(rawText);
    voiceText.innerText = `✅ Heard: "${text}"`;

    await processCommand(text);
};

// ── Command processor (called on every final result) ───────
async function processCommand(text) {

    // ── STAGE 1: INGREDIENTS ───────────────────────────────
    if (stage === "ingredients" && text.includes("done")) {
        const knownIngs = [
            // Vegetables
            "potato", "tomato", "onion", "garlic", "peas", "carrot", "cabbage",
            "capsicum", "cauliflower", "spinach", "broccoli", "mushroom", "corn",
            "pumpkin", "eggplant", "cucumber", "okra", "beans", "bitter gourd",
            "bottle gourd", "tinda", "fenugreek", "banana",
            // Proteins
            "paneer", "chicken", "egg", "tofu",
            // Legumes & Grains
            "rice", "dal", "moong dal", "toor dal", "chickpeas", "kidney beans",
            "matar", "lentil",
            // Aromatics / Spices
            "ginger", "turmeric", "cumin", "coriander", "tamarind", "coconut"
        ];
        detectedIngredients = knownIngs.filter(i => text.includes(i));

        stage = "servings";
        speak("Got it! How many servings do you need?");
        return;
    }

    // ── STAGE 2: SERVINGS ──────────────────────────────────
    if (stage === "servings") {
        let detected = extractServings(text);
        if (detected !== null) {
            servings = detected;

            const res = await fetch(`${BACKEND_URL}/suggest-recipes`, {
                method:  "POST",
                headers: { "Content-Type": "application/json" },
                body:    JSON.stringify({ ingredients: detectedIngredients })
            });
            searchResults = await res.json();

            if (searchResults.length > 0) {
                renderRecipes(searchResults);
                stage = "choose";
                const count = searchResults.length;
                speak(`I found ${count} recipe${count > 1 ? "s" : ""}. Say a number from 1 to ${count}, or its name, to choose.`);
            } else {
                stage = "ingredients";
                speak("No recipes found. Please try again with different ingredients.");
            }
        }
        return;
    }

    // ── STAGE 3: CHOOSE RECIPE (supports 1-8) ─────────────
    if (stage === "choose") {
        let sel = resolveRecipeChoice(text);
        if (sel !== -1 && searchResults[sel]) {
            recipeIndex = searchResults[sel].index;
            showIngredients();
        }
        return;
    }

    // ── STAGE 4: CONFIRM START (kept for fallback — auto-advance is default) ────
    if (stage === "confirm_start") {
        // Auto-advance fires via timer in showIngredients(); voice "start" is a backup.
        if (text.includes("start") || text.includes("ready") || text.includes("yes") || text.includes("yeah")) {
            clearTimeout(window._autoStartTimer);
            startCooking();
        }
        return;
    }

    // ── STAGE 5: COOKING ───────────────────────────────────
    if (stage === "cook") {
        if (text.includes("stop") || text.includes("exit") || text.includes("quit")) {
            location.reload();
        } else if (text.includes("repeat") || text.includes("again")) {
            speak(`Repeating: ${allSteps[currentStepIdx]}`);
        } else if (text.includes("next")) {
            handleStepChange(1);
        } else if (text.includes("previous") || text.includes("back") || text.includes("prev")) {
            handleStepChange(-1);
        }
        return;
    }
}

// ── Resolve a recipe choice 1-8 from spoken text ───────────
function resolveRecipeChoice(text) {
    // Ordinal words map
    const ordinals = {
        "first":   0, "1": 0, "one":   0, "option 1": 0,
        "second":  1, "2": 1, "two":   1, "option 2": 1,
        "third":   2, "3": 2, "three": 2, "option 3": 2,
        "fourth":  3, "4": 3, "four":  3, "option 4": 3,
        "fifth":   4, "5": 4, "five":  4, "option 5": 4,
        "sixth":   5, "6": 5, "six":   5, "option 6": 5,
        "seventh": 6, "7": 6, "seven": 6, "option 7": 6,
        "eighth":  7, "8": 7, "eight": 7, "option 8": 7,
    };

    // Check ordinal words / numbers
    for (const [key, idx] of Object.entries(ordinals)) {
        if (text.includes(key)) return idx;
    }

    // Fuzzy name match — check if spoken text contains part of a recipe name
    for (let i = 0; i < searchResults.length; i++) {
        const nameLower = searchResults[i].name.toLowerCase();
        // Match if user says any significant word from the recipe name
        const words = nameLower.split(/\s+/).filter(w => w.length > 3);
        if (words.some(w => text.includes(w))) return i;
    }

    return -1;
}

// ── Show ingredient list before cooking ────────────────────
async function showIngredients() {
    const res = await fetch(`${BACKEND_URL}/start-cooking`, {
        method:  "POST",
        headers: { "Content-Type": "application/json" },
        body:    JSON.stringify({ recipe_index: recipeIndex, servings: servings })
    });
    const data = await res.json();
    allSteps = data.steps;

    feedbackMsg.innerText = `Recipe: ${data.name} (${servings} Serving${servings > 1 ? "s" : ""})`;

    // ── Render ingredient cards ────────────────────────────
    let ingHTML = `<div style="text-align:left;padding:20px;color:white;width:100%">
        <h2 style="color:#fff;margin-bottom:20px;font-size:1.6rem;text-align:center">
            Ingredients for ${servings} serving${servings > 1 ? "s" : ""}
        </h2>
        <div class="result-grid">`;

    // Build per-ingredient speech chunks (one utterance per item avoids Chrome 15s cutoff)
    const ingChunks = [];
    ingChunks.push(`For ${servings} serving${servings > 1 ? "s" : ""}, here are the ingredients.`);

    for (let item in data.ingredients) {
        let qty = data.ingredients[item];
        ingChunks.push(`${qty} of ${item}.`);
        ingHTML += `
        <div class="ingredient-card">
            <div class="ing-name">${item}</div>
            <div class="ing-qty">${qty}</div>
        </div>`;
    }
    ingHTML += `</div>
        <p style="text-align:center;margin-top:25px;color:#fff;font-weight:bold;font-size:1.2rem">
            Starting cooking in a moment…
        </p>
    </div>`;

    recipeList.innerHTML = ingHTML;
    stage = "confirm_start";

    // Read ingredients as chained short chunks, then auto-start cooking
    speakChunked(ingChunks, () => {
        // Auto-start cooking 1 second after last ingredient is read
        window._autoStartTimer = setTimeout(startCooking, 1000);
    });
}

// ── Start cooking — display all steps ──────────────────────
async function startCooking() {
    currentStepIdx = 0;
    feedbackMsg.innerText = "Cooking Mode";
    stage = "cook";

    let stepsHTML = `<div class="steps-container" style="text-align:left;padding:10px;width:100%;max-width:800px;margin:0 auto">`;
    allSteps.forEach((step, index) => {
        let activeClass = index === 0 ? "active" : "";
        stepsHTML += `
            <div id="step-${index}" class="cooking-step ${activeClass}">
                <div class="step-title">Step ${index + 1}</div>
                <div class="step-body-text">${step}</div>
            </div>`;
    });
    stepsHTML += `
        <div style="text-align:center;margin-top:20px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
            <div class="btn btn-outline btn-sm">Say 'Previous'</div>
            <div class="btn btn-muted btn-sm">Say 'Repeat'</div>
            <div class="btn btn-saffron btn-sm">Say 'Next'</div>
            <div class="btn btn-outline btn-sm" style="border-color:#C0392B;color:#C0392B">Say 'Stop'</div>
        </div>
    </div>`;
    recipeList.innerHTML = stepsHTML;

    speak(`Step 1. ${allSteps[0]}`);
}

// ── Handle step navigation ─────────────────────────────────
function handleStepChange(dir) {
    let newIndex = currentStepIdx + dir;
    if (newIndex < 0 || newIndex >= allSteps.length) {
        speak(newIndex < 0 ? "You are already at the first step." : "Last step! Enjoy your meal!");
        return;
    }

    const oldStep = document.getElementById(`step-${currentStepIdx}`);
    if (oldStep) oldStep.classList.remove("active");

    const nextStepEl = document.getElementById(`step-${newIndex}`);
    if (nextStepEl) {
        nextStepEl.classList.add("active");
        nextStepEl.scrollIntoView({ behavior: "smooth", block: "center" });
    }

    currentStepIdx = newIndex;
    speak(`Step ${currentStepIdx + 1}. ${allSteps[currentStepIdx]}`);
}

// ── Render recipe cards (up to 8) ─────────────────────────
function renderRecipes(recipes) {
    recipeList.innerHTML = `<div class="dishes-grid">` +
        recipes.map((r, i) => `
            <div class="dish-card">
                <span class="dish-emoji">🍽️</span>
                <div class="dish-name">${r.name}</div>
                <div class="dish-hint">Option ${i + 1}</div>
            </div>
        `).join("") +
    `</div>`;
}

// ── Recognition lifecycle ──────────────────────────────────
recognition.onend = () => {
    isListening = false;
    // Auto-restart unless TTS is speaking or we're in idle state
    if (!isSpeaking && stage !== "idle") {
        setTimeout(startListening, 250);
    }
};

recognition.onerror = (e) => {
    isListening = false;
    if (e.error === "no-speech") {
        if (!isSpeaking && stage !== "idle") setTimeout(startListening, 500);
        return;
    }
    if (e.error === "aborted") return;
    console.warn("Voice recognition error:", e.error);
    voiceText.innerText = `⚠️ Mic error (${e.error}). Tap mic to try again.`;
};

// ── Pick best TTS voice ────────────────────────────────────
function getBestVoice() {
    const voices = window.speechSynthesis.getVoices();
    return voices.find(v => v.name.includes("Google") && v.lang.startsWith("en-IN")) ||
           voices.find(v => v.name.includes("Google") && v.lang.startsWith("en-US")) ||
           voices.find(v => v.name.includes("Google") && v.lang.startsWith("en-GB")) ||
           voices.find(v => v.lang.startsWith("en"));
}

// ── speak() — single short utterance ──────────────────────
//   Use speakChunked() for long text (ingredient lists, etc.)
function speak(text, onDone) {
    window.speechSynthesis.cancel();
    isSpeaking = true;
    stopListening();

    const u = new SpeechSynthesisUtterance(text);
    const v = getBestVoice();
    if (v) u.voice = v;
    u.rate  = 0.93;
    u.pitch = 1.0;

    u.onend = () => {
        isSpeaking = false;
        if (onDone) { onDone(); return; }
        if (stage !== "idle") setTimeout(startListening, 400);
    };
    u.onerror = () => {
        isSpeaking = false;
        if (onDone) { onDone(); return; }
        if (stage !== "idle") setTimeout(startListening, 400);
    };

    window.speechSynthesis.speak(u);
}

// ── speakChunked() — read an array of strings one at a time ──
//   Beats the Chrome ~15 second TTS cutoff for long lists.
//   Calls onAllDone() after the last chunk finishes.
function speakChunked(chunks, onAllDone) {
    window.speechSynthesis.cancel();
    isSpeaking = true;
    stopListening();

    const voice = getBestVoice();

    function speakNext(index) {
        if (index >= chunks.length) {
            isSpeaking = false;
            if (onAllDone) onAllDone();
            return;
        }
        const u = new SpeechSynthesisUtterance(chunks[index]);
        if (voice) u.voice = voice;
        u.rate  = 0.93;
        u.pitch = 1.0;
        u.onend   = () => speakNext(index + 1);
        u.onerror = () => speakNext(index + 1); // skip broken chunk
        window.speechSynthesis.speak(u);
    }

    speakNext(0);
}

// Voices load asynchronously in some browsers
if (speechSynthesis.onvoiceschanged !== undefined) {
    speechSynthesis.onvoiceschanged = () => {};
}

// ── Utility: convert common spoken number words → digits ──
function wordToNumber(text) {
    const map = {
        "one": "1",   "first":   "1", "single": "1",
        "two": "2",   "second":  "2", "to": "2", "too": "2",
        "three": "3", "third":   "3",
        "four": "4",  "fourth":  "4", "for": "4",
        "five": "5",  "fifth":   "5",
        "six": "6",   "sixth":   "6",
        "seven": "7", "seventh": "7",
        "eight": "8", "eighth":  "8",
    };
    return text.split(" ").map(w => map[w] || w).join(" ");
}

// ── Utility: extract a numeric serving size ─────────────────
function extractServings(text) {
    const m = text.match(/\b(\d+)\b/);
    if (m) {
        let num = parseInt(m[1]);
        // Fix speech-to-text doubling: "22" → "2", "33" → "3"
        if (num > 10 && num % 11 === 0) return parseInt(String(num)[0]);
        if (num > 15) return parseInt(String(num)[0]); // cap unrealistic values
        return num;
    }
    return null;
}