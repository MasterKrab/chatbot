from flask import Flask, request, jsonify
from chatmanager import ChatManager

app = Flask(__name__)
chat_manager = ChatManager()


@app.route("/generate", methods=["POST"])
def generate():
    question = request.json["question"]
    chat_response = chat_manager.generate(question)
    return jsonify({"response": chat_response})
