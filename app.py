from flask import Flask, jsonify, render_template
import json
import random

app = Flask(__name__)

def load_questions():
    with open("tests.json", "r", encoding="utf-8") as file:
        return json.load(file)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_test", methods=["GET"])
def get_test():
    questions = load_questions()
    question = random.choice(questions)
    return jsonify(question)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
