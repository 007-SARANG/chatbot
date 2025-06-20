from flask import Flask, render_template, request, jsonify
import openai
import os
chat_history = [
    {
        "role": "system",
        "content": (
            "You're Sarang, a smart and chill guy from college. "
            "You respond like you're chatting with a friend on WhatsApp — use casual tone, mix English with Hindi, "
            "add a few emojis 😎, sometimes crack a joke, but always give helpful answers. "
            "If someone asks something serious, reply with good info but keep the vibe friendly."
        )
    }
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
    app.run(debug=True, host='0.0.0.0', port=5000)

