const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-IN"; // changed from en-US to better understand Indian accents
recognition.continuous = true;
recognition.interimResults = false;

const BACKEND_URL = window.location.origin;

let stage = "ingredients";
let searchResults = [];
let servings = 1;
let recipeIndex = 0;
let currentStepIdx = 0;
let allSteps = [];
let detectedIngredients = [];

const voiceText = document.getElementById("voice-text");
const recipeList = document.getElementById("recipes");
const feedbackMsg = document.getElementById("feedback-msg");

// Helper to convert words to numbers to help the AI "understand" better
function wordToNumber(text) {
    const numbers = {
        'one': 1, 'first': 1, 'single': 1,
        'two': 2, 'to': 2, 'too': 2, 'second': 2,
        'three': 3, 'third': 3,
        'four': 4, 'for': 4, 'fourth': 4,
        'five': 5, 'fifth': 5,
        'six': 6, 'sixth': 6
    };
    let words = text.split(" ");
    return words.map(word => numbers[word] || word).join(" ");
}

document.querySelector(".mic-btn").onclick = () => {
    recognition.start();
    voiceText.innerText = "Listening... List ingredients, then say 'DONE'.";
};

recognition.onresult = async (e) => {
    const resultIdx = e.resultIndex;
    let rawText = e.results[resultIdx][0].transcript.toLowerCase().trim();

    // Clean the text immediately so "to" becomes "2" etc.
    let text = wordToNumber(rawText);
    voiceText.innerText = `Heard: "${text}"`;

    // --- STAGE 1: INGREDIENTS ---
    if (stage === "ingredients" && text.includes("done")) {
        const knownIngs = [
            // Vegetables (all in database)
            "potato", "tomato", "onion", "garlic", "peas", "carrot", "cabbage",
            "capsicum", "cauliflower", "spinach", "broccoli", "mushroom", "corn",
            "pumpkin", "eggplant", "cucumber", "okra", "beans", "bitter gourd",
            "bottle gourd", "tinda", "fenugreek", "banana",
            // Proteins
            "paneer", "chicken", "egg", "tofu",
            // Legumes & Grains
            "rice", "dal", "moong dal", "toor dal", "chickpeas", "kidney beans",
            "matar", "lentil",
            // Others
            "ginger", "turmeric", "cumin", "coriander", "tamarind", "coconut"
        ];
        detectedIngredients = knownIngs.filter(i => text.includes(i));


        stage = "servings";
        speak("How many servings do you need?");
    }

    // --- STAGE 2: ASK SERVINGS ---
    else if (stage === "servings") {
        let detected = extractServings(text);
        if (detected !== null) {
            servings = detected;
            const res = await fetch(`${BACKEND_URL}/suggest-recipes`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ingredients: detectedIngredients })
            });

            searchResults = await res.json();

            if (searchResults.length > 0) {
                renderRecipes(searchResults);
                stage = "choose";
                speak(`I found ${searchResults.length} recipes. Say first, second, or third.`);
            } else {
                stage = "ingredients";
                speak("No recipes found. Please try again.");
            }
        }
    }

    // --- STAGE 3: CHOOSE RECIPE ---
    else if (stage === "choose") {
        let sel = -1;
        if (text.includes("1") || text.includes("first")) sel = 0;
        else if (text.includes("2") || text.includes("second")) sel = 1;
        else if (text.includes("3") || text.includes("third")) sel = 2;

        if (sel !== -1 && searchResults[sel]) {
            recipeIndex = searchResults[sel].index;
            showIngredients();
        }
    }

    // --- STAGE 4: CONFIRM START ---
    else if (stage === "confirm_start") {
        if (text.includes("start") || text.includes("ready") || text.includes("yes")) {
            startCooking();
        }
    }

    // --- STAGE 5: COOKING ---
    else if (stage === "cook") {
        if (text.includes("stop") || text.includes("exit")) {
            location.reload();
        }
        else if (text.includes("repeat") || text.includes("again")) {
            speak(`Repeating: ${allSteps[currentStepIdx]}`);
        }
        else if (text.includes("next")) {
            handleStepChange(1);
        }
        else if (text.includes("previous") || text.includes("back")) {
            handleStepChange(-1);
        }
    }
};

async function showIngredients() {
    const res = await fetch(`${BACKEND_URL}/start-cooking`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ recipe_index: recipeIndex, servings: servings })
    });
    const data = await res.json();
    allSteps = data.steps;

    feedbackMsg.innerText = `Recipe: ${data.name} (${servings} Servings)`;

    let ingHTML = `<div style="text-align: left; padding: 20px; color: white; width: 100%;">
        <h2 style="color: #fff; margin-bottom: 20px; font-size: 1.6rem; text-align: center;">Ingredients for ${servings}</h2>
        <div class="result-grid">`;

    let speechText = `For ${servings} servings, you need: `;
    for (let item in data.ingredients) {
        let qty = data.ingredients[item];
        speechText += `${qty} of ${item}, `;

        ingHTML += `
        <div class="ingredient-card">
            <div class="ing-name">${item}</div>
            <div class="ing-qty">${qty}</div>
        </div>`;
    }
    ingHTML += `</div><p style="text-align: center; margin-top: 25px; color: #fff; font-weight: bold; font-size: 1.2rem;">Say "START" to begin!</p></div>`;

    recipeList.innerHTML = ingHTML;
    stage = "confirm_start";
    speak(speechText + " Shall we start?");
}

async function startCooking() {
    currentStepIdx = 0;
    feedbackMsg.innerText = `Cooking Mode`;
    stage = "cook";

    let stepsHTML = `<div class="steps-container" style="text-align: left; padding: 10px; width: 100%; max-width: 800px; margin: 0 auto;">`;
    allSteps.forEach((step, index) => {
        let activeClass = (index === 0) ? "active" : "";
        stepsHTML += `
            <div id="step-${index}" class="cooking-step ${activeClass}">
                <div class="step-title">Step ${index + 1}</div>
                <div class="step-body-text">${step}</div>
            </div>`;
    });
    stepsHTML += `
        <div style="text-align: center; margin-top: 20px; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap;">
            <div class="btn btn-outline btn-sm">Say 'Previous'</div>
            <div class="btn btn-muted btn-sm">Say 'Repeat'</div>
            <div class="btn btn-saffron btn-sm">Say 'Next'</div>
            <div class="btn btn-outline btn-sm" style="border-color: #C0392B; color: #C0392B;">Say 'Stop'</div>
        </div>
    </div>`;
    recipeList.innerHTML = stepsHTML;

    speak(`Step 1. ${allSteps[0]}`);
}

function handleStepChange(dir) {
    let newIndex = currentStepIdx + dir;
    if (newIndex < 0 || newIndex >= allSteps.length) {
        speak(newIndex < 0 ? "First step." : "Last step. Enjoy!");
        return;
    }

    const oldStep = document.getElementById(`step-${currentStepIdx}`);
    if (oldStep) { oldStep.classList.remove("active"); }

    const nextStepEl = document.getElementById(`step-${newIndex}`);
    if (nextStepEl) {
        nextStepEl.classList.add("active");
        nextStepEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    currentStepIdx = newIndex;
    speak(allSteps[currentStepIdx]);
}

// Improved end logic: ensure recognition doesn't stop during the conversation
recognition.onend = () => {
    recognition.start();
};

function renderRecipes(recipes) {
    recipeList.innerHTML = `<div class="dishes-grid">` + recipes.map((r, i) => `
        <div class="dish-card">
            <span class="dish-emoji">🍽️</span>
            <div class="dish-name">${r.name}</div>
            <div class="dish-hint">Option ${i + 1}</div>
        </div>
    `).join("") + `</div>`;
}

function extractServings(text) {
    // Only match the first instance of a standalone number to fix the "1 1" -> 11 bug
    const m = text.match(/\b(\d+)\b/);
    if (m) {
        let num = parseInt(m[1]);
        if (num > 10 && num % 11 === 0) {
            // Revert "22", "33" to "2", "3" (when user repeated digit)
            return parseInt(String(num)[0]);
        }
        if (num > 15) {
            // General cap for unrealistic serving sizes
            return parseInt(String(num)[0]);
        }
        return num;
    }
    return null;
}

function speak(text) {
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);

    let voices = window.speechSynthesis.getVoices();
    let preferredVoice = voices.find(v => v.name.includes("Google") && v.lang.includes("en-IN")) ||
        voices.find(v => v.name.includes("Google") && v.lang.includes("en-US")) ||
        voices.find(v => v.name.includes("Google") && v.lang.includes("en-GB")) ||
        voices.find(v => v.lang.startsWith("en"));
    if (preferredVoice) {
        u.voice = preferredVoice;
    }

    u.rate = 0.95;

    // We pause recognition while the AI is talking to prevent it from hearing itself
    u.onstart = () => { recognition.abort(); };
    u.onend = () => { recognition.start(); };

    window.speechSynthesis.speak(u);
}