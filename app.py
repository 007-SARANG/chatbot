from flask import Flask, render_template, request, jsonify
import openai
import os
chat_history = [
    {"role": "system", "content": "You are Sarang, a chill, witty, and friendly person who talks casually. You mix Hindi and English, sometimes add emojis 😎, and keep things light-hearted. You joke around but also give useful answers."}
]

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")  # set your key in environment

chat_history = []

@app.route("/")
def home():
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    chat_history.append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )

    reply = response["choices"][0]["message"]["content"]
    chat_history.append({"role": "assistant", "content": reply})
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
