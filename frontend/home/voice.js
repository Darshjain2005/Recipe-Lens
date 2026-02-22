const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
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
        const knownIngs = ["potato", "tomato", "onion", "garlic", "chicken", "paneer", "rice", "matar"];
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
                headers: {"Content-Type": "application/json"},
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
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ recipe_index: recipeIndex, servings: servings })
    });
    const data = await res.json();
    allSteps = data.steps; 
    
    feedbackMsg.innerText = `Recipe: ${data.name} (${servings} Servings)`;
    
    let ingHTML = `<div style="text-align: left; padding: 20px; color: white; width: 100%;">
        <h2 style="color: #79d7ed; margin-bottom: 15px;">Ingredients for ${servings}</h2>
        <ul style="list-style: none; font-size: 1.2rem; line-height: 2;">`;
    
    let speechText = `For ${servings} servings, you need: `;
    for (let item in data.ingredients) {
        let qty = data.ingredients[item];
        speechText += `${qty} of ${item}, `;
        ingHTML += `<li style="border-bottom: 1px solid rgba(255,255,255,0.1); padding: 5px 0;">
            <span style="color: #79d7ed;">✔</span> <strong>${qty}</strong> ${item}
        </li>`;
    }
    ingHTML += `</ul><p style="text-align: center; margin-top: 20px; color: #79d7ed; font-weight: bold;">Say "START" to begin!</p></div>`;
    
    recipeList.innerHTML = ingHTML;
    stage = "confirm_start";
    speak(speechText + " Shall we start?");
}

async function startCooking() {
    currentStepIdx = 0;
    feedbackMsg.innerText = `Cooking Mode`;
    stage = "cook";

    let stepsHTML = `<div class="steps-container" style="text-align: left; padding: 20px;">`;
    allSteps.forEach((step, index) => {
        let activeStyle = (index === 0) ? "background: rgba(121, 215, 237, 0.2); border: 1px solid #79d7ed;" : "";
        stepsHTML += `
            <div id="step-${index}" class="step-item" style="margin-bottom: 15px; padding: 15px; border-radius: 12px; color: white; transition: 0.3s; ${activeStyle}">
                <strong style="color: #79d7ed;">Step ${index + 1}:</strong> ${step}
            </div>`;
    });
    stepsHTML += `</div>`;
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
    if (oldStep) { oldStep.style.background = "transparent"; oldStep.style.border = "none"; }

    const nextStepEl = document.getElementById(`step-${newIndex}`);
    if (nextStepEl) {
        nextStepEl.style.background = "rgba(121, 215, 237, 0.2)";
        nextStepEl.style.border = "1px solid #79d7ed";
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
    recipeList.innerHTML = recipes.map((r, i) => `
        <div class="recipe-card" style="border: 2px solid #fff; margin: 10px; padding: 15px; border-radius: 12px; background: rgba(255,255,255,0.1); display: inline-block; width: 80%;">
            <p style="color: white; font-size: 1.2rem;"><strong>Option ${i+1}:</strong> ${r.name}</p>
        </div>
    `).join("");
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
    u.rate = 0.95;

    // We pause recognition while the AI is talking to prevent it from hearing itself
    u.onstart = () => { recognition.abort(); };
    u.onend = () => { recognition.start(); };
    
    window.speechSynthesis.speak(u);
}