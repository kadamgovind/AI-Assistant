from groq import Groq
import os
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

# ✅ Get API key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("❌ GROQ_API_KEY not found in .env file")

# ✅ Create client
client = Groq(api_key=GROQ_API_KEY)


# -----------------------------
# 🤖 AI Response Function
# -----------------------------
def get_ai_response(text: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are Aira, a smart voice assistant. Reply short and helpful."
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0.7
        )

        return response.choices[0].message.content

    except Exception as e:
        print("AI ERROR:", str(e))
        return "❌ AI error, try again"