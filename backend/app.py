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
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

# ---------- VOSK COMMAND LISTENER ----------
q = queue.Queue()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen_command():
    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                text = json.loads(result).get("text", "")
                if text:
                    print("You said:", text)
                    return text.lower()

# ---------- LOAD RECIPES ----------
def load_recipes():
    with open("../data/recipes.json", "r") as f:
        return json.load(f)

# ---------- COOKING MODE ----------
def cooking_mode(recipe):
    steps = recipe["steps"]
    step_index = 0

    speak(f"Let's start cooking {recipe['name']}")
    speak(f"Step 1. {steps[step_index]}")

    while True:
        command = listen_command()

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
    if not os.path.exists("vosk-model"):
        print("VOSK model not found")
        sys.exit(1)

    model = Model("vosk-model")
    recognizer = KaldiRecognizer(model, 16000)

    recipes = load_recipes()
    recipe = recipes[0]   # first recipe for now

    cooking_mode(recipe)
