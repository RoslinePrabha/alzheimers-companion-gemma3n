import requests

def generate_quiz_question(patient_name="Rosline", topic="family"):
    prompt = f"""
You are a cognitive quiz generator for an Alzheimer's companion.

Generate one short and simple memory-based quiz question to help {patient_name} remember something about their life or surroundings.

Topic: {topic}

Format:
Question: <question here>
Answer: <answer here>

Make sure the question is easy and helps cognitive engagement.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "gemma:latest",
                "prompt": prompt,
                "stream": False
            }
        )
        data = response.json()
        output = data.get("response", "").strip()

        # Safety check
        if not output:
            return "❌ No quiz was generated. Please try a different topic or check if Gemma is running."

        return output

    except Exception as e:
        return f"❌ Error generating quiz: {str(e)}"
