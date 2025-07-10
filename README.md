# Cognitive Companion for Alzheimer's Support

An AI-powered voice and photo assistant to support Alzheimer's patients with personalized interaction, memory reinforcement, and contextual conversations using Google Gemma 3n.

---

## 🧠 Features

### 👵 Personalized Support

* Patient profile with preferred name, tone, health history, and daily routine.
* Context-aware conversations powered by Gemma LLM via Ollama.

### 🗣️ Voice Interaction

* Record audio via microphone.
* Transcribe using OpenAI Whisper.
* Generate personalized responses with context.

### 📷 Photo Recognition

* Capture via webcam or upload.
* Identify people using OpenAI CLIP model.
* Customize photo-to-relation mapping in `photo_labels`.

### 🗂️ Memory & Logs

* Stores past interactions in `TinyDB` for building memory.
* Uses memory to continue meaningful conversations.

### ⏰ Routine Reminders

* Reads from `patient_profile.json > reminders`.
* Speaks upcoming reminders out loud.

---

## 🛠️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/alzheimers-companion.git
cd alzheimers-companion
```

### 2. Python Environment

* Python 3.10 or 3.11 recommended.
* Create a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Whisper + FFmpeg

* Install FFmpeg manually and set path:

  * Download from: [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
  * Extract and add `ffmpeg/bin` to your PATH

### 5. Ollama + Gemma

* Install Ollama: [https://ollama.com/](https://ollama.com/)
* Pull Gemma model:

```bash
ollama pull gemma
```

* Run Ollama locally (it runs by default on port `11434`)

---

## 🗃️ Project Structure

```
cognitive-companion/
├── main.py                    # Main program logic
├── gui_configurator.py       # GUI for setting up patient profile and family photos
├── rebuild_face_encodings.py # (Optional) for face_recognition-based matching
├── patient_profile.json      # Main patient context and data
├── conversation_memory.json  # Log of past voice conversations
├── photos/                   # Folder with labeled family member photos
├── captured_photo.jpg        # Temp file for photo recognition
├── requirements.txt          # All Python dependencies
```

---

## ⚙️ Configuration

### `patient_profile.json`

```json
{
  "preferred_name": "Rosline",
  "voice_tone": "calm and reassuring",
  "known_family": {
    "daughter": "Rosline",
    "grandson": "Cyrus",
    "husband": "Thomas"
  },
  "medical_history": ["diabetes", "mild memory loss"],
  "daily_routine": ["morning walk", "tea at 9AM", "puzzle time"],
  "reminders": ["Take medicine at 8AM", "Call daughter at 6PM"]
}
```

### `photo_labels` in `main.py`

```python
photo_labels = {
  "daughter Rosline": "photos/daughter_rosline.jpg",
  "grandson Cyrus": "photos/grandson_cyrus.jpg"
}
```

---

## ✅ Run the Assistant

```bash
python main.py
```

You will be asked to choose:

```
1 - Voice Conversation
2 - Photo Recognition
```

---

## 🚀 Upcoming Features

* 🧩 Cognitive Quiz Generator
* 📅 Daily Visual Timeline
* 🎯 Facial Memory Match Game
* 🧑‍⚕️ Medicine/Health Log Assistant
* 🌍 Localized Alerts + Emergency Button

---

## 📦 Requirements Summary

```
whisper
pyttsx3
sounddevice
scipy
requests
tinydb
opencv-python
Pillow
torch
clip-by-openai
```

> Optional: `face_recognition` + `dlib` (if switching to facial embedding matching)

---

## 📢 License & Hackathon Info

This project is developed for submission to the Google Gemma 3n Hackathon 2025.

All components are open source. You are welcome to fork and enhance it further for patient-specific care.

---

## 🧑‍💻 Contributors

* Rosline Prabha TM

---

Let’s bring compassionate AI to cognitive care. 💙
