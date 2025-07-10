import os
import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import pyttsx3
import requests
import json
from tinydb import TinyDB
from datetime import datetime
import cv2
from PIL import Image
import torch
import clip

# Environment setup
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"
db = TinyDB('conversation_memory.json')
device = "cuda" if torch.cuda.is_available() else "cpu"
clip_model, preprocess = clip.load("ViT-B/32", device=device)

# 📁 Known photo database
photo_labels = {
    "daughter Priya": "photos/daughter_priya.jpg"
    # Add more labeled photos here
}

# 🎙️ Record voice
def record_audio(filename, duration=5, fs=44100):
    print("🎙️ Speak now...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    write(filename, fs, audio)
    print("✅ Done recording.")

# 🧠 Transcribe voice to text
def transcribe_audio(file_path):
    print("🧠 Transcribing...")
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result["text"]

# 🗣️ Speak response
def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# 👵 Patient info context
def get_patient_context():
    with open("patient_profile.json") as f:
        data = json.load(f)
    summary = f"""You are talking to {data['preferred_name']}.
Use a {data['voice_tone']} tone.
Family members include: {', '.join([f"{k}: {v}" for k, v in data['known_family'].items()])}.
Health: {', '.join(data['medical_history'])}.
Daily routine: {', '.join(data['daily_routine'])}.
"""
    return summary

# 🧠 Memory context
def get_recent_conversation(n=3):
    records = db.all()[-n:]
    summary = ""
    for record in records:
        summary += f"Earlier, the user said: {record['user']}\n"
        summary += f"You responded: {record['assistant']}\n"
    return summary

# 🤖 LLM response
def get_llm_response(prompt):
    context = get_patient_context()
    memory = get_recent_conversation()
    full_prompt = context + "\n" + memory + "\nNow the user says: " + prompt

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "gemma:latest", "prompt": full_prompt, "stream": False}
    )
    data = response.json()
    return data.get("response", "Sorry, I didn’t get that.")

# 🧠 Generate quiz with LLM
def generate_memory_quiz():
    context = get_patient_context()
    prompt = context + "\nGenerate a short memory quiz question for the patient."

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "gemma:latest", "prompt": prompt, "stream": False}
    )
    data = response.json()
    return data.get("response", "Could not generate a quiz right now.")

# 💾 Save memory
def save_to_memory(user_input, assistant_reply):
    db.insert({
        "timestamp": datetime.now().isoformat(),
        "user": user_input,
        "assistant": assistant_reply
    })

# 📷 Capture photo using webcam
def capture_photo_from_camera(output_path="captured_photo.jpg"):
    cam = cv2.VideoCapture(0)
    print("📸 Camera ready. Press SPACE to capture or ESC to cancel.")

    while True:
        ret, frame = cam.read()
        cv2.imshow("Capture - Press SPACE", frame)

        key = cv2.waitKey(1)
        if key % 256 == 32:  # SPACE pressed
            cv2.imwrite(output_path, frame)
            print(f"✅ Photo saved to {output_path}")
            break
        elif key % 256 == 27:  # ESC
            print("❌ Cancelled.")
            output_path = None
            break

    cam.release()
    cv2.destroyAllWindows()
    return output_path

# 🧠 Identify who is in the photo
def identify_person_from_photo(photo_path):
    if not photo_path or not os.path.exists(photo_path):
        return "No photo found to analyze."

    image = preprocess(Image.open(photo_path)).unsqueeze(0).to(device)
    texts = clip.tokenize(list(photo_labels.keys())).to(device)

    with torch.no_grad():
        image_features = clip_model.encode_image(image)
        text_features = clip_model.encode_text(texts)
        similarity = (image_features @ text_features.T).softmax(dim=-1)
        best_match = list(photo_labels.keys())[similarity.argmax().item()]
        confidence = similarity.max().item()

    return f"This appears to be {best_match} (confidence: {confidence:.2f})"

# 🚀 Main loop
def main():
    print("\nChoose mode:")
    print("1 - Voice Conversation")
    print("2 - Photo Recognition")
    print("3 - Memory Quiz")
    choice = input("Your choice: ").strip()

    if choice == "1":
        wav_file = "input.wav"
        record_audio(wav_file)
        user_text = transcribe_audio(wav_file)
        print("📝 You said:", user_text)

        response = get_llm_response(user_text)
        print("🤖 Companion says:", response)
        speak_text(response)
        save_to_memory(user_text, response)

    elif choice == "2":
        photo_path = capture_photo_from_camera()
        if photo_path:
            description = identify_person_from_photo(photo_path)
            print("🧠 Companion says:", description)
            speak_text(description)
        else:
            print("⚠️ No photo captured.")

    elif choice == "3":
        quiz = generate_memory_quiz()
        print("🧠 Quiz:", quiz)
        speak_text(quiz)
        save_to_memory("[Memory Quiz Request]", quiz)

    else:
        print("❌ Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
