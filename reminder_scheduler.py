import json
import schedule
import time
import pyttsx3
from datetime import datetime

def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def load_reminders():
    with open("reminders.json") as f:
        return json.load(f)

def setup_schedule():
    reminders = load_reminders()
    for item in reminders:
        schedule.every().day.at(item["time"]).do(speak_text, text=item["message"])
        print(f"✅ Reminder set for {item['time']}: {item['message']}")

def run_scheduler():
    setup_schedule()
    print("⏳ Reminder system running...\n")
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    run_scheduler()
