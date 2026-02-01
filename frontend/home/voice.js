const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.continuous = true; 
recognition.interimResults = false; // Set to false to prevent multiple triggers per sentence

const BACKEND_URL = "http://127.0.0.1:5000";

let stage = "ingredients"; 
let searchResults = []; 
let servings = 1;
let recipeIndex = 0;
let currentStepIdx = 0;
let allSteps = [];

const voiceText = document.getElementById("voice-text");
const recipeList = document.getElementById("recipes"); 
const feedbackMsg = document.getElementById("feedback-msg");

document.querySelector(".mic-btn").onclick = () => {
    recognition.start();
    voiceText.innerText = "Listening... List ingredients, then say 'DONE'.";
};

recognition.onresult = async (e) => {
    // Only process the latest phrase spoken
    const resultIdx = e.resultIndex;
    let text = e.results[resultIdx][0].transcript.toLowerCase().trim();
    voiceText.innerText = `Heard: "${text}"`;

    // --- STAGE 1: INGREDIENTS ---
    if (stage === "ingredients" && text.includes("done")) {
        recognition.stop(); 
        
        servings = extractServings(text);
        const knownIngs = ["potato", "tomato", "onion", "garlic", "chicken", "paneer", "rice", "matar"];
        let found = knownIngs.filter(i => text.includes(i));

        const res = await fetch(`${BACKEND_URL}/suggest-recipes`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ ingredients: found })
        });

        searchResults = await res.json();
        
        if (searchResults.length > 0) {
            renderRecipes(searchResults);
            speak(`I found ${searchResults.length} recipes. Say first, second, or third.`);
            stage = "choose";
        } else {
            speak("No recipes found. Please try again.");
            voiceText.innerText = "No matches. Try again.";
        }
    } 
    // --- STAGE 2: CHOOSE RECIPE ---
    else if (stage === "choose") {
        let sel = -1;
        if (text.includes("first")) sel = 0;
        else if (text.includes("second")) sel = 1;
        else if (text.includes("third")) sel = 2;

        if (sel !== -1 && searchResults[sel]) {
            recognition.stop();
            recipeIndex = searchResults[sel].index; 
            startCooking();
        }
    }
    // --- STAGE 3: COOKING (Navigation, Repeat, and Stop) ---
    else if (stage === "cook") {
        if (text.includes("stop") || text.includes("exit")) {
            location.reload();
        } 
        else if (text.includes("repeat") || text.includes("again") || text.includes("say that again")) {
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

async function startCooking() {
    const res = await fetch(`${BACKEND_URL}/start-cooking`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ recipe_index: recipeIndex, servings })
    });
    const data = await res.json();
    
    allSteps = data.steps;
    currentStepIdx = 0;
    feedbackMsg.innerText = `Cooking: ${data.name}`;
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

    speak(`Starting ${data.name}. Step 1. ${allSteps[0]}`);
}

function handleStepChange(dir) {
    let newIndex = currentStepIdx + dir;

    if (newIndex < 0) {
        speak("You are already at the first step.");
        return;
    }
    if (newIndex >= allSteps.length) {
        speak("That was the last step. Enjoy your meal!");
        return;
    }

    // VISUAL UPDATE
    const oldStep = document.getElementById(`step-${currentStepIdx}`);
    if (oldStep) {
        oldStep.style.background = "transparent";
        oldStep.style.border = "none";
    }

    const nextStepEl = document.getElementById(`step-${newIndex}`);
    if (nextStepEl) {
        nextStepEl.style.background = "rgba(121, 215, 237, 0.2)";
        nextStepEl.style.border = "1px solid #79d7ed";
        nextStepEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    currentStepIdx = newIndex;
    speak(allSteps[currentStepIdx]);
}

recognition.onend = () => {
    if (stage === "choose" || stage === "cook") {
        recognition.start();
    }
};

function renderRecipes(recipes) {
    recipeList.innerHTML = recipes.map((r, i) => `
        <div class="recipe-card" style="border: 2px solid #fff; margin: 10px; padding: 15px; border-radius: 12px; background: rgba(255,255,255,0.1); display: inline-block; width: 80%;">
            <p style="color: white; font-size: 1.2rem;"><strong>Option ${i+1}:</strong> ${r.name}</p>
        </div>
    `).join("");
}

function extractServings(text) {
    const m = text.match(/(\d+)/);
    return m ? parseInt(m[1]) : 1;
}

function speak(text) {
    window.speechSynthesis.cancel(); 
    const u = new SpeechSynthesisUtterance(text);
    // Adjust rate for clarity
    u.rate = 0.9; 
    window.speechSynthesis.speak(u);
}