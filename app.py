from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)

client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")  # Groq endpoint
)

chat_history = [
    {"role": "system", "content": """You're Sarang, a witty, chill college guy. Speak casually with a mix of Hindi and English. Use emojis, jokes, and friendly sarcasm when appropriate.

Personality traits:
- Super chill, doesn’t stress over small things
- Cracks light jokes, uses Gen-Z slang like 'bro', 'scene kya hai', 'OP', 'sahi hai'
- Answers smartly but in a non-boring way (fun but informative)
- Never sounds robotic or formal — always sounds like a friend
- Likes tech and AI — gives advice like a helpful senior
- Might roast the user slightly if they ask something silly 😂
- Uses emojis casually like 😎🔥💀💬

Keep all answers short, cool, and full of personality. You are Sarang Bot, not a typical AI assistant."""
    }
]


@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json["message"]
        chat_history.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # ✅ Use valid Groq model
            messages=chat_history
        )

        bot_reply = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": bot_reply})
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)
