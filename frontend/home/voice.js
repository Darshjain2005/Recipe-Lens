const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.continuous = false; 

// THE FIX: Point this specifically to your Flask Port
const BACKEND_URL = "http://127.0.0.1:5000";

let stage = "ingredients"; 
let currentIngredients = [];
let servings = 1;
let recipeIndex = 0;
let currentStepIdx = 0;

const voiceText = document.getElementById("voice-text");
const recipeList = document.getElementById("recipes"); 
const feedbackMsg = document.getElementById("feedback-msg");

document.querySelector(".mic-btn").onclick = () => recognition.start();

recognition.onresult = async (e) => {
    const text = e.results[0][0].transcript.toLowerCase();
    voiceText.innerText = `You said: "${text}"`;

    if (stage === "ingredients") {
        servings = extractServings(text);
        const knownIngs = ["potato", "tomato", "onion", "garlic", "chicken", "paneer", "rice"];
        currentIngredients = knownIngs.filter(i => text.includes(i));

        // FETCH 1: Suggest Recipes
        const res = await fetch(`${BACKEND_URL}/suggest-recipes`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ ingredients: currentIngredients })
        });

        const data = await res.json();
        renderRecipes(data);
        
        const feedback = "I found some recipes. Say first, second, or third.";
        const stepsDisplay = document.getElementById("steps");
        if (stepsDisplay) stepsDisplay.innerText = feedback;
        
        speak(feedback);
        stage = "choose";
    }

    else if (stage === "choose") {
        if (text.includes("first")) recipeIndex = 0;
        else if (text.includes("second")) recipeIndex = 1;
        else if (text.includes("third")) recipeIndex = 2;
        else return;

        // FETCH 2: Start Cooking
        const res = await fetch(`${BACKEND_URL}/start-cooking`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ recipe_index: recipeIndex, servings })
        });

        const data = await res.json();
        currentStepIdx = 0;
        feedbackMsg.innerText = `Cooking: ${data.name}`;
        
        recipeList.innerHTML = '<div id="steps" style="color: white; font-weight: bold; font-size: 1.5rem; text-align: center; padding: 20px;"></div>';
        
        const firstStep = `Step 1: ${data.steps[0]}`;
        document.getElementById("steps").innerText = firstStep; 
        
        speak(`Starting ${data.name}. ${firstStep}`);
        stage = "cook";
    }

    else if (stage === "cook") {
        if (text.includes("next")) {
            currentStepIdx++;
        } else if (text.includes("previous")) {
            currentStepIdx = Math.max(0, currentStepIdx - 1);
        } else if (text.includes("stop")) {
            location.reload();
            return;
        } 

        // FETCH 3: Next Step
        const res = await fetch(`${BACKEND_URL}/next-step`, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ recipe_index: recipeIndex, step: currentStepIdx })
        });

        const data = await res.json();
        const stepsDisplay = document.getElementById("steps");

        if (data.done) {
            if (stepsDisplay) stepsDisplay.innerText = "Enjoy your meal!";
            speak("That was the last step. Enjoy!");
            stage = "ingredients";
        } else {
            const stepText = `Step ${currentStepIdx + 1}: ${data.step}`;
            if (stepsDisplay) stepsDisplay.innerText = stepText; 
            speak(data.step);
        }
    }
};

recognition.onend = () => {
    if (stage === "cook" || stage === "choose") recognition.start();
};

function extractServings(text) {
    const m = text.match(/(\d+)/);
    return m ? parseInt(m[1]) : 1;
}

function renderRecipes(recipes) {
    let html = recipes.map((r, i) => `
        <div class="recipe-card" style="border: 1px solid #fff; margin: 10px; padding: 15px; border-radius: 10px; display: inline-block; background: rgba(255,255,255,0.1);">
            <p><strong>Option ${i+1}:</strong> ${r.name}</p>
        </div>
    `).join("");
    html += '<div id="steps" style="color: white; font-weight: bold; font-size: 1.5rem; text-align: center; padding: 20px;"></div>';
    recipeList.innerHTML = html;
}

function speak(text) {
    window.speechSynthesis.cancel(); 
    const u = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(u);
}