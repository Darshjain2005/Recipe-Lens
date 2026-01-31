const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.continuous = true; 
recognition.interimResults = true;

const BACKEND_URL = "http://127.0.0.1:5000";

let stage = "ingredients"; 
let searchResults = []; 
let servings = 1;
let recipeIndex = 0;
let currentStepIdx = 0;

const voiceText = document.getElementById("voice-text");
const recipeList = document.getElementById("recipes"); 
const feedbackMsg = document.getElementById("feedback-msg");

document.querySelector(".mic-btn").onclick = () => {
    recognition.start();
    voiceText.innerText = "Listening... List ingredients, then say 'DONE'.";
};

recognition.onresult = async (e) => {
    let text = "";
    for (let i = 0; i < e.results.length; i++) {
        text += e.results[i][0].transcript;
    }
    text = text.toLowerCase();
    voiceText.innerText = `Heard: "${text}"`;

    if (stage === "ingredients" && text.includes("done")) {
        recognition.stop(); // Stop mic to process
        
        // Extract info
        servings = extractServings(text);
        const knownIngs = ["potato", "tomato", "onion", "garlic", "chicken", "paneer", "rice", "matar"];
        let found = knownIngs.filter(i => text.includes(i));

        // Call Backend
        const res = await fetch(`${BACKEND_URL}/suggest-recipes`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ ingredients: found })
        });

        searchResults = await res.json();
        
        // REDISPLAY OPTIONS
        if (searchResults.length > 0) {
            renderRecipes(searchResults);
            speak(`I found ${searchResults.length} recipes. Say first, second, or third.`);
            stage = "choose";
        } else {
            speak("No recipes found. Please try again.");
            voiceText.innerText = "No matches. Try again.";
        }
    } 
    else if (stage === "choose") {
        let selectedIndex = -1;
        if (text.includes("first")) selectedIndex = 0;
        else if (text.includes("second")) selectedIndex = 1;
        else if (text.includes("third")) selectedIndex = 2;

        if (selectedIndex !== -1 && searchResults[selectedIndex]) {
            recognition.stop();
            recipeIndex = searchResults[selectedIndex].index; // Use REAL ID
            startCooking();
        }
    }
    else if (stage === "cook") {
        if (text.includes("next")) handleStepChange(1);
        else if (text.includes("previous")) handleStepChange(-1);
        else if (text.includes("stop")) location.reload();
    }
};

async function startCooking() {
    const res = await fetch(`${BACKEND_URL}/start-cooking`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ recipe_index: recipeIndex, servings })
    });
    const data = await res.json();
    currentStepIdx = 0;
    feedbackMsg.innerText = `Cooking: ${data.name}`;
    
    recipeList.innerHTML = '<div id="steps" style="color: white; font-weight: bold; font-size: 1.5rem; text-align: center; padding: 20px;"></div>';
    document.getElementById("steps").innerText = `Step 1: ${data.steps[0]}`;
    
    speak(`Starting ${data.name}. Step 1: ${data.steps[0]}`);
    stage = "cook";
}

async function handleStepChange(dir) {
    currentStepIdx = Math.max(0, currentStepIdx + dir);
    const res = await fetch(`${BACKEND_URL}/next-step`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ recipe_index: recipeIndex, step: currentStepIdx })
    });
    const data = await res.json();
    const stepsDisplay = document.getElementById("steps");

    if (data.done) {
        stepsDisplay.innerText = "Enjoy your meal!";
        speak("That was the last step. Enjoy!");
        stage = "ingredients";
    } else {
        stepsDisplay.innerText = `Step ${currentStepIdx + 1}: ${data.step}`;
        speak(data.step);
    }
}

recognition.onend = () => {
    // Re-start mic automatically if we are in choose or cook mode
    if (stage === "choose" || stage === "cook") {
        recognition.start();
    }
};

function renderRecipes(recipes) {
    recipeList.innerHTML = recipes.map((r, i) => `
        <div class="recipe-card" style="border: 2px solid #fff; margin: 10px; padding: 15px; border-radius: 12px; background: rgba(255,255,255,0.1); display: inline-block; width: 80%;">
            <p style="color: white; font-size: 1.2rem;"><strong>Option ${i+1}:</strong> ${r.name}</p>
        </div>
    `).join("") + '<div id="steps"></div>';
}

function extractServings(text) {
    const m = text.match(/(\d+)/);
    return m ? parseInt(m[1]) : 1;
}

function speak(text) {
    window.speechSynthesis.cancel(); 
    const u = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(u);
}