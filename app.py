from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

chat_history = [
    {"role": "system", "content": "You're Sarang, a chill, witty college guy. Talk like a close friend — mix Hindi-English, crack jokes, use emojis 😎."}
]

@app.route("/")
def index():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    chat_history.append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )

    bot_reply = response["choices"][0]["message"]["content"]
    chat_history.append({"role": "assistant", "content": bot_reply})
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
