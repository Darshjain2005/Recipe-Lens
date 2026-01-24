import json
import os
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from gtts import gTTS
import playsound
import sys

# ---------- TEXT TO SPEECH ----------
def speak(text):
    print("Assistant:", text)
    temp_file = "voice.mp3"  # Windows-friendly temporary file
    tts = gTTS(text=text, lang="en")
    tts.save(temp_file)
    playsound.playsound(temp_file)
    os.remove(temp_file)

# ---------- VOSK COMMAND LISTENER ----------
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen_command(recognizer, mic_index=None):
    try:
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=8000,
            dtype="int16",
            channels=1,
            callback=callback,
            device=mic_index  # set correct mic index if needed
        ):
            while True:
                data = q.get()
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    text = result.get("text", "")
                    if text:
                        print("You said:", text)
                        return text.lower()
    except Exception as e:
        print("Microphone error:", e)
        return ""

# ---------- LOAD RECIPES ----------
def load_recipes():
    with open("../data/recipes.json", "r") as f:
        return json.load(f)

# ---------- SCALE INGREDIENTS ----------
def scale_ingredients(ingredients, servings):
    scaled = {}
    for k, v in ingredients.items():
        parts = v.split()
        try:
            qty = float(parts[0])
            unit = " ".join(parts[1:])
            scaled_qty = qty * servings
            scaled[k] = f"{scaled_qty} {unit}"
        except:
            scaled[k] = v
    return scaled

# ---------- COOKING MODE ----------
def cooking_mode(recipe, servings, recognizer, mic_index=None):
    steps = recipe["steps"]
    step_index = 0

    scaled_ingredients = scale_ingredients(recipe["ingredients"], servings)
    speak(f"Ingredients for {servings} serving(s):")
    for k, v in scaled_ingredients.items():
        speak(f"{k}: {v}")

    speak(f"Let's start cooking {recipe['name']}")
    speak(f"Step 1. {steps[step_index]}")

    while True:
        command = listen_command(recognizer, mic_index)
        if not command:
            speak("I could not hear you. Please say again.")
            continue

        if "next" in command:
            if step_index < len(steps) - 1:
                step_index += 1
                speak(f"Step {step_index + 1}. {steps[step_index]}")
            else:
                speak("You have completed all steps. Enjoy your meal!")
                break

        elif "previous" in command:
            if step_index > 0:
                step_index -= 1
                speak(f"Step {step_index + 1}. {steps[step_index]}")
            else:
                speak("This is the first step.")

        elif "repeat" in command:
            speak(f"Step {step_index + 1}. {steps[step_index]}")

        elif "stop" in command or "exit" in command:
            speak("Cooking stopped. Goodbye.")
            break

        else:
            speak("Please say next, previous, repeat, or stop.")

# ---------- MAIN ----------
if __name__ == "__main__":
    # Initialize Vosk model
    vosk_path = "vosk-model"  # model inside backend folder
    if not os.path.exists(vosk_path):
        print("VOSK model not found in backend/vosk-model")
        sys.exit(1)

    model = Model(vosk_path)
    recognizer = KaldiRecognizer(model, 16000)

    # Load recipes
    recipes = load_recipes()

    # Show top 5 recipes
    print("Top 5 Recipes:")
    for i, r in enumerate(recipes[:5]):
        print(f"{i+1}. {r['name']}")
    speak("Please type the number of the recipe you want to cook")
    choice = int(input("Select recipe (1-5): ")) - 1
    if choice < 0 or choice >= 5:
        print("Invalid choice.")
        sys.exit(1)

    # Ask number of servings
    speak("How many servings do you want to make?")
    while True:
        try:
            servings = int(input("Enter number of servings: "))
            if servings > 0:
                break
            else:
                print("Enter a number greater than 0.")
        except ValueError:
            print("Invalid input. Enter a number.")

    # Start cooking mode
    cooking_mode(recipes[choice], servings, recognizer)
