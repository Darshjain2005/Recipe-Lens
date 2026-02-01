# 🎙️ Recipe Lens: Voice & Vision AI Sous Chef

**Recipe Lens** is an interactive web application designed to simplify the cooking process through **Voice Commands** and **Computer Vision**. Users can search for recipes by talking to the app or showing ingredients to the camera, making it a truly hands-free kitchen assistant.

---

## 🚀 Key Features

* **AI Vision Search:** Identify ingredients instantly using the camera.
* **Voice-Controlled Navigation:** Search, select, and follow recipes using speech.
* **Smart Silence Detection:** Allows users to speak at their own pace; processing only begins after the keyword **"Done"** is heard.
* **Relational SQLite Database:** Fast and accurate mapping of ingredients to a 100+ recipe dataset.
* **Dynamic Scaling:** Voice-activated serving adjustment (e.g., "Make it for 4 people").
* **Step-by-Step Guidance:** Interactive "Next" and "Previous" voice commands for cooking instructions.

---

## 🛠️ Tech Stack

* **Frontend:** HTML5, CSS3, JavaScript (Web Speech API, MediaDevices API)
* **Backend:** Python 3, Flask, Flask-CORS
* **Database:** SQLite3
* **Vision:** Integrated ML Model for Object Detection (Vision Stage)

---

## 📂 Project Structure

```text
recipe-lens/
├── backend/
│   ├── app.py                # Flask API Server
│   ├── utils.py              # SQL Database Queries & Logic
│   ├── database_setup.py     # Database Initialization Script
│   ├── recipes.db            # SQLite Database File
│   └── data/
│       └── recipes.json      # Source data for migration
└── frontend/
    └── home/
        ├── home.html         # Main User Interface
        ├── voice.js          # Speech Logic & API Integration
        └── vision.js         # Camera Handling & Image Logic

