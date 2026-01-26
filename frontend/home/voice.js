const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";
recognition.continuous = false; // We manually restart it to keep things precise

let stage = "ingredients"; 
let currentIngredients = [];
let servings = 1;
let recipeIndex = 0;
let currentStepIdx = 0;

const voiceText = document.getElementById("voice-text");
const recipeList = document.getElementById("recipes");
const stepsDisplay = document.getElementById("steps");
const feedbackMsg = document.getElementById("feedback-msg");

document.querySelector(".mic-btn").onclick = () => recognition.start();

recognition.onresult = async (e) => {
    const text = e.results[0][0].transcript.toLowerCase();
    voiceText.innerText = `You said: "${text}"`;

    if (stage === "ingredients") {
        servings = extractServings(text);
        const knownIngs = ["potato", "tomato", "onion", "garlic", "chicken", "paneer", "rice"];
        currentIngredients = knownIngs.filter(i => text.includes(i));

        const res = await fetch("http://127.0.0.1:5000/suggest-recipes", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ ingredients: currentIngredients })
        });

        const data = await res.json();
        renderRecipes(data);
        speak("I found some recipes. Which one would you like? Say first, second, or third.");
        stage = "choose";
    }

    else if (stage === "choose") {
        if (text.includes("first")) recipeIndex = 0;
        else if (text.includes("second")) recipeIndex = 1;
        else if (text.includes("third")) recipeIndex = 2;

        const res = await fetch("http://127.0.0.1:5000/start-cooking", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ recipe_index: recipeIndex, servings })
        });

        const data = await res.json();
        currentStepIdx = 0;
        feedbackMsg.innerText = `Cooking: ${data.name}`;
        recipeList.innerHTML = ""; // Clear the list to show steps
        
        speak(`Starting ${data.name}. Step one: ${data.steps[0]}`);
        stepsDisplay.innerText = `Step 1: ${data.steps[0]}`;
        stage = "cook";
    }

    else if (stage === "cook") {
        if (text.includes("next")) {
            currentStepIdx++;
        } else if (text.includes("previous")) {
            currentStepIdx = Math.max(0, currentStepIdx - 1);
        } else if (text.includes("stop")) {
            speak("Cooking stopped.");
            stage = "ingredients";
            location.reload(); // Reset the page
            return;
        } 

        const res = await fetch("http://127.0.0.1:5000/next-step", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ recipe_index: recipeIndex, step: currentStepIdx })
        });

        const data = await res.json();
        if (data.done) {
            speak("That was the last step. Enjoy your meal!");
            stepsDisplay.innerText = "Enjoy your meal!";
            stage = "ingredients";
        } else {
            speak(data.step);
            stepsDisplay.innerText = `Step ${currentStepIdx + 1}: ${data.step}`;
        }
    }
};

// Auto-restart recognition if we are in the middle of cooking
recognition.onend = () => {
    if (stage === "cook" || stage === "choose") {
        recognition.start();
    }
};

function extractServings(text) {
    const m = text.match(/(\d+)/);
    return m ? parseInt(m[1]) : 1;
}

function renderRecipes(recipes) {
    if (recipes.length === 0) {
        recipeList.innerHTML = "<p>No recipes found for those ingredients.</p>";
        return;
    }
    recipeList.innerHTML = recipes.map((r, i) => `
        <div class="recipe-card" style="border: 1px solid #fff; margin: 5px; padding: 10px;">
            <p><strong>Option ${i+1}:</strong> ${r.name}</p>
        </div>
    `).join("");
}

function speak(text) {
    window.speechSynthesis.cancel(); // Stop any current speaking
    const u = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(u);
}